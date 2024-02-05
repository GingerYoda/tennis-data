### Dependencies

1. Virtual enviroment: 

    $ apt install python3.10-venv
    $ python3 -m venv ./venv/

2. Python modules: selenium and webdriver-manager: 

    $ pip install selenium
    $ pip install webdriver-manager

3. Chrome browser:

    $ wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
    $ sudo apt install ./google-chrome-stable_current_amd64.deb

4. Other

    $ sudo apt install jq
### Set up

1. Install dependencies above

2. set up a cronjob something like "*/15 * * * * /path/runScraper.sh"


### TODO:

- Add something smart to handle all this above.
- File hierarchy must be fixed -> monthly directories
- No need to run scraper that often every half an hour?
