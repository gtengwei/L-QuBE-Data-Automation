from automation import *
from configuration import *
from collation import *
# python -m PyInstaller -F test.py
# in cmd admin mode
# nssm.exe install Automation C:\Users\tengwei.goh\Desktop\automation\dist\test.exe
# nssm.exe start Automation

config = get_config()
# print(config.ip[config.ip['ip_choice']])
for _, ip in config.ip.items():
    automate_time(config)