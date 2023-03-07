from collation import *
from automation import *
from configuration import *
from threading import Thread
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

def get_ip():
    ip = input('Enter the IP address of the Training Device: ')
    return ip

def main(config):
    print('')
    print('Welcome to the Trend Export Automation Software')
    print('Choose your option')
    print('1. Collate all data')
    print('2. Collate yesterday\'s data')
    print('3. Choose specific slots to collate')
    print('4. Exit')
    input_option = input()
    print(input_option)
    while True:
        match input_option:
            case '1':
                run_automation(config, 'all')
                main(config)
            case '2':
                run_automation(config, 'daily')
                main(config)
            case '3':
                run_automation(config, 'choose')
                main(config)
            case '4':
                print('Exiting...')
                # driver.close()
                exit()
                
            case _:
                print('Invalid option')
                main(config)

if __name__ == '__main__':
    # ip = get_ip()
    # driver = initialise_driver(ip)
    # main(ip)
    config = get_config()
    # print('IP address: ' + config.ip)

    main_thread = Thread(target=main, args=(config,))
    automate_time_thread = Thread(target=automate_time, args=(config,))

    main_thread.start()
    automate_time_thread.start()
    main_thread.join()
    automate_time_thread.join()