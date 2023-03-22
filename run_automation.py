from automation import *
from configuration import *
from collation import *
# python -m PyInstaller -F run_automation.py
# in cmd admin mode
# nssm.exe install Automation C:\Users\tengwei.goh\Desktop\automation\dist\run_automation.exe
# nssm.exe start Automation

config = get_config()
# print(config.ip[config.ip['ip_choice']])
automate_time(config)