# ./venv/bin/python3 app.py

import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService

from webdriver_manager.chrome import ChromeDriverManager

import os
import time

def download_zip(quarter_offset: int):
    cwd = os.getcwd()
    try:
        chrome_options = Options()
        prefs = {'download.default_directory': cwd}
        chrome_options.add_experimental_option('prefs', prefs)

        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

        driver.get('https://cdr.ffiec.gov/public/PWS/DownloadBulkData.aspx')

        type_selection = driver.find_element(By.XPATH, '//*[@id="ListBox1"]/option[1]')
        type_selection.click() # Call Reports -- single period

        # select the corresponding quarteer to quarter_offset throught the selctions dropdown
        quarter_selector = Select( driver.find_element(By.XPATH, '//*[@id="DatesDropDownList"]') )
        quarter_selector.select_by_index(quarter_offset) 

        download_button = driver.find_element(By.XPATH, '//*[@id="Download_0"]')
        download_button.click()

        time.sleep(4)

        driver.close()

    except:
        raise Exception('issue scraping data')

def lambda_handler(event, context):
    print('it worked')


    # TODO
    # quarter offset needs grabbed from event
    # unzip the folder
    quarter_offset = -1
    quarter_offset = -quarter_offset
    
    download_zip(quarter_offset=quarter_offset)

    
    
    
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'hello, world.'})
    }

lambda_handler(1, 1)