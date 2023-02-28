import json
class Configuration:
    def __init__(self, ip, month, day, hour, minute, second):
        self.ip = ip
        self.month = month
        self.day = day
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
        config = Configuration(user_config['ip'], user_config['month'], 
                               user_config['day'], user_config['hour'], 
                               user_config['minute'], user_config['second'])
        return config
    except Exception as e:
        print(e)
        return None

# config = get_config()
# print(config.ip) 
