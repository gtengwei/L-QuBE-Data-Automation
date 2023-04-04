from selenium_automation import *
from configuration import *
from collation import *
# python -m PyInstaller -F run_automation.py
# in cmd admin mode
# nssm.exe install Automation C:\Users\tengwei.goh\Documents\L-QuBE-Data-Automation\dist\run_automation.exe
# nssm.exe start Automation

config = get_config()
automate_time(config)