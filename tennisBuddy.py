from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from time import sleep, time
from datetime import datetime
import json


def cleanData(freeTimes):
    cleanedTimes = freeTimes[0].replace("\nVaraa", " ").strip().split()[1:]
    cleanedHalves = freeTimes[1].replace("\nVaraa", " ").strip().split()
    return (cleanedTimes, cleanedHalves)


startTime = time()

URL = 'https://tampereentenniskeskus.cintoia.com/'
CALENDAR_BUTTON_XPATH = '//*[@id="root"]/div/div[2]/div[2]/div/div[2]/span[1]'
DATE_X_PATH = '//*[@id="date"]'
NEXT_DAY_X_PATH = '//*[@id="root"]/div/div[2]/div[1]/div[1]/button[2]/span[1]/*[name()="svg"]'

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disabled-dev-shm-usage")

currentTime = datetime.now()
print(f"Current time is {currentTime}.")
webdriver_service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)
driver.get(URL)
sleep(3)

currentDateString = driver.find_element(By.XPATH, DATE_X_PATH) \
    .get_attribute("value")

previousDate = None
driver.find_element(By.XPATH, CALENDAR_BUTTON_XPATH).click()

dateDict = {}
while currentDateString != previousDate:
    currentDateDict = {}
    print(f"Current Date is: {currentDateString}")

    # This has to be fast as the page pings the server every couple seconds and messes up the selectors.
    tableRows = driver \
        .find_element(By.TAG_NAME, "tbody") \
        .find_elements(By.TAG_NAME, "tr")
    if len(tableRows) > 0:
        for row in tableRows:
            # Handle days without any free courts.
            try:
                court = row.find_element(By.TAG_NAME, "th").text
            except(StaleElementReferenceException, NoSuchElementException): 
                break
            halves = row.find_elements(By.XPATH, "./td[contains(@style, 'background: repeating-linear-gradient')]")
            halvesAsString = " ".join(f"{half.text}" for half in halves)
            currentDateDict[court] = (row.text, halvesAsString)
    else:
        # TODO: Log error and terminate.
        print("Error")
        exit()

    dateDict[currentDateString] = currentDateDict
    driver.find_element(By.XPATH, NEXT_DAY_X_PATH).click()
    sleep(1)
    previousDate = currentDateString
    currentDateString = driver.find_element(
        By.XPATH, DATE_X_PATH).get_attribute("value")

driver.quit()

# A bit of cleaning must be done here.
print(f"Stopping at {currentDateString}.")
cleanBatchData = {}
for date, courts in dateDict.items():
    cleanedCourtData = {court: cleanData(freeTimes) for court, freeTimes in courts.items()}
    cleanBatchData[date] = cleanedCourtData

# for k, v in cleanBatchData.items():
#     print(k)
#     for c, t in v.items():
#         print(f"----{c}")
#         print(f"--------Allcourts: {t[0]}")
#         if len(t[1]) > 0:
#             print(f"--------Half an hour: {t[1]}")

# Specify the file path
file_path = 'output.json'

# Write the data to the JSON file
with open(file_path, 'w') as json_file:
    json.dump(cleanBatchData, json_file, indent=2)

endTime = time()
print(f"Done in {endTime - startTime} seconds.")
