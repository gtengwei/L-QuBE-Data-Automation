from collation import main_directory, create_new_directory, collate_dataframes, get_current_datetime
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService # Similar thing for firefox also!
from subprocess import CREATE_NO_WINDOW # This flag will only be available in windows
import os
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.executors.debug import DebugExecutor
import pytz

stop_thread = False

def initialise_driver(ip, device_num):
    try:
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
        
        # To prevent python terminal from opening
        chrome_service = ChromeService()
        chrome_service.creation_flags = CREATE_NO_WINDOW
        #initialise driver with curated options
        driver = webdriver.Chrome(service=chrome_service, options=options)
        # driver.get("http://192.168.253.20")
    except:
        current_date = get_current_datetime()
        os.chdir(main_directory)
        file = open('error_log.txt','a')
        file.write(f'{current_date} - Configuration Error: Chromedriver not installed properly. \n')
        file.close()
        return 'chromedriver error'
    
    # Initialise driver with ip given. If ip is invalid, this means that there is an issue with the IP address
    try:
        driver.get("http://" + ip)
        # run_to_trend_export_page(driver, password, device_num)
        return driver
    except:
        current_date = get_current_datetime()
        os.chdir(main_directory)
        file = open('error_log.txt','a')
        file.write(f'{current_date} - Configuration Error: {device_num}\'s IP address {ip} is not valid/incorrect. \n')
        file.close()
        driver.close()
        return None
        
def run_to_trend_export_page(driver, password, device_num):
    
    driver.implicitly_wait(10)
    # password_button = driver.find_element('id',"elem_4")
    # password_button.click()
    password_button = driver.find_element('xpath', "//span[text()='Password']")
    password_button.click()
    # print('clicked password button')

    driver.implicitly_wait(10)
    password_textbox = driver.find_element(By.CLASS_NAME, "gwt-PasswordTextBox")
    password_textbox.send_keys(password)

    driver.implicitly_wait(10)
    password_textbox.send_keys(u'\ue007')
    # print('entered and submitted password')
    # password_submit_button = driver.find_element(By.CLASS_NAME, "gwt-Button")

    time.sleep(2)
    # system = driver.find_element('id', "elem_63")

    # After submitting the password, 
    # if we are unable to find the system button, it means that the password is incorrect
    try:
        system = driver.find_element('xpath', "//span[text()='system']")
        system.click()
        # print('clicked system button')
    except:
        current_date = get_current_datetime()
        os.chdir(main_directory)
        file = open('error_log.txt','a')
        file.write(f'{current_date} - Configuration Error: {device_num}\'s password {password} is not valid/incorrect. \n')
        file.close()
        driver.close()

    time.sleep(1)
    # trend_export = driver.find_element('id', "elem_115")
    trend_export = driver.find_element('xpath', "//span[text()='Trend-Export']")
    trend_export.click()
    # print('clicked trend export button')

    driver.implicitly_wait(10)
    driver.switch_to.frame(1)
    # print('switched to frame')

def automate_time(config, window):
    # open('error_log.txt', 'w').close()
    SG = pytz.timezone('Asia/Singapore')
    scheduler = BackgroundScheduler()
    scheduler.start()
    # print('starting scheduler')
    window.write_event_value('-START_SCHEDULER-', None)
    cron_trigger = CronTrigger(
        year="*", month="*", day="*", 
        hour=config.hour, minute=config.minute, second="0", timezone=SG
    )

    scheduler.add_executor(DebugExecutor(), 'consecutive')
    scheduler.add_job(run_automation, args=[config,'daily', window], trigger=cron_trigger, id='daily', 
                      executor='consecutive', misfire_grace_time=1800, max_instances=1)
    scheduler.add_job(run_automation, args=[config,'daily_selected', window], trigger=cron_trigger, id='daily_selected', 
                      executor='consecutive', misfire_grace_time=1800, max_instances=1)

    while True:
        time.sleep(5)
        # print(stop_thread)
        if stop_thread:
            break
    
    scheduler.shutdown()

