from collation import *
from automation import *
import tzlocal
from threading import Thread
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

def get_ip():
    ip = input('Enter the IP address of the Training Device: ')
    return ip

def main(driver):
    print('')
    print('Welcome to the Trend Export Automation Software')
    print('Choose your option')
    print('1. Collate all data')
    print('2. Choose specific slots to collate')
    print('3. Exit')
    input_option = input()
    print(input_option)
    while True:
        match input_option:
            case '1':
                run_automation(driver)
                main(driver)
            case '2':
                run_to_trend_export_page(driver)
                choose_slot(driver)
                # TRF-01 GENERAL ALARM
                # FCU-B1-CORRIDOR-1 RA TEMP
                collate_dataframes()
                main(driver)
            case '3':
                print('Exiting...')
                driver.close()
                exit()
                
            case _:
                print('Invalid option')
                main(driver)

if __name__ == '__main__':
    ip = get_ip()
    driver = initialise_driver(ip)
    main(driver)