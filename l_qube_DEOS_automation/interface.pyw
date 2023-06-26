from ui_selenium_automation import run_automation, choose_slot, collate_dataframes, automate_time, initialise_driver, find_all_slots
import ui_selenium_automation
from configuration import get_config
from collation import get_current_datetime, main_directory
import PySimpleGUI as sg
from psgtray import SystemTray
import threading
import datetime as dt
import time
import os
from collections import defaultdict
# Add a touch of color
sg.theme('DarkBlue3')  

# Change font and font size
sg.set_options(font=('Helvetica', 10))
sg.set_options(tooltip_font=('Helvetica', 10))

# Default size for frames, can be changed
WIDTH = 420
HEIGHT = 360

MULTILINE_WIDTH = 550
config = get_config()

# Blank frame for testing purposes
def blank_frame():
    return sg.Frame("", [[]], pad=(5, 3), expand_x=True, expand_y=True, background_color='#404040', border_width=0)

# Move window to the center of the screen
def move_center(window):
    print(window.current_location())
    screen_width, screen_height = window.get_screen_dimensions()
    win_width, win_height = window.size
    x, y = (screen_width - win_width)//2, (screen_height - win_height)//2
    window.move(x, y)

# Update tooltip text
def update(element, text):
    element.TooltipObject.text = text

def block_focus(window):
    for key in window.key_dict:    # Remove dash box of all Buttons
        element = window[key]
        if isinstance(element, sg.Button):
            element.block_focus()

