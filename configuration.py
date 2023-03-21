import json
# C:\\Users\\tengwei.goh\\Documents\\GitHub\\L-QuBE-Data-Automation
# C:\\Users\\tengwei.goh\\Desktop\\test
class Configuration:
    def __init__(self, ip_choice, ip, directory, slots, hour, minute, second):
        self.ip_choice = ip_choice
        self.ip = ip
        self.directory = directory
        self.slots = slots
        self.hour = hour
        self.minute = minute
        self.second = second

def get_json():
    """ read json content"""
    with open('config.json') as f:
        config = json.loads(f.read())
        return config

def get_config():
    try:
        json_config = get_json()
        user_config = json_config['config']
        config = Configuration(user_config['ip_choice'], user_config['ip'], user_config['directory'],
                               user_config['slots'], user_config['hour'], 
                               user_config['minute'], user_config['second'])
        return config
    except Exception as e:
        print(e)
        return None

config = get_config()
for key, items in config.ip.items():
    print(key, items)
print(config.ip[config.ip_choice])
# print(config.directory) 
