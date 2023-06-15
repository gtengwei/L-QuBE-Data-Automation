from ui_selenium_automation import run_automation, choose_slot, collate_dataframes, automate_time
import ui_selenium_automation
from configuration import get_config
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
# WIDTH, HEIGHT = sg.Window.get_screen_size()
WIDTH = 420
HEIGHT = 350

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

# Popup loading message
def popup(message):
    sg.theme('DarkGrey')
    layout = [[sg.Text(message)]]
    window = sg.Window('Message', layout, no_titlebar=True, keep_on_top=True, finalize=True)
    return window

# Build the GUI
def build():
    # Frame to choose dates
    date_frame = [
        [sg.InputText('', size=(20, 1), key='-START_DATE-', disabled=True, tooltip='Start Date', enable_events=True),
         sg.CalendarButton('Choose Start Date', target='-START_DATE-', key='-CALENDAR-', tooltip='Click to choose date', size=(20, 1), format='%m-%d-%Y %H:%M:%S', )],
        [sg.InputText('', size=(20, 1), key='-END_DATE-', disabled=True, tooltip='End Date', enable_events=True),
         sg.CalendarButton('Choose End Date', target='-END_DATE-', key='-CALENDAR-', tooltip='Click to choose date', size=(20, 1), format='%m-%d-%Y %H:%M:%S')],
        [sg.InputCombo('default', size=(24, len(config.devices.keys())), key='-DEVICE_CHOICE-', tooltip='Choose which device to choose slots from', enable_events=True)],
        [sg.Button('Select Dates', key='-DATES_CHOSEN-', tooltip='Click to select dates to collate')],

    ]
    device_input_combo = [
        sg.InputCombo(('default'), size=(24, len(config.devices.keys())), default_value=next(iter(config.devices)), key='-DEVICE-', tooltip='Device Name', enable_events=True)
    ]
    
    device_parameters =[
        [sg.Text(size=(12,1)), sg.Text('IP', size=(8, 1), key='-IP_text-', visible=False), sg.InputText('default ip', key='-IP-', tooltip='IP Address of device', enable_events=True, visible=False, size=(30, 1))],
        [sg.Text(size=(12,1)), sg.Text('Password', size=(8, 1), key='-PASSWORD_text-', visible=False), sg.InputText('default password', key='-PASSWORD-', tooltip='Password of device', enable_events=True, visible=False, size=(30, 1))],
        [sg.Text(size=(12,1)), sg.Text('Slots', size=(8, 1), key='-SLOTS_text-', visible=False), sg.InputCombo('default', size=(20, 5), key='-SLOTS-', tooltip='Slots to collate data from', enable_events=True, visible=False),],
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
        [sg.Button('Save Configuration', key='-SAVE_CONFIG-', tooltip='Click to save configuration')],
    ]
    
    

    # Initial frame to choose option
    option_frame = [
        [sg.Text('Option'), 
         sg.InputCombo(('Edit Configuration',
                        'Automate Collation (Repeated)',
                        'Download all data (Non-repeated)', 
                        'Choose specific slots to download (Non-repeated)',), default_value='Edit Configuration', enable_events=True, size=(70, 4), key='-OPTION-')],
        [sg.Button('Start Collation', key='-COLLATE_FILES-', tooltip='Click to collate files in the chosen folder', visible=False), 
         sg.Button('Stop Collation', key='-STOP_SCHEDULER-', tooltip='Click to stop scheduler', visible=False)],
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
    # layout = [
    #     [
    #         sg.Frame('Progress Bar', progress_bar, size=(WIDTH,100), visible=False, key='-PROGRESS_COL-'),
    #         [sg.Frame('Choose your folder', folder_frame, size=(WIDTH,HEIGHT), visible=True, key='-OPTION_COL-'),
    #         sg.Frame('Summary', inform_user_frame_1, size=(MULTILINE_WIDTH,HEIGHT), visible=False, key='-INFORM_USER_COL1-', expand_x=True, expand_y=True),
    #         sg.Frame('Error Files', inform_user_frame_2, size=(MULTILINE_WIDTH,HEIGHT), visible=False, key='-INFORM_USER_COL2-', expand_x=True, expand_y=True),
    #         sg.Frame('Duplicate Timestamps Detected', inform_user_frame_3, size=(MULTILINE_WIDTH,HEIGHT), visible=False, key='-INFORM_USER_COL3-', expand_x=True, expand_y=True),
    #         sg.Frame('Missing Minutes Added', inform_user_frame_4, size=(MULTILINE_WIDTH,HEIGHT), visible=False, key='-INFORM_USER_COL4-', expand_x=True, expand_y=True),
    #         sg.Frame('Empty Cells Detected', inform_user_frame_5, size=(MULTILINE_WIDTH,HEIGHT), visible=False, key='-INFORM_USER_COL5-', expand_x=True, expand_y=True)],
    #         sg.Frame('', button_frame, visible=False, key='-BUTTON_COL-', element_justification='right')
    #     ]
    # ]

    margins = (5, 5)
    return sg.Window('L-QuBE DEOS Automation', layout, margins = margins, finalize=True, resizable=True, enable_close_attempted_event=True)

# Main function to run the GUI
def interface():
    # config = get_config()
    # Create the window
    window = build()
    menu = ['', ['Show Window', 'Hide Window', '---', 'Scheduler',['Start Scheduler','End Scheduler'], 'Change Icon', ['Happy', 'Sad', 'Plain'], 'Exit']]
    tooltip = 'Double click to show interface'
    tray = SystemTray(menu, single_click_events=False, window=window, tooltip=tooltip, icon=sg.DEFAULT_BASE64_ICON)
    tray.show_message('DEOS Interface', 'DEOS Interface launched!')
    # window.maximize()
    # window['-OPTION-'].expand(expand_x=True, expand_y=False)
    window['-OPTION_COL-'].expand(True, True)
    popup_win = None
    layout = 1
    start_scheduler = False
    window['-START_DATE-'].update(value=dt.datetime.now().strftime('%m-%d-%Y' + ' 00:00:00'))
    window['-END_DATE-'].update(value=dt.datetime.now().strftime('%m-%d-%Y %H:%M:%S'))
    config = get_config()
    device_num_dict = defaultdict()
    for device_num, device in config.devices.items():
        device_num_dict[device_num] = f"{device_num} ({device['ip']})"
    first_device = next(iter(device_num_dict))
    window['-DEVICE-'].update(value=next(iter(device_num_dict.values())), values=list(device_num_dict.values()))
    window['-DEVICE_CHOICE-'].update(value=f"{config.device_choice} ({config.devices[config.device_choice]['ip']})", values=list(device_num_dict.values()))
    window['-IP-'].update(value=config.devices[first_device]['ip'])
    window['-PASSWORD-'].update(value=config.devices[first_device]['password'])
    # Display window
    while True:
        event, values = window.read()
        # print(event)
        # print(values['-OPTION-'])
        # print(values['-START_DATE-'])
        # End program if user closes window or clicks cancel
        if event == tray.key:
            # sg.cprint(f'System Tray Event = ', values[event], c='white on red')
            event = values[event]       # use the System Tray's event as if was from the window

        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        
        print(event)
        print(tray.menu_items[3])
        tray.show_message(title=event)
        if event == 'End Scheduler':
            if start_scheduler == True:
                ui_selenium_automation.stop_thread = True
                automate_thread.join()
                tray.show_message('Scheduler', 'Scheduler has been stopped')
            else:
                sg.popup('Scheduler has not been started yet!')

        elif event == 'Start Scheduler':
            if start_scheduler == False:
                automate_thread = threading.Thread(target= automate_time, args=(config, window, ))
                automate_thread.start()
                tray.show_message('Scheduler', 'Scheduler has been started')
            else:
                sg.popup('Scheduler has already been started!')
        if event in ('Show Window', sg.EVENT_SYSTEM_TRAY_ICON_DOUBLE_CLICKED):
            window.un_hide()
            window.bring_to_front()
        elif event in ('Hide Window', sg.WIN_CLOSE_ATTEMPTED_EVENT):
            window.hide()
            tray.show_icon()        # if hiding window, better make sure the icon is visible
            tray.show_message('Exiting', 'Minimising to tray')
        elif event == 'Happy':
            tray.change_icon(sg.EMOJI_BASE64_HAPPY_JOY)
        elif event == 'Sad':
            tray.change_icon(sg.EMOJI_BASE64_FRUSTRATED)
        elif event == 'Plain':
            tray.change_icon(sg.DEFAULT_BASE64_ICON)
        elif event == 'Hide Icon':
            tray.hide_icon()
        elif event == 'Show Icon':
            tray.show_icon()

        if values['-OPTION-'] == 'Edit Configuration':
            window['-DATES_FRAME-'].update(visible=False)
            window['-COLLATE_FILES-' ].update(visible=False)
            window['-CONFIG_COL-' ].update(visible=True)
            window['-STOP_SCHEDULER-' ].update(visible=False)

        if values['-OPTION-'] == 'Automate Collation (Repeated)':
            window['-DATES_FRAME-'].update(visible=False)
            window['-CONFIG_COL-' ].update(visible=False)
            window['-COLLATE_FILES-' ].update(visible=True)
            window['-STOP_SCHEDULER-' ].update(visible=True)

        if values['-OPTION-'] == 'Download all data (Non-repeated)':
            window['-DATES_FRAME-'].update(visible=False)
            window['-CONFIG_COL-' ].update(visible=False)
            window['-COLLATE_FILES-' ].update(visible=True)
            window['-STOP_SCHEDULER-' ].update(visible=False)

        if values['-OPTION-'] == 'Choose specific slots to download (Non-repeated)':
            window['-DATES_FRAME-'].update(visible=True)
            window['-CONFIG_COL-' ].update(visible=False)
            window['-COLLATE_FILES-' ].update(visible=False)
            window['-STOP_SCHEDULER-' ].update(visible=False)

        if event == '-START_DATE-':
            date, _ = values['-START_DATE-'].split(' ')
            window['-START_DATE-'].update(date + ' 00:00:00')
        
        if event == '-END_DATE-':
            date, _ = values['-END_DATE-'].split(' ')
            window['-END_DATE-'].update(date + ' 23:59:59')

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
            for slot_num, slot in device['slots'].items(): 
                slots_list.append(slot)
            window['-SLOTS-'].update(value='', values=slots_list)

        if event == '-SAVE_CONFIG-':
            device_num = values['-DEVICE-'].split(' ')[0]
            config.directory = values['-DIRECTORY-']
            config.hour = values['-HOUR-']
            config.minute = values['-MINUTE-']
            config.devices[device_num]['ip'] = values['-IP-']
            config.devices[device_num]['password'] = values['-PASSWORD-']
            # config.devices[device_num]['slots'] = values['-SLOTS-']
            config.save()
            device_num_dict = defaultdict()
            for device_num, device in config.devices.items():
                device_num_dict[device_num] = f"{device_num} ({device['ip']})"
            first_device = next(iter(device_num_dict))
            window['-DEVICE-'].update(value=next(iter(device_num_dict.values())), values=list(device_num_dict.values()))
            window['-DEVICE_CHOICE-'].update(value=f"{config.device_choice} ({config.devices[config.device_choice]['ip']})", values=list(device_num_dict.values()))
            window['-IP-'].update(value=config.devices[first_device]['ip'])
            window['-PASSWORD-'].update(value=config.devices[first_device]['password'])
            sg.popup('Configuration saved successfully!', icon='success')
        
        if event == '-DEVICE_CHOICE-':
            config.device_choice = values['-DEVICE_CHOICE-'].split(' ')[0]
            config.save()

        if event == '-COLLATE_FILES-' or event == '-DATES_CHOSEN-':
            if window['-OPTION-'] == '':
                sg.popup(title='No Option Selected', custom_text = 'Please select an option first', button_type=sg.POPUP_BUTTONS_OK, icon='error')
            else:
                # popup_win = popup('Please wait for the UI to load...')
                # window.force_focus()
                # window['-PROGRESS_COL-'].update(visible=True)
                # Parallel thread to execute the collation on top of the pop up loading
                if window['-OPTION-'].get() == 'Automate Collation (Repeated)':
                    automate_thread = threading.Thread(target= automate_time, args=(config, window, ))
                    automate_thread.start()
                    start_scheduler = True

                
                if window['-OPTION-'].get() == 'Download all data (Non-repeated)':
                    threading.Thread(target= run_automation, args=(config, 'all', window, )).start()

                elif window['-OPTION-'].get() == 'Choose specific slots to download (Non-repeated)':
                    sg.popup_quick_message('Please wait for the slots to be displayed...', keep_on_top=True, background_color='grey')
                    window['-SLOTS_COL-'].update(visible=True)
                    window['-SELECT_SLOTS_BTN-'].update(visible=True)
                    window['-COLLATE_FILES-'].update(visible=False)
                    window['-DATES_CHOSEN-'].update(disabled=True)
                    driver, slots, directory = run_automation(config, 'choose', window)
                    
        
        if event == '-STOP_SCHEDULER-':
            if start_scheduler == True:
                ui_selenium_automation.stop_thread = True
                automate_thread.join()
                tray.show_message('Scheduler', 'Scheduler has been stopped')
            else:
                sg.popup('Scheduler has not been started yet!')

        if event == 'EXECUTION DONE':
            window['-SLOTS_COL-'].update(visible=False)
            window['-SELECT_SLOTS_BTN-'].update(visible=False)
            window['-COLLATE_FILES-'].update(visible=True)
            window['-DATES_CHOSEN-'].update(disabled=False)
        
        if event == '-START_SCHEDULER-':
            sg.popup(title='Scheduler Started', custom_text = 'Scheduler started successfully!', button_type=sg.POPUP_BUTTONS_OK, icon='success')
        
            
        if event == '-SLOTS_CHOSEN-':
            chosen_slots = []
            for i in range(len(slots)):
                if window[f'-SLOT{i+1}-'].get() == True:
                    chosen_slots.append(slots[i])
            print(chosen_slots)
            sg.popup_quick_message('Please wait for the download to complete...', keep_on_top=True, background_color='grey')
            choose_slot(driver, chosen_slots, window)
            collate_dataframes('choose', directory)
            driver.close()
            sg.popup(custom_text = 'Download successfully!', button_type=sg.POPUP_BUTTONS_OK, icon='success')
        
        if event == '-BACK-':
            window['-OPTION_COL-'].update(visible=True)
            window['-ERROR_FILES_COL-'].update(visible=False)
            window['-DUPLICATE_TIMESTAMP_COL-'].update(visible=False)
            window['-BACK_COL-'].update(visible=False)
            window['-ERROR_FILES_LIST-'].update('')
            window['-DUPLICATE_TIMESTAMP_LIST-'].update('')

    tray.close()
    window.close()

if __name__ == '__main__':
    interface()