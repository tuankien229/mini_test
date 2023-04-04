from selenium import webdriver
from msedge.selenium_tools import Edge, EdgeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import glob
import os
import time

# get download target
download_dir = os.getcwd()

# path = 'C:/Users/'
# msedgedriver = 'msedgedriver.exe'
# driver_path = glob.glob(f'{path}/**/{msedgedriver}', recursive=True)
# print(driver_path)

executable_path='C:/Users/tuank/Work/edgedriver_win64/msedgedriver.exe'
# create EdgeOptions object
# set download directory
options = EdgeOptions()
options.use_chromium = True
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_experimental_option("prefs",{
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})

# create Edge browser object
driver = Edge(executable_path=executable_path, options=options)
driver.get('https://www.sgx.com/research-education/derivatives')

download_button = driver.find_element_by_css_selector('widget-reports-derivatives-tick-and-trade-cancellation .sgx-button--primary')

download_button.click()