from selenium_automation import run_automation
from configuration import get_config
import PySimpleGUI as sg
import threading
from time import sleep
import os
# Add a touch of color
sg.theme('DarkBlue3')  

# Change font and font size
sg.set_options(font=('Helvetica', 12))
sg.set_options(tooltip_font=('Helvetica', 11))
# Default size for frames, can be changed
# WIDTH, HEIGHT = sg.Window.get_screen_size()
WIDTH = 400
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
    # Initial frame to choose option
    option_frame = [
        [sg.Text('Option'), sg.InputCombo(('1. Collate all data', '2. Choose specific slots to collate' ), size=(27, 2), key='-OPTION-')],
        [sg.Button('Collate Files', key='-COLLATE_FILES-', tooltip='Click to collate files in the chosen folder')]
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
        [sg.Frame('Choose your option', option_frame, size=(WIDTH,HEIGHT), visible=True, key='-OPTION_COL-'),]
    
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
    return sg.Window('L-QuBE DEOS Automation', layout, margins = margins, finalize=True, resizable=True)

# Main function to run the GUI
def interface():
    # config = get_config()
    # Create the window
    window = build()
    window['-OPTION-'].expand(expand_x=True, expand_y=False)
    window['-OPTION_COL-'].expand(True, True)
    popup_win = None
    layout = 1
    # Display window
    while True:
        event, values = window.read()
        # End program if user closes window or clicks cancel
        if event == sg.WIN_CLOSED or event == 'Exit':
            break

        if event == '-COLLATE_FILES-':
            if window['-OPTION-'] == '':
                sg.popup(title='No Option Selected', custom_text = 'Please select an option first', button_type=sg.POPUP_BUTTONS_OK, icon='error')
            else:
                config = get_config()
                popup_win = popup('Please wait while the files are being collated...')
                window.force_focus()
                window['-PROGRESS_COL-'].update(visible=True)
                # Parallel thread to execute the collation on top of the pop up loading
                if window['-OPTION-'].get() == '1. Collate all data':
                    threading.Thread(target= run_automation, args=(config, 'all', )).start()
                elif window['-OPTION-'].get() == '2. Choose specific slots to collate':
                    threading.Thread(target= run_automation, args=(config, 'choose', )).start()
        
        if event == 'EXECUTION DONE':
            popup_win.close()
            popup_win = None
            window['-PROGRESS_COL-'].update(visible=False)
            # window['-OPTION_COL-'].update(visible=False)
            window['-INFORM_USER_COL1-'].update(visible=True)
            # for i in range(1,5):
            #     window[f'button_{i}'].update(visible=True)
            window['-BUTTON_COL-'].update(visible=True)
        
        if event == 'COLLATION SUCCESSFUL':
            popup_win.close()
            popup_win = None
            window['-PROGRESS_COL-'].update(visible=False)
            sg.popup('Collation Successful! No errors found.')

        
        if event == '-BACK-':
            window['-OPTION_COL-'].update(visible=True)
            window['-ERROR_FILES_COL-'].update(visible=False)
            window['-DUPLICATE_TIMESTAMP_COL-'].update(visible=False)
            window['-BACK_COL-'].update(visible=False)
            window['-ERROR_FILES_LIST-'].update('')
            window['-DUPLICATE_TIMESTAMP_LIST-'].update('')


    window.close()

if __name__ == '__main__':
    interface()