from selenium import webdriver
from msedge.selenium_tools import Edge, EdgeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import WebDriverException,  NoSuchElementException, StaleElementReferenceException, TimeoutException, ElementClickInterceptedException
from selenium.webdriver.common.log import Logger
import glob
import os
import time
import argparse
from io import StringIO
import sys

# Redirect stderr to a file
buffer = StringIO()
sys.stderr = buffer


def choose_dropdown(driver, num, type_link):
    if type_link == 'type_of_data':
        xpath_dropdown = "//article[@id='page-container']/template-base/div/div/section/div/sgx-widgets-wrapper/widget-research-and-reports-download/widget-reports-derivatives-tick-and-trade-cancellation/div/sgx-input-select/label/span[2]/span"
    elif type_link == 'date':
        xpath_dropdown = "//article[@id='page-container']/template-base/div/div/section/div/sgx-widgets-wrapper/widget-research-and-reports-download/widget-reports-derivatives-tick-and-trade-cancellation/div/sgx-input-select[2]/label/span[2]/span"
    # find dropdown list 
    dropdown_input = driver.find_element_by_xpath(xpath_dropdown)
    # Click on the input element to open the dropdown menu
    dropdown_input.click()
    if num != 1:
        for i in range(1, num + 1):
            action = ActionChains(driver)
            action.send_keys(Keys.ARROW_DOWN).perform()
            # Wait for the dropdown dialog to be visible
            dialog = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "sgx-dialog#sgx-select-dialog")))
        # Click on the second option in the dropdown
        option = dialog.find_element_by_xpath(f"//sgx-select-picker-option[{num}]/label/span")
        option.click()

def downloading_file(driver):
    download_button = driver.find_element_by_css_selector('widget-reports-derivatives-tick-and-trade-cancellation .sgx-button--primary')
    download_button.click()

def create_dir(name_dir):
    os.makedirs(name_dir, exist_ok=True)

def setup_browser(name_file):
    # get download target
    local_dir = os.getcwd()
    download_dir = os.path.join(local_dir, name_file)
    create_dir(name_dir=download_dir)

    
    # get driver path
    # path = 'C:/Users/'
    # msedgedriver = 'msedgedriver.exe'
    # driver_path = glob.glob(f'{path}/**/{msedgedriver}', recursive=True)
    driver_path='C:/Users/tuank/Work/edgedriver_win64/msedgedriver.exe'


    # create EdgeOptions object and set download directory
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
    driver = Edge(executable_path=driver_path, options=options)
    driver.get('https://www.sgx.com/research-education/derivatives')
    return driver



parser = argparse.ArgumentParser(description='Process to crawl data from https://www.sgx.com/research-education/derivatives')
subparsers = parser.add_subparsers(title='subcommands', dest='command')

# Mode automatic
autoparsers = subparsers.add_parser('auto', help='set auto crawl mode', description='This mode will download all data according to the time of each file')

# Mode manual
manualparsers = subparsers.add_parser('manual', help='set manual crawl mode', description="Perform a download based on the user's selection")
manualparsers.add_argument('list_file', nargs='+', help="List of files  user's instruction want to download. Choose a file to download: (1 - WEBPXTICK_DT-*.zip| 2 - TickData_structure.dat| 3 - TC_*.txt| 4 - TC_structure.dat)")
manualparsers.add_argument('days_ago', type=int, help="(type:int) Day user's instructions want to get Choose day ago to download: (0 - today| 1 -> 4 day(s) ago )")
args = parser.parse_args()

if args.command == 'auto':
    for num in range(1, 5):
        print(f'num {num}')
        if num == 1:
            name_file = 'WEBPXTICK_DT'
        elif num == 2:
            name_file = 'TickData_structure'
        elif num == 3:
            name_file = 'TC'
        elif num == 4:
            name_file = 'TC_structure'
        driver = setup_browser(name_file=name_file)
        num_tries = 5
        wait_time = 5
        for i in range(num_tries):
            try:
                choose_dropdown(driver, num, 'type_of_data')
                for days in range(1, 6):
                    choose_dropdown(driver, days, 'date')
                    downloading_file(driver)
                    error_messages = [line.strip() for line in buffer.getvalue().splitlines() if 'ERROR' in line]

                    # Print the error messages
                    for message in error_messages:
                        print(f'----------{message}')
                    time.sleep(10)
                driver.delete_all_cookies()
                driver.quit()
                break
            except (WebDriverException, NoSuchElementException, StaleElementReferenceException, TimeoutException, ElementClickInterceptedException):
                driver.delete_all_cookies()
                driver.quit()
                driver = setup_browser(name_file=name_file)
                print(f"Error opening web page. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
    driver.delete_all_cookies()
    driver.quit()
elif args.command == 'manual':
    print(args.list_file)