def popup_add_device():
    class Device:
        def __init__(self, num, ip, password, slots):
            self.num = num
            self.ip = ip
            self.password = password
            self.slots = slots
    device = Device('', '', '', '')
    driver = None
    slots_frame = [[sg.Text('Choose the slots to collate')]]
    for i in range(1, 251):
        if i % 4 == 1:
            slots_frame += [
                [sg.Checkbox('Slot {}'.format(i), key='-SLOT{}-'.format(i), enable_events=True, visible=False),
                sg.Checkbox('Slot {}'.format(i+1), key='-SLOT{}-'.format(i+1), enable_events=True, visible=False),
                sg.Checkbox('Slot {}'.format(i+2), key='-SLOT{}-'.format(i+2), enable_events=True, visible=False),
                sg.Checkbox('Slot {}'.format(i+3), key='-SLOT{}-'.format(i+3), enable_events=True, visible=False),]

            ]

    slots_column_frame = [
        [sg.Column(slots_frame, size=(WIDTH, HEIGHT), scrollable=True,expand_x=True, expand_y=True, key='-SLOTS_COL_FRAME-')],
        [sg.Button('Select Slots', key='-SLOTS CHOSEN-', tooltip='Click to select slots to collate')]
    ]

    select_slots_button = [
        [sg.Button('Select Slots', key='-SLOTS_CHOSEN-', tooltip='Click to select slots to collate')]
    ]

    col_layout = [[sg.Button('Add', bind_return_key=True), sg.Button('Cancel')]]
    device_info_frame = [
        [sg.Text('Enter Device IP')],
        [sg.InputText(key='-IP-', tooltip='Device IP', enable_events=True, expand_x=True)],
        [sg.Text('Enter Device Password')],
        [sg.InputText(key='-PASSWORD-', tooltip='Device Password', enable_events=True, expand_x=True)],
        [sg.Text('Enter Device Slots'), sg.Button('Find All Slots', key='-FIND_All_SLOTS-', tooltip='Find all slots on device')],
        [sg.Multiline(key='-SLOTS-', size=(43, 10), tooltip='Enter every new slot on new line', enable_events=True, expand_x=True, expand_y=True)],
        [sg.Column(col_layout, expand_x=True, element_justification='left')],
    ]
    layout = [
        
        [sg.Frame('Enter Device Information', device_info_frame, size=(WIDTH,HEIGHT), expand_x=True, expand_y=True, visible=True, key='-DEVICE_INFO_FRAME-'),
        sg.Frame('Choose your slots', slots_column_frame, size=(WIDTH,HEIGHT), expand_x=True, expand_y=True, visible=False, key='-SLOTS_COL-'),],
        [sg.Frame('', select_slots_button, size=(WIDTH, 60),  expand_x=True, element_justification='right', visible=False, key='-SELECT_SLOTS_BTN-')]
    ]
    window = sg.Window("Add Device", layout, use_default_focus=False, finalize=True, modal=True, resizable=True)
    block_focus(window)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':
            window.close()
            return None
        
        if event == 'Add':
            if values['-IP-'] == '' or values['-PASSWORD-'] == '':
                sg.popup('Please fill in both IP and Password field', keep_on_top=True)
                continue
            exist = False
            for device_num, device_info in config.devices.items():
                if device_info['ip'] == values['-IP-']:
                    sg.popup('IP already exists', keep_on_top=True)
                    exist = True
                    break
            if not exist:
                window.close()
                device.ip = values['-IP-']
                device.password = values['-PASSWORD-']
                device.slots = values['-SLOTS-']
                if driver:
                    driver.close()
                return device
            
        if event == '-FIND_All_SLOTS-':
            sg.popup_quick_message('Finding all slots on device. Please wait...', keep_on_top=True, background_color='grey')
            try:
                device_num = f'device_{len(config.devices) + 1}'
                print(values['-IP-'], values['-PASSWORD-'], device_num)
                driver = initialise_driver(values['-IP-'], values['-PASSWORD-'], device_num)
                driver.implicitly_wait(10)
                slots = find_all_slots(driver)
                window['-SLOTS_COL-'].update(visible=True)
                window['-SELECT_SLOTS_BTN-'].update(visible=True)
                window['-FIND_All_SLOTS-'].update(visible=False)
                print('This is the list of slot names: ')
                for i in range(len(slots)):
                    print(str(i+1) + '. ' + slots[i])
                    window['-SLOT' + str(i+1) + '-'].update(text = slots[i])
                    window['-SLOT' + str(i+1) + '-'].update(visible = True)
            except:
                sg.popup_error('Unable to find all slots on device. Please check if the device information is correct and try again.')
                window['-SLOTS_COL-'].update(visible=False)
                window['-SELECT_SLOTS_BTN-'].update(visible=False)
                window['-FIND_All_SLOTS-'].update(visible=True)

        if event == '-SLOTS_CHOSEN-':
            chosen_slots = []
            for i in range(len(slots)):
                if window[f'-SLOT{i+1}-'].get() == True:
                    chosen_slots.append(slots[i])
            window['-SLOTS-'].update(value = '\n'.join(chosen_slots))
            
        
def popup_remove_device(config):
    col_layout = [[sg.Button('Remove', bind_return_key=True), sg.Button('Cancel')]]
    layout = [
        [sg.Text('Select Device to Remove')],
        [sg.InputCombo(list(config.devices.keys()), size=(24, len(config.devices.keys())), key='-DEVICE-', tooltip='Device Name', enable_events=True)],
        [sg.Column(col_layout, expand_x=True, element_justification='right')],
    ]
    window = sg.Window("Remove Device", layout, use_default_focus=False, finalize=True, modal=True)
    block_focus(window)

    device_num_dict = defaultdict()
    for device_num, device in config.devices.items():
        device_num_dict[device_num] = f"{device_num} ({device['ip']})"
    window['-DEVICE-'].update(value=next(iter(device_num_dict.values())), values=list(device_num_dict.values()))

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':
            window.close()
            return None
        if event == 'Remove':
            window.close()
            return values['-DEVICE-']

