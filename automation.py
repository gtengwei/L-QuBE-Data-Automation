import urllib.request
from selenium import webdriver
import webbrowser
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz

from collation import *

def initialise_driver(ip):
    # Must wait for 'Run' LED light to start blinking before running the program
    directory = os.getcwd()
    chrome_prefs = {"download.default_directory": directory} # (windows)

    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.experimental_options["prefs"] = chrome_prefs

    # For headless version of software
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    

    # ip = input("Enter IP address: ")
    #initialise driver with curated options
    driver = webdriver.Chrome(options=options)
    # driver.get("http://192.168.253.20")
    while True:
        try:
            driver.get("http://" + ip)
            run_to_trend_export_page(driver)
            return driver
        except:
            print("Invalid IP address, try again")
            ip = input("Enter IP address: ")
            driver.get("http://" + ip)
            run_to_trend_export_page(driver)
            return driver
    


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

def automate_time(ip):
    SG = pytz.timezone('Asia/Singapore')
    scheduler = BackgroundScheduler()
    scheduler.start()
    print('starting scheduler')

    trigger = CronTrigger(
        year="*", month="*", day="*", 
        hour="8", minute="*", second="*", timezone=SG
    )
    scheduler.add_job(run_automation,args=[ip,'daily'], trigger=trigger)
    while True:
        time.sleep(5)

# Find and download all the csv files
def download_csv(driver, option):
    files = driver.find_elements('xpath', "//*[@id[contains(.,'csvlink')]]")
    print(len(files))

    # Find all the checkboxes to toggle appearance of csv files
    checkboxes = driver.find_elements('xpath', "//*[@id[contains(.,'checkbox')]]")

    if option == 'all':
        # Iterate through all the checkboxes and click them to download the csv files
        for i in range(len(checkboxes)):
            checkboxes[i].click()
            # time.sleep(0.5)
            files[i+1].click()
            print('downloaded csv ' + str(i+1))
    
    elif option == 'daily':
        period_button = driver.find_element('id', "periodselection")
        period_button.click()
        print('clicked period button')
        driver.implicitly_wait(10)
        date = driver.find_element('id', "gestern") # yesterday
        date.click()
        print('chose yesterday')

        daily_csvlink = driver.find_element('id', "csvlink")
        daily_button = daily_csvlink.find_element('xpath', "//img[@alt='csvicon']")

        for i in range(len(checkboxes)):
            checkboxes[i].click()
            daily_button.click()
            print('downloaded csv ' + str(i+1))

def choose_slot(driver, slots):
    # part 1: no slot number
    # print('This is the list of slot names: ')
    # for slot in slots:
    #     print(slot)
    # while True:
    #     name = input("Enter slot name(press 'Q' to exit): ")
    #     if name == 'Q' or name == 'q':
    #         driver.close()
    #         break
    #     elif name in slots:
    #         slot_name = driver.find_element('xpath', "//*[.='" + name + "']").get_attribute("id")
    #         print(slot_name)
    #         time.sleep(1)
    #         slot_num = slot_name[7:]
    #         print(slot_num)

    #         checkbox = driver.find_element('id', "checkbox" + slot_num)
    #         checkbox.click()

    #         csv = driver.find_element('id', "csvlink" + slot_num)
    #         csv.click()
    #         print('downloaded csv file')
    #         time.sleep(1)
    #     else:
    #         print('Slot name not found. Please try again.')

    # part 2: add slot number to choose
    print('This is the list of slot names: ')
    for i in range(len(slots)):
        print(str(i+1) + '. ' + slots[i])
    while True:
        try:
            name = input("Enter slot number(press 'Q' to exit): ")
            if name == 'Q' or name == 'q':
                break
            elif slots[int(name)-1] in slots:
                slot_name = driver.find_element('xpath', "//*[.='" + slots[int(name)-1] + "']").get_attribute("id")
                print(slot_name)
                time.sleep(1)
                slot_num = slot_name[7:]
                print(slot_num)

                checkbox = driver.find_element('id', "checkbox" + slot_num)
                checkbox.click()

                csv = driver.find_element('id', "csvlink" + slot_num)
                csv.click()
                print('downloaded csv file')
                time.sleep(1)
        except:
            print('Slot number not found. Please try again.')
    # while True:
    #     try:
    #         name = input("Enter slot name(press 'Q' to exit): ")
    #         # TRF-01 GENERAL ALARM
    #         # FCU-B1-CORRIDOR-1 RA TEMP
    #         if name == 'Q' or name == 'q':
    #             break
    #         slot_name = driver.find_element('xpath', "//*[.='" + name + "']").get_attribute("id")
    #         print(slot_name)
    #         time.sleep(1)
    #         slot_num = slot_name[-1]
    #         print(slot_num)

    #         checkbox = driver.find_element('id', "checkbox" + slot_num)
    #         checkbox.click()
    #         # time.sleep(1)
    #         csv = driver.find_element('id', "csvlink" + slot_num)
    #         csv.click()
    #         print('downloaded csv')
    #     except:
    #         print("Invalid slot name, try again")

def find_all_slots(driver):
    slots = []
    slot_names = driver.find_elements('xpath', "//*[@id[contains(.,'slotbez')]]")
    print(len(slot_names))
    for slot_name in slot_names:
        # print(slot_name.text)
        slots.append(slot_name.text)
    return slots

def run_automation(ip, option):
    create_new_directory()
    driver = initialise_driver(ip)
    # run_to_trend_export_page(driver)
    driver.implicitly_wait(10)

    download_csv(driver, option)
    collate_dataframes()
    driver.close()

# driver = initialise_driver()
# run_to_trend_export_page(driver)
# choose_slot(driver)
# collate_dataframes()
# driver.close()
