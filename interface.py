import PySimpleGUI as sg
import threading
from configuration import get_config
from combined_automation import combined_collation
from time import sleep
# Add a touch of color
sg.theme('DarkBlue3')   

# Change font and font size
sg.set_options(font=('Helvetica', 12))
sg.set_options(tooltip_font=('Helvetica', 11))
# Default size for frames, can be changed
# WIDTH, HEIGHT = sg.Window.get_screen_size()
WIDTH = 400
HEIGHT = 300

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
        [sg.InputCombo(('1. Collate csv/excel files', ), size=(20, 1), key='-OPTION-')],
        [sg.Button('Submit Option', key='-SUBMIT_OPTION-')]
    ]

    error_files_frame = [
        [sg.Multiline(size=(WIDTH, HEIGHT), key='-ERROR_FILES_LIST-', expand_x=True, font=('Helvetica', 10))]
    ]

    duplicate_timestamp_frame = [
        [sg.Multiline(size=(WIDTH, HEIGHT), key='-DUPLICATE_TIMESTAMP_LIST-', expand_x=True, font=('Helvetica', 10))]
    ]

    missing_minutes_frame = [
        [sg.Multiline(size=(WIDTH, HEIGHT), key='-MISSING_MINUTES_LIST-', expand_x=True, font=('Helvetica', 10))]
    ]

    empty_cells_frame = [
        [sg.Multiline(size=(WIDTH, HEIGHT), key='-EMPTY_CELLS_LIST-', expand_x=True, font=('Helvetica', 10))]
    ]

    inform_user_frame_1 = [
        [sg.Frame("", error_files_frame, expand_x=True, expand_y=True)]    
    ]

    inform_user_frame_2 = [
        [sg.Frame("", duplicate_timestamp_frame, expand_x=True, expand_y=True)]
    ]

    inform_user_frame_3 = [
        [sg.Frame("", missing_minutes_frame, expand_x=True, expand_y=True)]
    ]

    inform_user_frame_4 = [
        [sg.Frame("", empty_cells_frame, expand_x=True, expand_y=True)]
    ]

    button_frame = [
        [sg.Button('1'), sg.Button('2'),
        sg.Button('3'), sg.Button('4')]
    ]


    back_button = [
        [sg.Button('Back', key='-BACK-')]
    ]
    progress_bar = [
        [sg.Text('', key='-PROGRESS_TEXT-', justification='center', size=(20, 1), expand_x=True)],
         [sg.ProgressBar(100, orientation='h', size=(40, 20), key='-PROGRESS_BAR-')]    
        ]
    
    # Layout to combine all frames
    # layout = [
    # [
    # sg.Frame('Progress Bar', progress_bar, size=(WIDTH,100), visible=False, key='-PROGRESS_COL-'),
    #  [sg.Frame('Choose your option', option_frame, size=(WIDTH,HEIGHT), visible=True, key='-OPTION_COL-'),
    #  sg.Frame('Error Files', error_files_frame, size=(WIDTH,HEIGHT), visible=False, key='-ERROR_FILES_COL-'),
    #  sg.Frame('Duplicate Timestamps', duplicate_timestamp_frame, size=(WIDTH,HEIGHT), visible=False, key='-DUPLICATE_TIMESTAMP_COL-')],
    # [sg.Frame('', back_button, size=(60,40), visible=False, key='-BACK_COL-')]
    
    #  ]
    # ]
    layout = [
        [
            sg.Frame('Progress Bar', progress_bar, size=(WIDTH,100), visible=False, key='-PROGRESS_COL-'),
            [sg.Frame('Choose your option', option_frame, size=(WIDTH,HEIGHT), visible=True, key='-OPTION_COL-'),
            sg.Frame('Error Files', inform_user_frame_1, size=(WIDTH,HEIGHT), visible=False, key='-INFORM_USER_COL1-'),
            sg.Frame('Duplicate Timestamps', inform_user_frame_2, size=(WIDTH,HEIGHT), visible=False, key='-INFORM_USER_COL2-'),
            sg.Frame('Missing Minutes', inform_user_frame_3, size=(WIDTH,HEIGHT), visible=False, key='-INFORM_USER_COL3-'),
            sg.Frame('Empty Cells', inform_user_frame_4, size=(WIDTH,HEIGHT), visible=False, key='-INFORM_USER_COL4-')],
            sg.Frame('', button_frame, visible=False, key='-BUTTON_COL-', element_justification='right')
        ]
    ]

    margins = (5, 5)
    return sg.Window('L-QuBE Automated Data Collation', layout, margins = margins, finalize=True, resizable=True)

# Main function to run the GUI
def interface():
    config = get_config()
    # Create the window
    window = build()
    popup_win = None
    layout = 1
    # Display window
    while True:
        event, values = window.read()
        # End program if user closes window or clicks cancel
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        
        if event == '-SUBMIT_OPTION-':
            popup_win = popup('Please wait while the files are being collated...')
            window.force_focus()
            window['-PROGRESS_COL-'].update(visible=True)
            # Parallel thread to execute the collation on top of the pop up loading
            threading.Thread(target= combined_collation, args=(config.collation,window, )).start()
        
        if event == 'EXECUTION DONE':
            popup_win.close()
            popup_win = None
            window['-PROGRESS_COL-'].update(visible=False)
            # window['-OPTION_COL-'].update(visible=False)
            window['-INFORM_USER_COL1-'].update(visible=True)
            # for i in range(1,5):
            #     window[f'button_{i}'].update(visible=True)
            window['-BUTTON_COL-'].update(visible=True)
        
        if event in '1234':
            window[f'-INFORM_USER_COL{layout}-'].update(visible=False)
            layout = int(event)
            window[f'-INFORM_USER_COL{layout}-'].update(visible=True)
        
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