def check_device_info(config):
    accurate_devices_info = True
    for device_num, device in config.devices.items():
        for key, item in device.items():
            sg.popup_quick_message('Checking device info...', keep_on_top=True, background_color='grey')
            if key == 'ip':
                ip = item
                try:
                    driver = initialise_driver(ip, device['password'], device_num)
                    driver.implicitly_wait(10)
                    all_slots = find_all_slots(driver)
                    print(all_slots)
                    driver.close()
                except:
                    sg.popup_error(f"Unable to connect to {device_num} ({ip}). Please check your device IP.")
                    accurate_devices_info = False
                    break
            if key == 'slots':
                for _, slot_name in item.items():
                    if slot_name in all_slots:
                        pass
                    else:
                        sg.popup_error(f"Slot {slot_name} does not exist on {device_num}. Please check your device's slot names.")
                        accurate_devices_info = False
                        current_date = get_current_datetime()
                        os.chdir(main_directory)
                        file = open('error_log.txt','a')
                        file.write(f'{current_date} - Configuration Error: {device_num}\'s slot: \'{slot_name}\' is not valid/spelled incorrectly. \n')
                        file.close()
    if accurate_devices_info:
        sg.popup_ok('All device information is correct! You may proceed to start the daily scheduler.')  
    else:
        sg.popup_error('Please check your device(s) information and try again.')                
    
                
def update_device_display(window, config):
    device_num_dict = defaultdict()
    for device_num, device in config.devices.items():
        device_num_dict[device_num] = f"{device_num} ({device['ip']})"
    first_device = next(iter(device_num_dict))
    window['-DEVICE-'].update(value=next(iter(device_num_dict.values())), values=list(device_num_dict.values()))
    window['-DEVICE_CHOICE-'].update(value=f"{config.device_choice} ({config.devices[config.device_choice]['ip']})", values=list(device_num_dict.values()))
    window['-IP-'].update(value=config.devices[first_device]['ip'])
    window['-PASSWORD-'].update(value=config.devices[first_device]['password'])
    window['-SLOTS-'].update(value='')
    for slot_num, slot in config.devices[first_device]['slots'].items(): 
        window['-SLOTS-'].update(f'{slot}\n', append=True)