# Find and download all the csv files
def download_csv(driver, device, option, device_num, window):
    # Find all of the csv download buttons
    files = driver.find_elements('xpath', "//*[@id[contains(.,'csvlink')]]")

    # Find all the checkboxes to toggle appearance of csv files
    checkboxes = driver.find_elements('xpath', "//*[@id[contains(.,'checkbox')]]")

    # If the user wants to download all files' data for the whole duration
    if option == 'all':
        # Iterate through all the checkboxes and click them to download the csv files
        for i in range(len(checkboxes)):
            checkboxes[i].click()
            # time.sleep(0.5)
            files[i+1].click()
            # print('downloaded csv ' + str(i+1))
    
    # If the user wants to download all files' data for the past day
    elif option == 'daily':
        period_button = driver.find_element('id', "periodselection")
        period_button.click()
        # print('clicked period button')
        driver.implicitly_wait(10)
        date = driver.find_element('id', "gestern") # yesterday
        date.click()
        # print('chose yesterday')

        daily_csvlink = driver.find_element('id', "csvlink")
        daily_button = daily_csvlink.find_element('xpath', "//img[@alt='csvicon']")

        for i in range(len(checkboxes)):
            checkboxes[i].click()
            daily_button.click()
            # print('downloaded csv ' + str(i+1))

    # If the user wants to choose and download selected files' data for the specified duration
    elif option == 'choose':
        slots = find_all_slots(driver)
        window.write_event_value('CHOOSING SLOTS', None)
        # print('This is the list of slot names: ')
        for i in range(len(slots)):
            # print(str(i+1) + '. ' + slots[i])
            window['-SLOT' + str(i+1) + '-'].update(text = slots[i])
            window['-SLOT' + str(i+1) + '-'].update(visible = True)
        return driver, slots
        # choose_slot(driver, slots, window)
    
    # If the user wants to download all configured files' data for the past day
    elif option == 'daily_selected':
        period_button = driver.find_element('id', "periodselection")
        period_button.click()
        # print('clicked period button')
        driver.implicitly_wait(10)
        date = driver.find_element('id', "gestern") # yesterday
        date.click()
        # print('chose yesterday')

        for _, slot in device['slots'].items():
            try:
                slot_name = driver.find_element('xpath', "//*[.='" + slot + "']").get_attribute("id")
                # print(slot_name)
                time.sleep(0.5)
                slot_num = slot_name[7:]
                # print(slot_num)

                checkbox = driver.find_element('id', "checkbox" + slot_num)
                checkbox.click()

                # csv = driver.find_element('id', "csvlink" + slot_num)
                daily_csvlink = driver.find_element('id', "csvlink")
                daily_button = daily_csvlink.find_element('xpath', "//img[@alt='csvicon']")
                daily_button.click()
                # print('downloaded csv file')
            except:
                current_date = get_current_datetime()
                os.chdir(main_directory)
                file = open('error_log.txt','a')
                file.write(f'{current_date} - Configuration Error: {device_num}\'s slot: \'{slot}\' is not valid/spelled incorrectly. \n')
                file.close()
                driver.close()
    
    # If the user wants to download all files' data for today
    elif option == 'today':
        daily_csvlink = driver.find_element('id', "csvlink")
        daily_button = daily_csvlink.find_element('xpath', "//img[@alt='csvicon']")

        for i in range(len(checkboxes)):
            checkboxes[i].click()
            daily_button.click()
            # print('downloaded csv ' + str(i+1))

def find_all_slots(driver):
    slots = []
    slot_names = driver.find_elements('xpath', "//*[@id[contains(.,'slotbez')]]")
    for slot_name in slot_names:
        slots.append(slot_name.text)
    return slots

def choose_slot(driver, chosen_slots, window):
    for slot in chosen_slots:
        slot_name = driver.find_element('xpath', "//*[.='" + slot + "']").get_attribute("id")
        slot_num = slot_name[7:]

        checkbox = driver.find_element('id', "checkbox" + slot_num)
        checkbox.click()

        csv = driver.find_element('id', "csvlink" + slot_num)
        csv.click()
        # print('downloaded csv file')
    window.write_event_value('EXECUTION DONE', None)
        
def run_automation(config, option, window):
        if option != 'choose':
            for device_num, device in config.devices.items():
                for key, item in device.items():
                    if key == 'ip':
                        ip = item
                        if option == 'daily_selected':
                            if len(device['slots']) == 0:
                                # print('No slots selected')
                                continue
                        try:
                            directory = create_new_directory(ip, config.directory, option)
                            driver = initialise_driver(ip, device_num)
                            run_to_trend_export_page(driver, device['password'], device_num)
                            driver.implicitly_wait(10)

                            download_csv(driver, device, option, device_num, window)
                            collate_dataframes(option, directory)
                            driver.close()
                            if option != 'all':
                                window.write_event_value('DAILY COLLATION COMPLETE', None)
                        except:
                            pass
        else:
            device = config.devices[config.device_choice]
            ip = device['ip']
            directory = create_new_directory(ip, config.directory, option)
            driver = initialise_driver(ip, config.device_choice)
            if driver is not None:
                run_to_trend_export_page(driver, device['password'], config.device_choice)
                driver.implicitly_wait(10)
                driver, slots = download_csv(driver, device, option, config.device_choice, window)
                return driver, slots, directory
            else:
                current_date = get_current_datetime()
                os.chdir(main_directory)
                file = open('error_log.txt','a')
                file.write(f'{current_date} - Connection Error: Chromedriver is not properly installed. \n')
                file.close()
                return None, None, None