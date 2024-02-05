import json
import sys
from datetime import time, timedelta, datetime
import sqlite3

"""
This script checks if the court is free 15 minutes before the time slots starts. If slot is free saves the information
to a db.
"""
date = sys.argv[1]

data = []
with open(f'./data/merged_files/{date}.json', 'r') as json_file:
    json_object_list = json.load(json_file)
    for json_object in json_object_list:
        json_date: str = json_object["time"]
        batch_date = datetime.fromisoformat(json_date)
        reference_time = (batch_date + timedelta(minutes=15)).time()

        date_data = json_object[date]
        for k,v in date_data.items():
            for free_time in v[0]:
                if len(free_time) < 5:
                    time_obj = time.fromisoformat('0' + free_time)
                    
                else:
                    time_obj = time.fromisoformat(free_time)
                if time_obj < reference_time:
                    data.append((k[1:], date, time_obj.strftime('%H:%M')))

if len(data) > 0:
    db_connection = sqlite3.connect("tennisData.db")
    db_cursor = db_connection.cursor()
    db_cursor.executemany("INSERT INTO free_courts VALUES(?, ?, ?)", data)
    db_connection.commit()
    db_connection.close()