# Build the GUI
def build():
    # Frame to choose dates
    date_frame = [
        [sg.InputText('', size=(20, 1), key='-START_DATE-', disabled=True, tooltip='Start Date', enable_events=True),
         sg.CalendarButton('Choose Start Date', target='-START_DATE-', key='-CALENDAR-', tooltip='Click to choose date', size=(20, 1), format='%m-%d-%Y %H:%M:%S', )],
        [sg.InputText('', size=(20, 1), key='-END_DATE-', disabled=True, tooltip='End Date', enable_events=True),
         sg.CalendarButton('Choose End Date', target='-END_DATE-', key='-CALENDAR-', tooltip='Click to choose date', size=(20, 1), format='%m-%d-%Y %H:%M:%S')],
        [sg.InputCombo('default', size=(24, 5), key='-DEVICE_CHOICE-', tooltip='Choose which device to choose slots from', enable_events=True)],
        [sg.Button('Select Dates', key='-DATES_CHOSEN-', tooltip='Click to select dates to collate')],

    ]
    device_input_combo = [
        sg.InputCombo(('default'), size=(24, 5), default_value=next(iter(config.devices)), key='-DEVICE-', tooltip='Device Name', enable_events=True),
        sg.Button('Test IP', key='-TEST_IP-', tooltip='Click to test IP address'),
    ]
    
    device_parameters =[
        [sg.Text(size=(12,1)), sg.Text('IP', size=(8, 1), key='-IP_text-'), sg.InputText('default ip', key='-IP-', tooltip='IP Address of device', enable_events=True, size=(30, 1), expand_x=True)],
        [sg.Text(size=(12,1)), sg.Text('Password', size=(8, 1), key='-PASSWORD_text-'), sg.InputText('default password', key='-PASSWORD-', tooltip='Password of device', enable_events=True, size=(30, 1), expand_x=True)],
        [sg.Text(size=(12,1)), sg.Text('Slots', size=(8, 1), key='-SLOTS_text-'), sg.Multiline(key='-SLOTS-', tooltip='Slots to collate data from', enable_events=True, size=(30, 8), expand_x=True, expand_y=True)],
    ]

    config_frame = []
    config_frame += [
        [sg.Text('Directory', size=(12, 1)), sg.InputText(config.directory, key='-DIRECTORY-', tooltip='Directory to save files', enable_events=True, size=(30, 1), expand_x=True), sg.FolderBrowse('Browse', key='-BROWSE-', tooltip='Click to browse for directory')],
    ]
    config_frame += [
        [sg.Text('Folder Name', size=(12, 1)), sg.Text(os.path.basename(os.path.normpath(config.directory)), key='-FOLDER_NAME-', tooltip='Name of folder to save files', enable_events=True, size=(30, 1))],
    ]
    
    config_frame += [
        [sg.Text('Time to collate', size=(12, 1)), 
         sg.InputText((config.hour), key='-HOUR-', tooltip='Choose hour to collate data from', enable_events=True, size=(3, 1)),
         sg.Text(':'),
         sg.InputText((config.minute), key='-MINUTE-', tooltip='Choose minute to collate data from', enable_events=True, size=(3, 1))],
    ]

    config_frame += [
        [sg.Text('Devices', size=(12, 1))] + device_input_combo,
    ]
    config_frame += device_parameters
    config_frame += [
        [sg.Button('Save Configuration', key='-SAVE_CONFIG-', tooltip='Click to save configuration'),
         sg.Button('Add Device', key='-ADD_DEVICE-', tooltip='Click to add device'),
         sg.Button('Remove Device', key='-REMOVE_DEVICE-', tooltip='Click to remove device')],
    ]
    
    error_log_multiline= [
        [sg.Multiline(key='-ERROR_LOG-', tooltip='Error log', enable_events=True, size=(30, 8), autoscroll=True, expand_x=True, expand_y=True)],
        [sg.Button('Clear Error Log', key='-CLEAR_ERROR_LOG-', tooltip='Click to clear error log')]
    ]

    # Initial frame to choose option
    option_frame = [
        [sg.Text('Option'), 
         sg.InputCombo(('Edit Configuration',
                        'Automate Collation (Repeated)',
                        'Download all data (Non-repeated)', 
                        'Choose specific slots to download (Non-repeated)',), default_value='Edit Configuration', enable_events=True, size=(None, 4), key='-OPTION-', expand_x=True),
                        sg.Button('Check Device Info', key='-CHECK_DEVICE_INFO-', tooltip='Click to check device info', visible=False)],
        [sg.Button('Start Collation', key='-COLLATE_FILES-', tooltip='Click to collate files in the chosen folder', visible=False), 
         sg.Button('Stop Collation', key='-STOP_SCHEDULER-', tooltip='Click to stop scheduler', visible=False, disabled=True)],
        [sg.Text('Status: ', size=(5, 1), key='-STATUS_text-', visible=False), sg.Text('Scheduler not started', size=(20, 1), key='-STATUS-', text_color='firebrick3', visible=False)],
        [sg.pin(sg.Column(error_log_multiline, key='-ERROR_FRAME-', visible=False, pad=(0,0), expand_x=True, expand_y=True), expand_x=True, expand_y=True)],
        [sg.Frame('Choose Time Period', date_frame, size=(WIDTH,HEIGHT), visible=False, key='-DATES_FRAME-', expand_x=True, expand_y=True)],
    ]

    slots_frame = [[sg.Text('Choose the slots to collate')]]
    for i in range(1, 251):
        if i % 4 == 1:
            slots_frame += [
                [sg.Checkbox('Slot {}'.format(i), key='-SLOT{}-'.format(i), enable_events=True, visible=False),
                sg.Checkbox('Slot {}'.format(i+1), key='-SLOT{}-'.format(i+1), enable_events=True, visible=False),
                sg.Checkbox('Slot {}'.format(i+2), key='-SLOT{}-'.format(i+2), enable_events=True, visible=False),
                sg.Checkbox('Slot {}'.format(i+3), key='-SLOT{}-'.format(i+3), enable_events=True, visible=False),]

            ]

    slots_column_frame = [
        [sg.Column(slots_frame, size=(WIDTH, HEIGHT), scrollable=True,expand_x=True, expand_y=True, key='-SLOTS_COL_FRAME-')],
        [sg.Button('Select Slots', key='-SLOTS CHOSEN-', tooltip='Click to select slots to collate')]
    ]

    select_slots_button = [
        [sg.Button('Select Slots', key='-SLOTS_CHOSEN-', tooltip='Click to select slots to collate')]
    ]
    back_button = [
        [sg.Button('Back', key='-BACK-')]
    ]

    progress_bar = [
        [sg.Text('', key='-PROGRESS_TEXT-', justification='center', size=(20, 1), expand_x=True)],
         [sg.ProgressBar(100, orientation='h', size=(40, 20), key='-PROGRESS_BAR-')]    
        ]
    
    # Layout to combine all frames
    layout = [
    [
        sg.Frame('Progress Bar', progress_bar, size=(WIDTH,100), visible=False, key='-PROGRESS_COL-'),
        [sg.Frame('Choose your option', option_frame, size=(WIDTH,HEIGHT), visible=True, key='-OPTION_COL-'),
        sg.Frame('Choose your slots', slots_column_frame, size=(WIDTH,HEIGHT), expand_x=True, expand_y=True, visible=False, key='-SLOTS_COL-'),
        sg.Frame('Edit Configuration', config_frame, size=(WIDTH+59,HEIGHT), visible=True, expand_x=True, expand_y=True, key='-CONFIG_COL-'),],
        [sg.Frame('', select_slots_button, size=(WIDTH, 60),  expand_x=True, element_justification='right', visible=False, key='-SELECT_SLOTS_BTN-')]
    
     ]
    ]

    margins = (5, 5)
    return sg.Window('L-QuBE DEOS Automation', layout, margins = margins, finalize=True, resizable=True, enable_close_attempted_event=True)

