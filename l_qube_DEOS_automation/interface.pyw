from ui_selenium_automation import run_automation, choose_slot, collate_dataframes, automate_time
from configuration import get_config
import PySimpleGUI as sg
from psgtray import SystemTray
import threading
import datetime as dt

# Add a touch of color
sg.theme('DarkBlue3')  

# Change font and font size
sg.set_options(font=('Helvetica', 12))
sg.set_options(tooltip_font=('Helvetica', 11))
# Default size for frames, can be changed
# WIDTH, HEIGHT = sg.Window.get_screen_size()
WIDTH = 420
HEIGHT = 350

MULTILINE_WIDTH = 550

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
        [sg.Text('Choose the date to collate')],
        [sg.InputText('', size=(20, 1), key='-START_DATE-', disabled=True, tooltip='Start Date', enable_events=True),
         sg.CalendarButton('Choose Start Date', target='-START_DATE-', key='-CALENDAR-', tooltip='Click to choose date', size=(20, 1), format='%m-%d-%Y %H:%M:%S', )],
        [sg.InputText('', size=(20, 1), key='-END_DATE-', disabled=True, tooltip='End Date', enable_events=True),
         sg.CalendarButton('Choose End Date', target='-END_DATE-', key='-CALENDAR-', tooltip='Click to choose date', size=(20, 1), format='%m-%d-%Y %H:%M:%S')],
        [sg.Button('Select Dates', key='-DATES_CHOSEN-', tooltip='Click to select dates to collate')]

    ]
    # Initial frame to choose option
    option_frame = [
        [sg.Text('Option'), sg.InputCombo(('Collate all data (Non-repeated)', 'Choose specific slots to collate (Non-repeated)'), enable_events=True, size=(27, 2), key='-OPTION-', expand_x=True)],
        [sg.Button('Collate Files', key='-COLLATE_FILES-', tooltip='Click to collate files in the chosen folder', visible=False)],
                        'Choose specific slots to collate (Non-repeated)',), enable_events=True, size=(27, 3), key='-OPTION-', expand_x=True)],
        [sg.Frame('Choose your Dates', date_frame, size=(WIDTH,HEIGHT), visible=False, key='-DATES_FRAME-', expand_x=True, expand_y=True)],
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
        sg.Frame('Choose your slots', slots_column_frame, size=(WIDTH,HEIGHT), expand_x=True, expand_y=True, visible=False, key='-SLOTS_COL-')],
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
    menu = ['', ['Show Window', 'Hide Window', '---', 'End Scheduler', 'Change Icon', ['Happy', 'Sad', 'Plain'], 'Exit']]
    tooltip = 'Double click to show interface'
    tray = SystemTray(menu, single_click_events=False, window=window, tooltip=tooltip, icon=sg.DEFAULT_BASE64_ICON)
    tray.show_message('System Tray', 'System Tray Icon Started!')
    # window.maximize()
    # window['-OPTION-'].expand(expand_x=True, expand_y=False)
    window['-OPTION_COL-'].expand(True, True)
    popup_win = None
    layout = 1
    window['-START_DATE-'].update(value=dt.datetime.now().strftime('%m-%d-%Y' + ' 00:00:00'))
    window['-END_DATE-'].update(value=dt.datetime.now().strftime('%m-%d-%Y %H:%M:%S'))
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
        tray.show_message(title=event)

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

        if values['-OPTION-'] == 'Collate all data (Non-repeated)':
            window['-DATES_FRAME-'].update(visible=False)
            window['-COLLATE_FILES-' ].update(visible=True)

        if values['-OPTION-'] == 'Choose specific slots to collate (Non-repeated)':
            window['-DATES_FRAME-'].update(visible=True)
            window['-COLLATE_FILES-' ].update(visible=False)

        if event == '-START_DATE-':
            date, _ = values['-START_DATE-'].split(' ')
            window['-START_DATE-'].update(date + ' 00:00:00')
        
        if event == '-END_DATE-':
            date, _ = values['-END_DATE-'].split(' ')
            window['-END_DATE-'].update(date + ' 23:59:59')

        if event == '-COLLATE_FILES-' or event == '-DATES_CHOSEN-':
            if window['-OPTION-'] == '':
                sg.popup(title='No Option Selected', custom_text = 'Please select an option first', button_type=sg.POPUP_BUTTONS_OK, icon='error')
            else:
                config = get_config()
                # popup_win = popup('Please wait for the UI to load...')
                # window.force_focus()
                # window['-PROGRESS_COL-'].update(visible=True)
                # Parallel thread to execute the collation on top of the pop up loading
                if window['-OPTION-'].get() == '1. Collate all data':
                    threading.Thread(target= run_automation, args=(config, 'all', window, )).start()
                elif window['-OPTION-'].get() == 'Choose specific slots to collate (Non-repeated)':
                    window['-SLOTS_COL-'].update(visible=True)
                    window['-SELECT_SLOTS_BTN-'].update(visible=True)
                    window['-COLLATE_FILES-'].update(visible=False)
                    # threading.Thread(target= run_automation, args=(config, 'choose', window, )).start()
                    driver, slots, directory = run_automation(config, 'choose', window)
        
        if event == 'EXECUTION DONE':
            window['-SLOTS_COL-'].update(visible=False)
            window['-SELECT_SLOTS_BTN-'].update(visible=False)
            window['-COLLATE_FILES-'].update(visible=True)
        
        # if event == 'CHOOSING SLOTS':
        #     popup_win.close()
        #     popup_win = None
            
        if event == '-SLOTS_CHOSEN-':
            chosen_slots = []
            for i in range(len(slots)):
                if window[f'-SLOT{i+1}-'].get() == True:
                    chosen_slots.append(slots[i])
            print(chosen_slots)
            choose_slot(driver, chosen_slots, window)
            collate_dataframes('choose', directory)
            sg.popup(title='Collation Completed', custom_text = 'Collation completed successfully!', button_type=sg.POPUP_BUTTONS_OK, icon='success')
        
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