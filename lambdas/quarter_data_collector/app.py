from file_utils import get_zip_name, unzip, clean_dir

import json
import os
import time

from selenium import webdriver
from tempfile import mkdtemp
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


def download_zip(chrome: webdriver.Chrome, quarter_offset: int):
    chrome.get('https://cdr.ffiec.gov/public/PWS/DownloadBulkData.aspx')
    # Select 'Call Reports -- Single Period'
    report_type_selection = chrome.find_element(By.XPATH, '//*[@id="ListBox1"]/option[1]')
    report_type_selection.click() 

    # select the corresponding quarter based on quarter_offset parameter throught the selctions dropdown
    quarter_selector = Select( chrome.find_element(By.XPATH, '//*[@id="DatesDropDownList"]') )
    quarter_selector.select_by_index(quarter_offset)

    # click download button
    download_button = chrome.find_element(By.XPATH, '//*[@id="Download_0"]')
    download_button.click()

    # wait to give time to download and close browser
    time.sleep(4)
    chrome.close()
    

def lambda_handler(event, context):
    # NEED TO GET QUARTER OFFSET FROM EVENT
    
    options = webdriver.ChromeOptions()
    options.binary_location = '/opt/chrome/chrome'
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280x1696")
    options.add_argument("--single-process")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-dev-tools")
    options.add_argument("--no-zygote")
    options.add_argument(f"--user-data-dir={mkdtemp()}")
    options.add_argument(f"--data-path={mkdtemp()}")
    options.add_argument(f"--disk-cache-dir={mkdtemp()}")
    options.add_argument("--remote-debugging-port=9222")

    chrome = webdriver.Chrome("/opt/chromedriver", options=options)

    quarter_offset = 0
    download_zip(chrome, quarter_offset)

    zip_file_name = get_zip_name()

    data_directory = unzip(zip_file_name)

    clean_dir(data_directory)
    

    print(os.listdir(data_directory))

    return 'worked'