# Main function to run the GUI
def interface():
    # Create the window
    window = build()
    menu = ['', ['Show Window', 'Hide Window', '---', 'Scheduler',['Start Scheduler','Stop Scheduler'], 'Exit']]
    tooltip = 'Double click to show interface'
    tray = SystemTray(menu, single_click_events=False, window=window, tooltip=tooltip, icon=sg.DEFAULT_BASE64_ICON)
    tray.show_message('DEOS Interface', 'DEOS Interface launched!')

    window['-OPTION_COL-'].expand(True, True)
    start_scheduler = False

    window['-START_DATE-'].update(value=dt.datetime.now().strftime('%m-%d-%Y' + ' 00:00:00'))
    window['-END_DATE-'].update(value=dt.datetime.now().strftime('%m-%d-%Y %H:%M:%S'))

    config = get_config()
    update_device_display(window, config)

    file = open('error_log.txt','r')
    window['-ERROR_LOG-'].update(value=file.read())   
    file.close()

    # Display window
    while True:
        event, values = window.read()
        # End program if user closes window or clicks cancel
        if event == tray.key:
            event = values[event]       # use the System Tray's event as if was from the window

        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        
        print(event)
        tray.show_message(title=event)

        # When user stops scheduler via tray menu
        if event == 'Stop Scheduler':
            if start_scheduler == True:
                start_scheduler = False
                ui_selenium_automation.stop_thread = True
                automate_thread.join()
                window['-COLLATE_FILES-'].update(disabled=False)
                window['-STOP_SCHEDULER-'].update(disabled=True)
                window['-STATUS-'].update(value='Scheduler stopped', text_color='firebrick3')
                tray.change_icon(sg.DEFAULT_BASE64_ICON)
                tray.show_message('Scheduler', 'Scheduler has been stopped')
            else:
                sg.popup('Scheduler has not been started yet!')

        # When user starts scheduler via tray menu
        elif event == 'Start Scheduler':
            if start_scheduler == False:
                start_scheduler = True
                ui_selenium_automation.stop_thread = False
                window['-COLLATE_FILES-'].update(disabled=True)
                window['-STOP_SCHEDULER-'].update(disabled=False)
                window['-STATUS-'].update(value='Scheduler started', text_color='lightgreen')
                tray.change_icon(sg.EMOJI_BASE64_HAPPY_JOY)
                tray.show_message('Scheduler', 'Scheduler has been started')

                automate_thread = threading.Thread(target= automate_time, args=(config, window, ))
                automate_thread.start()
                
            else:
                sg.popup('Scheduler has already been started!')

        # Show window when tray icon is double clicked
        if event in ('Show Window', sg.EVENT_SYSTEM_TRAY_ICON_DOUBLE_CLICKED):
            window.un_hide()
            window.bring_to_front()
        
        # Hide window when user clicks on close button
        elif event in ('Hide Window', sg.WIN_CLOSE_ATTEMPTED_EVENT):
            window.hide()
            tray.show_icon()        # if hiding window, better make sure the icon is visible
            tray.show_message('Minimising to tray (Application not closed)', 'Running in the background...')

        # Edit configuration
        if values['-OPTION-'] == 'Edit Configuration':
            window['-DATES_FRAME-'].update(visible=False)
            window['-COLLATE_FILES-' ].update(visible=False)
            window['-CONFIG_COL-' ].update(visible=True)
            window['-STOP_SCHEDULER-' ].update(visible=False)
            window['-STATUS_text-'].update(visible=False)
            window['-STATUS-'].update(visible=False)
            window['-CHECK_DEVICE_INFO-'].update(visible=False)
            window['-ERROR_FRAME-'].update(visible=False)

        # Run daily automation
        if values['-OPTION-'] == 'Automate Collation (Repeated)':
            window['-DATES_FRAME-'].update(visible=False)
            window['-CONFIG_COL-' ].update(visible=False)
            window['-COLLATE_FILES-' ].update(visible=True)
            window['-STOP_SCHEDULER-' ].update(visible=True)
            window['-STATUS_text-'].update(visible=True)
            window['-STATUS-'].update(visible=True)
            window['-CHECK_DEVICE_INFO-'].update(visible=True)
            window['-ERROR_FRAME-'].update(visible=True)


        # Download all data
        if values['-OPTION-'] == 'Download all data (Non-repeated)':
            window['-DATES_FRAME-'].update(visible=False)
            window['-CONFIG_COL-' ].update(visible=False)
            window['-COLLATE_FILES-' ].update(visible=True)
            window['-STOP_SCHEDULER-' ].update(visible=False)
            window['-STATUS_text-'].update(visible=False)
            window['-STATUS-'].update(visible=False)
            window['-CHECK_DEVICE_INFO-'].update(visible=False)
            window['-ERROR_FRAME-'].update(visible=False)

        # Download specific slots in a specific date range
        if values['-OPTION-'] == 'Choose specific slots to download (Non-repeated)':
            window['-DATES_FRAME-'].update(visible=True)
            window['-CONFIG_COL-' ].update(visible=False)
            window['-COLLATE_FILES-' ].update(visible=False)
            window['-STOP_SCHEDULER-' ].update(visible=False)
            window['-STATUS_text-'].update(visible=False)
            window['-STATUS-'].update(visible=False)
            window['-CHECK_DEVICE_INFO-'].update(visible=False)
            window['-ERROR_FRAME-'].update(visible=False)

        # Set default start date to 00:00:00
        if event == '-START_DATE-':
            date, _ = values['-START_DATE-'].split(' ')
            window['-START_DATE-'].update(date + ' 00:00:00')
        
        # Set default end date to 23:59:59
        if event == '-END_DATE-':
            date, _ = values['-END_DATE-'].split(' ')
            window['-END_DATE-'].update(date + ' 23:59:59')

        # Only show device details when a device is selected
        if event == '-DEVICE-':
            slots_list = []
            window['-IP_text-'].update(visible=True)
            window['-PASSWORD_text-'].update(visible=True)
            window['-SLOTS_text-'].update(visible=True)
            window['-IP-'].update(visible=True)
            window['-PASSWORD-'].update(visible=True)
            window['-SLOTS-'].update(visible=True)
            device_num = values['-DEVICE-'].split(' ')[0]
            device = config.devices[device_num]
            print(device)
            window['-IP-'].update(value=device['ip'])
            window['-PASSWORD-'].update(value=device['password'])
            window['-SLOTS-'].update(value='')
            for slot_num, slot in device['slots'].items(): 
                window['-SLOTS-'].update(f'{slot}\n', append=True)

        # Save configuration
        if event == '-SAVE_CONFIG-':
            device_num = values['-DEVICE-'].split(' ')[0]
            config.directory = values['-DIRECTORY-']
            config.hour = values['-HOUR-']
            config.minute = values['-MINUTE-']
            config.devices[device_num]['ip'] = values['-IP-']
            config.devices[device_num]['password'] = values['-PASSWORD-']
            config.devices[device_num]['slots'].clear()
            slots_list = values['-SLOTS-'].split('\n')
            print(slots_list)
            slots_list = [slot for slot in slots_list if slot != '']
            for i in range(len(slots_list)):
                slots_list[i] = slots_list[i].strip()
                config.devices[device_num]['slots'][str(i+1)] = slots_list[i]
            device_num_dict = defaultdict()
            for device_number, device in config.devices.items():
                device_num_dict[device_number] = f"{device_number} ({device['ip']})"
            first_device = next(iter(device_num_dict))

            # Update values in window to show current device details
            window['-FOLDER_NAME-'].update(value=os.path.basename(os.path.normpath(config.directory)))
            window['-DEVICE-'].update(value=device_num_dict[device_num], values=list(device_num_dict.values()))
            window['-DEVICE_CHOICE-'].update(value=f"{config.device_choice} ({config.devices[config.device_choice]['ip']})", values=list(device_num_dict.values()))
            window['-IP-'].update(value=config.devices[device_num]['ip'])
            window['-PASSWORD-'].update(value=config.devices[device_num]['password'])
            window['-SLOTS-'].update(value='')
            for slot_num, slot in config.devices[device_num]['slots'].items(): 
                window['-SLOTS-'].update(f'{slot}\n', append=True)
            config.save()
            sg.popup('Configuration saved successfully!', icon='success')
        
        # Device chosen in specific slots to download
        if event == '-DEVICE_CHOICE-':
            config.device_choice = values['-DEVICE_CHOICE-'].split(' ')[0]
            config.save()

        # Add device to configuration
        if event == '-ADD_DEVICE-':
            device = popup_add_device()
            if device:
                device.num = f'device_{len(config.devices) + 1}'
                config.devices[device.num] = {'ip': device.ip, 'password': device.password, 'slots': {}}
                slots_list = device.slots.split('\n')
                print(slots_list)
                slots_list = [slot.strip() for slot in slots_list if slot.strip() != '']
                for i in range(len(slots_list)):
                    slots_list[i] = slots_list[i].strip()
                    config.devices[device.num]['slots'][str(i+1)] = slots_list[i]
                update_device_display(window, config)
                config.save()
                sg.popup('Device added successfully!', icon='success')

        # Remove device from configuration
        if event == '-REMOVE_DEVICE-':
            device = popup_remove_device(config)
            if device:
                device = device.split(' ')[0]
                del config.devices[device]
                update_device_display(window, config)
                config.save()
                sg.popup('Device removed successfully!', icon='success')

        # Test connection to device
        if event == '-TEST_IP-':
            print(values['-IP-'], values['-PASSWORD-'], values['-DEVICE-'].split(' ')[0])
            sg.popup_quick_message('Testing connection to device...', keep_on_top=True, background_color='grey')
            driver = initialise_driver(values['-IP-'], values['-PASSWORD-'], values['-DEVICE-'].split(' ')[0])
            if driver:
                sg.popup('Connection successful!', icon='success')
                driver.quit()
            else:
                sg.popup('Connection failed!', icon='error')
        
        if event == '-CHECK_DEVICE_INFO-':
            check_device_info(config)
            file = open('error_log.txt','r')
            window['-ERROR_LOG-'].update(value=file.read())   
            file.close()

        if event == '-CLEAR_ERROR_LOG-':
            open('error_log.txt', 'w').close()
            file = open('error_log.txt','r')
            window['-ERROR_LOG-'].update(value=file.read())   
            file.close()
            
        if event == '-COLLATE_FILES-' or event == '-DATES_CHOSEN-':
            if window['-OPTION-'] == '':
                sg.popup(title='No Option Selected', custom_text = 'Please select an option first', button_type=sg.POPUP_BUTTONS_OK, icon='error')
            else:
                # Parallel thread to execute the collation
                if window['-OPTION-'].get() == 'Automate Collation (Repeated)':
                    if not start_scheduler:
                        ui_selenium_automation.stop_thread = False
                        start_scheduler = True
                        tray.change_icon(sg.EMOJI_BASE64_HAPPY_JOY)
                        tray.show_message('Scheduler', 'Scheduler has been started')
                        window['-COLLATE_FILES-'].update(disabled=True)
                        window['-STOP_SCHEDULER-'].update(disabled=False)
                        window['-STATUS-'].update(value='Scheduler started', text_color='lightgreen')
                        automate_thread = threading.Thread(target= automate_time, args=(config, window, ))
                        automate_thread.start()
                        
                    else:
                        sg.popup('Scheduler has already been started', icon='warning')
                
                if window['-OPTION-'].get() == 'Download all data (Non-repeated)':
                    sg.popup_quick_message('Please wait for the data to be downloaded...', keep_on_top=True, background_color='grey')
                    # threading.Thread(target= run_automation, args=(config, 'all', window, )).start()
                    run_automation(config, 'all', window)

                elif window['-OPTION-'].get() == 'Choose specific slots to download (Non-repeated)':
                    sg.popup_quick_message('Please wait for the slots to be displayed...', keep_on_top=True, background_color='grey')
                    
                    driver, slots, directory = run_automation(config, 'choose', window)
                    if driver is None:
                        sg.popup('Error occurred!', icon='warning')
                        continue
                    else:
                        window['-SLOTS_COL-'].update(visible=True)
                        window['-SELECT_SLOTS_BTN-'].update(visible=True)
                        window['-COLLATE_FILES-'].update(visible=False)
                        window['-DATES_CHOSEN-'].update(disabled=True)
        
        # Stop scheduler within UI
        if event == '-STOP_SCHEDULER-':
            if start_scheduler == True:
                ui_selenium_automation.stop_thread = True
                start_scheduler = False
                automate_thread.join()
                window['-COLLATE_FILES-'].update(disabled=False)
                window['-STOP_SCHEDULER-'].update(disabled=True)
                window['-STATUS-'].update(value='Scheduler stopped', text_color='firebrick3')
                tray.change_icon(sg.DEFAULT_BASE64_ICON)
                tray.show_message('Scheduler', 'Scheduler has been stopped')
            else:
                sg.popup('Scheduler has not been started yet!')

        if event == 'EXECUTION DONE':
            window['-SLOTS_COL-'].update(visible=False)
            window['-SELECT_SLOTS_BTN-'].update(visible=False)
            window['-DATES_CHOSEN-'].update(disabled=False)
            
        if event == '-SLOTS_CHOSEN-':
            chosen_slots = []
            for i in range(len(slots)):
                if window[f'-SLOT{i+1}-'].get() == True:
                    chosen_slots.append(slots[i])
            print(chosen_slots)
            window['-SLOTS_CHOSEN-'].update(disabled=True)
            sg.popup_quick_message('Please wait for the download to complete...', keep_on_top=True, background_color='grey')
            choose_slot(driver, chosen_slots, window)
            collate_dataframes('choose', directory)
            driver.close()
            sg.popup(custom_text = 'Download successfully!', button_type=sg.POPUP_BUTTONS_OK, icon='success')
        
    tray.close()
    window.close()

if __name__ == '__main__':
    interface()