import urllib.request
from selenium import webdriver
import webbrowser
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)
driver.get("http://192.168.253.20")
time.sleep(5)
button = driver.find_element('id',"elem_4")
button.click()
time.sleep(1)

password = driver.find_element(By.CLASS_NAME, "gwt-PasswordTextBox")
password.send_keys("0007")
time.sleep(2)
password.send_keys(u'\ue007')
# password_submit_button = driver.find_element(By.CLASS_NAME, "gwt-Button")
# password_submit_button.click()
time.sleep(5)

system = driver.find_element('id', "elem_63")
system.click()
time.sleep(2)

trend_export = driver.find_element('id', "elem_115")
trend_export.click()
time.sleep(5)

driver.switch_to.frame(1)
print('switched to frame')
time.sleep(2)


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

files = driver.find_elements('xpath', "//*[@id[contains(.,'csvlink')]]")
print(len(files))

checkboxes = driver.find_elements('xpath', "//*[@id[contains(.,'checkbox')]]")
for i in range(len(checkboxes)):
    checkboxes[i].click()
    # time.sleep(0.5)
    files[i+1].click()
