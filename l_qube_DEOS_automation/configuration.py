import json
# C:\\Users\\tengwei.goh\\Documents\\GitHub\\L-QuBE-Data-Automation
# C:\\Users\\tengwei.goh\\Desktop\\test
class Configuration:
    def __init__(self, directory, device_choice, devices, hour, minute):
        self.directory = directory
        self.device_choice = device_choice
        self.devices = devices
        self.hour = hour
        self.minute = minute
    
    def save(self):
        """ save configuration to json file"""
        with open('config.json', 'w') as f:
            json.dump(self.__dict__, f, indent=4)


def get_json():
    """ read json content"""
    with open('config.json') as f:
        config = json.loads(f.read())
        return config

def get_config():
    try:
        json_config = get_json()
        # user_config = json_config['config']
        config = Configuration(json_config['directory'], json_config['device_choice'],
                               json_config['devices'],
                               json_config['hour'], json_config['minute'])
        return config
    except Exception as e:
        file = open('error_log.txt','a')
        file.write(f'JSON Formatting Error: {str(e)} \n')
        file.close()
        return None

# config = get_config()
# print(config.devices)
# for _, device in config.devices.items():
#     print(len(device['slots']) == 0)

# print(config.devices['device_1']['slots']['1'])
# print(config.devices[config.device_choice]['ip'])
# print(config.devices[config.device_choice])
# device = config.devices[config.device_choice]

# ip = device['ip']
# print(ip)

# for _, slots in device['slots'].items():
#     print(slots)

# for _, device in config.devices.items():
#             for key, item in device.items():
#                 if key == 'ip':
#                      print(device['password'])

# for key, items in config.ip.items():
#     print(key, items)
# print(config.ip[config.ip_choice])

# for key, items in config.slots.items():
#     print(config.slots[key])
# print(config.slots['192.168.253.20'])

# for key, items in config.slots['192.168.253.20'].items():
#     print(items)
# print(config.slots['ip_1'])
