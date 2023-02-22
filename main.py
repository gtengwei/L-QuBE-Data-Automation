from collation import *
from automation import *
from threading import Thread
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

def get_ip():
    ip = input('Enter the IP address of the Training Device: ')
    return ip

def main(ip):
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
                run_automation(ip, 'all')
                main(ip)
            case '2':
                run_automation(ip, 'daily')
                main(ip)
            case '3':
                # run_to_trend_export_page(driver)
                slots = find_all_slots(ip)
                choose_slot(ip, slots)
                # TRF-01 GENERAL ALARM
                # FCU-B1-CORRIDOR-1 RA TEMP
                collate_dataframes()
                main(ip)
            case '4':
                print('Exiting...')
                # driver.close()
                exit()
                
            case _:
                print('Invalid option')
                main(ip)

if __name__ == '__main__':
    ip = get_ip()
    # driver = initialise_driver(ip)
    # main(ip)
    main_thread = Thread(target=main, args=(ip,))
    automate_time_thread = Thread(target=automate_time, args=(ip,))

    main_thread.start()
    automate_time_thread.start()
    main_thread.join()
    automate_time_thread.join()