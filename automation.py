import urllib.request
from selenium import webdriver
import webbrowser
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

chrome_prefs = {"download.default_directory": r"C:\Users\tengwei.goh\Documents\Github\L-QuBE-Data-Automation"} # (windows)

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.experimental_options["prefs"] = chrome_prefs

driver = webdriver.Chrome(options=options)
driver.get("http://192.168.253.20")

driver.implicitly_wait(10)
# button = driver.find_element('id',"elem_4")
# button.click()
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

# csv = driver.find_element('id', "csvlink1")
# arrow = driver.find_element('id','noPointsSection')
# test = arrow.find_element('id','csvColumn1')

# csv.click()


# trs = driver.find_elements(By.TAG_NAME, "tr") 

# tds = trs[4].find_elements(By.TAG_NAME, "td")
# for td in tds:
#     print(td.text)

# checkbox = driver.find_element('id', "checkbox2")
# checkbox.click()
# time.sleep(2)

driver.implicitly_wait(10)
files = driver.find_elements('xpath', "//*[@id[contains(.,'csvlink')]]")
print(len(files))

checkboxes = driver.find_elements('xpath', "//*[@id[contains(.,'checkbox')]]")
for i in range(len(checkboxes)):
    checkboxes[i].click()
    # time.sleep(0.5)
    files[i+1].click()
