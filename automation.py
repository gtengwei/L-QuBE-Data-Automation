import urllib.request
from selenium import webdriver
import webbrowser
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
from collation import *

def initialise_driver():
    # Must wait for 'Run' LED light to start blinking before running the program
    directory = os.getcwd()
    chrome_prefs = {"download.default_directory": directory} # (windows)

    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.experimental_options["prefs"] = chrome_prefs

    # For headless version of software
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    

    # ip = input("Enter IP address: ")
    #initialise driver with curated options
    driver = webdriver.Chrome(options=options)
    # driver.get("http://192.168.253.20")
    while True:
        try:
            ip = input("Enter IP address: ")
            driver.get("http://" + ip)
            return driver
        except:
            print("Invalid IP address, try again")
    


def run_to_trend_export_page(driver):
    
    driver.implicitly_wait(10)
    # password_button = driver.find_element('id',"elem_4")
    # password_button.click()
    password_button = driver.find_element('xpath', "//span[text()='Password']")
    password_button.click()
    print('clicked password button')

    driver.implicitly_wait(10)
    password = driver.find_element(By.CLASS_NAME, "gwt-PasswordTextBox")
    password.send_keys("0007")

    driver.implicitly_wait(10)
    password.send_keys(u'\ue007')
    print('entered and submitted password')
    # password_submit_button = driver.find_element(By.CLASS_NAME, "gwt-Button")
    # password_submit_button.click()
    #driver.get("http://192.168.253.20/client/index.html")

    time.sleep(2)
    # system = driver.find_element('id', "elem_63")
    # system.click()
    system = driver.find_element('xpath', "//span[text()='system']")
    system.click()
    print('clicked system button')

    time.sleep(1)
    # trend_export = driver.find_element('id', "elem_115")
    # trend_export.click()
    trend_export = driver.find_element('xpath', "//span[text()='Trend-Export']")
    trend_export.click()
    print('clicked trend export button')

    driver.implicitly_wait(10)
    driver.switch_to.frame(1)
    print('switched to frame')

# checkbox = driver.find_element('id', "checkbox2")
# checkbox.click()
# time.sleep(2)

# Find and download all the csv files
def download_csv(driver):
    files = driver.find_elements('xpath', "//*[@id[contains(.,'csvlink')]]")
    print(len(files))

    # Find all the checkboxes to toggle appearance of csv files
    checkboxes = driver.find_elements('xpath', "//*[@id[contains(.,'checkbox')]]")

    # Iterate through all the checkboxes and click them to download the csv files
    for i in range(len(checkboxes)):
        checkboxes[i].click()
        # time.sleep(0.5)
        files[i+1].click()
        print('downloaded csv ' + str(i+1))

def choose_slot(driver):
    name = input("Enter slot name: ")
    # TRF-01 GENERAL ALARM
    slot_name = driver.find_element('xpath', "//*[.='" + name + "']").get_attribute("id")
    print(slot_name)
    time.sleep(1)
    slot_num = slot_name[-1]
    print(slot_num)

    checkbox = driver.find_element('id', "checkbox" + slot_num)
    checkbox.click()
    # time.sleep(1)
    csv = driver.find_element('id', "csvlink" + slot_num)
    csv.click()
    print('downloaded csv')

driver = initialise_driver()
run_to_trend_export_page(driver)
choose_slot(driver)
# collate_dataframes()
driver.close()
