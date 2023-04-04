from selenium import webdriver
from msedge.selenium_tools import Edge, EdgeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import WebDriverException,  NoSuchElementException
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

# driver = webdriver.Edge(executable_path=executable_path)

driver.get('https://www.sgx.com/research-education/derivatives')
num_tries = 3
wait_time = 5
for i in range(num_tries):
    try:
        dropdown_input = driver.find_element_by_xpath("//article[@id='page-container']/template-base/div/div/section/div/sgx-widgets-wrapper/widget-research-and-reports-download/widget-reports-derivatives-tick-and-trade-cancellation/div/sgx-input-select/label/span[2]/span")
        # Click on the input element to open the dropdown menu
        dropdown_input.click()
        action = ActionChains(driver)
        action.send_keys(Keys.ARROW_DOWN).perform()
        # Wait for the dropdown dialog to be visible
        dialog = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "sgx-dialog#sgx-select-dialog")))

        # Click on the second option in the dropdown
        option = dialog.find_element_by_xpath("//sgx-select-picker-option/label/span")
        option.click()

        dropdown_input = driver.find_element_by_xpath("//article[@id='page-container']/template-base/div/div/section/div/sgx-widgets-wrapper/widget-research-and-reports-download/widget-reports-derivatives-tick-and-trade-cancellation/div/sgx-input-select[2]/label/span[2]/span")
        # Click on the input element to open the dropdown menu
        dropdown_input.click()
        action = ActionChains(driver)
        action.send_keys(Keys.ARROW_DOWN).perform()
        # Wait for the dropdown dialog to be visible
        dialog = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "sgx-dialog#sgx-select-dialog")))

        # Click on the second option in the dropdown
        option = dialog.find_element_by_xpath("//sgx-select-picker-option[2]/label/span")
        option.click()

        download_button = driver.find_element_by_css_selector('widget-reports-derivatives-tick-and-trade-cancellation .sgx-button--primary')

        download_button.click()
        break
    except NoSuchElementException:
        print(f"Error opening web page. Retrying in {wait_time} seconds...")
        time.sleep(wait_time)
time.sleep(10)
driver.delete_all_cookies()
driver.quit()
# if dropdown_input.is_displayed():
#     dropdown_input.send_keys(Keys.DOWN)
#     dropdown_input.send_keys(Keys.ENTER)
# else:
#     print('error')
    # handle the case when the element is not visible
# Send the down arrow key to highlight the first option in the dropdown

# Send the enter key to select the highlighted option
# Find all the option elements in the dropdown menu
# Get the text of the selected option
# options_loaded = EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".sgx-select-dropdown-menu .sgx-dropdown-option"))
# WebDriverWait(driver, 20).until(options_loaded)
# options = driver.find_elements_by_css_selector(".sgx-select-dropdown-menu .sgx-dropdown-option")
# print(options)
# # Loop through the option elements and get the name of each option
# for option in options:
#     option_name = option.get_attribute("innerText")
#     print(option_name)
# Find all the option elements in the dropdown menu
# options = driver.find_elements_by_css_selector(".sgx-select-picker-option--highlighted .sgx-icon--before")

# # Loop through the option elements and click on each one to make a selection
# for option in options:
#     print("Clicked option:", option.text)
#     print('------')



# wait for the download to complete
# download_button = driver.find_element_by_xpath('//button[text()="Download"]')