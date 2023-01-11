import urllib.request
from selenium import webdriver
import webbrowser
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
# urllib.request.urlretrieve("http://192.168.253.20", "mp3.mp3")
# print("Downloaded")

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
#driver.get("http://192.168.253.20/client/index.html")

