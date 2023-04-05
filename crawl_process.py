from selenium import webdriver
from msedge.selenium_tools import Edge, EdgeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import WebDriverException,  NoSuchElementException, StaleElementReferenceException, TimeoutException, ElementClickInterceptedException
from selenium.webdriver.remote.remote_connection import LOGGER
import glob
import os
import time
import argparse
import logging
import re


def choose_dropdown(driver:webdriver, num:int, type_data:str, is_select_file:bool, is_download:bool):
    if type_data == 'Time and Sales Historical Data':
        type_download = ''
        type_button = 'tick-and-trade-cancellation'
        if is_select_file:
            xpath_dropdown = f"//article[@id='page-container']/template-base/div/div/section/div/sgx-widgets-wrapper/widget-research-and-reports-download{type_download}/widget-reports-derivatives-tick-and-trade-cancellation/div/sgx-input-select/label/span[2]/span"
        else:
            xpath_dropdown = f"//article[@id='page-container']/template-base/div/div/section/div/sgx-widgets-wrapper/widget-research-and-reports-downloa{type_download}d/widget-reports-derivatives-tick-and-trade-cancellation/div/sgx-input-select[2]/label/span[2]/span"
    # find dropdown list 
    dropdown_input = driver.find_element_by_xpath(xpath_dropdown)
    # Click on the input element to open the dropdown menu
    dropdown_input.click()
    if num != 1:
        for i in range(1, num):
            action = ActionChains(driver)
            action.send_keys(Keys.ARROW_DOWN).perform()
            # Wait for the dropdown dialog to be visible
            dialog = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "sgx-dialog#sgx-select-dialog")))
        # Click on the second option in the dropdown
        time.sleep(5)
        option = dialog.find_element_by_xpath(f"//sgx-select-picker-option[{num}]/label/span")
        option.click()
        time.sleep(5)
    if is_download:
        download_button = driver.find_element_by_css_selector(f'widget-reports-derivatives-{type_button} .sgx-button--primary')
        download_button.click()
        time.sleep(10)

def crawl_process(driver:webdriver, num:int, days_ago:int):
    num_tries = 5
    wait_time = 5
    downloaded = False
    for j in range(num_tries):
        try:
            choose_dropdown(driver=driver, num=num, type_data=type_data, is_select_file=True, is_download=False)
            choose_dropdown(driver=driver, num=days_ago + 1, type_data=type_data, is_select_file=False, is_download=True)
            logging.info(f'Downloaded file {days_ago} day(s) ago')
            downloaded = True
            driver.quit()
            break
        except (NoSuchElementException,StaleElementReferenceException, ElementClickInterceptedException, TimeoutException):
            driver.refresh()
            logging.debug(f"Error opening web page. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
            downloaded = False
    return downloaded, days_ago



def create_dir(name_dir):
    os.makedirs(name_dir, exist_ok=True)

def setup_browser(name_file:str):
    wait_time = 5
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
    logging.debug(f"Wait in {wait_time} seconds...")
    time.sleep(wait_time)
    return driver



parser = argparse.ArgumentParser(description='Process to crawl data from https://www.sgx.com/research-education/derivatives')
subparsers = parser.add_subparsers(title='subcommands', dest='command')

# Mode automatic
autoparsers = subparsers.add_parser('auto', help='set auto crawl mode', description='This mode will download all data according to the time of each file')
autoparsers.add_argument('-t','--type_data', type=int,default=1, help="(type:int, default:1) Type of data users want to select. Choose type of data : (1 - Time and Sales Historical Data|)")
autoparsers.add_argument('-d','--days_ago', type=int,default=0, help="(type:int, default:0) Day users want to get. Choose day ago to download: (0 -> 4 day(s) ago )")
# Mode manual
manualparsers = subparsers.add_parser('manual', help='set manual crawl mode', description="Perform a download based on the user's selection")
manualparsers.add_argument('-t','--type_data', default=1, type=int, help="(type:int, default:1) Type of data users want to select. Choose type of data : (1 - Time and Sales Historical Data|)")
manualparsers.add_argument('-lf','--list_files', nargs='+', help="List of files  users want to download. Choose file to download: ('Time and Sales Historical Data':[1 - 'WEBPXTICK_DT', 2 - 'TickData_structure', 3 - 'TC', 4 - 'TC_structure'])")
manualparsers.add_argument('-d','--days_ago', type=int,default=0, help="(type:int, default:0) Day users want to get. Choose day ago to download: (0 -> 4 day(s) ago )")
args = parser.parse_args()

class IgnorePostFilter(logging.Filter):
    def filter(self, record):
        return "POST" not in record.getMessage()

# Set up the logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Add a console handler with the custom filter
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.addFilter(IgnorePostFilter())
console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)


# Add a file handler without the custom filter
file_handler_1 = logging.FileHandler('selenium.log')
file_handler_1.setLevel(logging.DEBUG)
file_formatter1 = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler_1.setFormatter(file_formatter1)
file_handler_1.addFilter(IgnorePostFilter())
logger.addHandler(file_handler_1)
# Add a file handler without the custom filter
file_handler_2 = logging.FileHandler('logging.log')
file_handler_2.setLevel(logging.DEBUG)
file_formatter2 = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler_2.setFormatter(file_formatter2)
file_handler_2.addFilter(IgnorePostFilter())
logger.addHandler(file_handler_2)

# Log some messages
logger.debug('Debug message')
logger.info('Info message')
logger.warning('Warning message')
logger.debug('POST request received')


list_file_target = [{'Time and Sales Historical Data':['WEBPXTICK_DT', 'TickData_structure', 'TC', 'TC_structure']}]

if args.command == 'auto':
    dir_data = list_file_target[args.type_data - 1]
    type_data = list(dir_data.keys())[0]
    list_file = dir_data[list(dir_data.keys())[0]]
    for i in range(len(list_file)):
        name_file = list_file[i]
        num = i + 1
        driver = setup_browser(name_file=name_file)
        downloaded, days_ago = crawl_process(driver=driver, num=num, days_ago=args.days_ago)
        if downloaded:
            logging.info(f'Downloaded file: {name_file}')
        else:
            logging.debug(f"Can't downloaded file: {name_file}|{str(num)}|{str(days_ago)}")
elif args.command == 'manual':
    dir_data = list_file_target[args.type_data - 1]
    type_data = list(dir_data.keys())[0]
    list_file = dir_data[list(dir_data.keys())[0]]
    for i in args.list_files:
        name_file = list_file[int(i) - 1]
        num = int(i)
        driver = setup_browser(name_file=name_file)
        downloaded, days_ago = crawl_process(driver=driver, num=num, days_ago=args.days_ago)
        if downloaded:
            logging.info(f'Downloaded file: {name_file}')
        else:
            logging.debug(f"Can't downloaded file: {name_file}|{str(num)}|{str(days_ago)}")
