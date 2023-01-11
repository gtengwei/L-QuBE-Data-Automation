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

