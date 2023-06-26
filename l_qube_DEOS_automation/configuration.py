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
        config = Configuration(json_config['directory'], json_config['device_choice'],
                               json_config['devices'],
                               json_config['hour'], json_config['minute'])
        return config
    except Exception as e:
        file = open('error_log.txt','a')
        file.write(f'JSON Formatting Error: {str(e)} \n')
        file.close()
        return None

