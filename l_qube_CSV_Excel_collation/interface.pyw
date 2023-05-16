import PySimpleGUI as sg
import threading
from combined_automation import combined_collation
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
    valid_files_multiline = [
        [sg.Multiline(size=(MULTILINE_WIDTH, 5), key='-VALID_FILES_LIST-', expand_x=True, font=('Helvetica', 10))],
    ]
    invalid_files_multiline = [
        [sg.Multiline(size=(MULTILINE_WIDTH, 5), key='-INVALID_FILES_LIST-', expand_x=True, font=('Helvetica', 10))],
    ]
    folder_frame = [
        [sg.In(size=(35,1), enable_events=True ,key='-FOLDER-'), sg.FolderBrowse(tooltip='Click to choose folder')], 
        # [sg.Text('Option'), sg.InputCombo(('1. Collate csv/excel files', ), size=(20, 1), key='-OPTION-')],
        [sg.Frame('Valid Files', valid_files_multiline)],
        [sg.Frame('Invalid Files', invalid_files_multiline)],
        [sg.Button('Collate Files', key='-COLLATE_FILES-', tooltip='Click to collate files in the chosen folder')]
    ]
    summary_frame = [
        [sg.Multiline(size=(MULTILINE_WIDTH, HEIGHT), key='-SUMMARY_LIST-', expand_x=True, font=('Helvetica', 10))]
    ]
    error_files_frame = [
        [sg.Multiline(size=(MULTILINE_WIDTH, HEIGHT), key='-ERROR_FILES_LIST-', expand_x=True, font=('Helvetica', 10))]
    ]

    duplicate_timestamp_frame = [
        [sg.Multiline(size=(MULTILINE_WIDTH, HEIGHT), key='-DUPLICATE_TIMESTAMPS_LIST-', expand_x=True, font=('Helvetica', 10))]
    ]

    missing_minutes_frame = [
        [sg.Multiline(size=(MULTILINE_WIDTH, HEIGHT), key='-MISSING_MINUTES_LIST-', expand_x=True, font=('Helvetica', 10))]
    ]

    empty_cells_frame = [
        [sg.Multiline(size=(MULTILINE_WIDTH, HEIGHT), key='-EMPTY_CELLS_LIST-', expand_x=True, font=('Helvetica', 10))]
    ]

    inform_user_frame_1 = [
        [sg.Frame("", summary_frame, expand_x=True, expand_y=True)]
    ]

    inform_user_frame_2 = [
        [sg.Frame("", error_files_frame, expand_x=True, expand_y=True)]    
    ]

    inform_user_frame_3 = [
        [sg.Frame("", duplicate_timestamp_frame, expand_x=True, expand_y=True)]
    ]

    inform_user_frame_4 = [
        [sg.Frame("", missing_minutes_frame, expand_x=True, expand_y=True)]
    ]

    inform_user_frame_5 = [
        [sg.Frame("", empty_cells_frame, expand_x=True, expand_y=True)]
    ]

    button_frame = [
        [sg.Button('Summary', key='1', tooltip='Click to view summary of faults'),
         sg.Button('Error Files', key='2', tooltip='Click to view the error file(s) which is/are ignored in the collated file'),
         sg.Button('Duplicate Timestamp', key='3', tooltip='Click to view the duplicate timestamp(s) detected'), 
         sg.Button('Missing Minutes', key='4', tooltip='Click to view the missing minute(s) added in the collated file'), 
         sg.Button('Empty Cells', key='5', tooltip='Click to view the empty cell(s) detected')
        ]
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
            [sg.Frame('Choose your folder', folder_frame, size=(WIDTH,HEIGHT), visible=True, key='-OPTION_COL-'),
            sg.Frame('Summary', inform_user_frame_1, size=(MULTILINE_WIDTH,HEIGHT), visible=False, key='-INFORM_USER_COL1-', expand_x=True, expand_y=True),
            sg.Frame('Error Files', inform_user_frame_2, size=(MULTILINE_WIDTH,HEIGHT), visible=False, key='-INFORM_USER_COL2-', expand_x=True, expand_y=True),
            sg.Frame('Duplicate Timestamps Detected', inform_user_frame_3, size=(MULTILINE_WIDTH,HEIGHT), visible=False, key='-INFORM_USER_COL3-', expand_x=True, expand_y=True),
            sg.Frame('Missing Minutes Added', inform_user_frame_4, size=(MULTILINE_WIDTH,HEIGHT), visible=False, key='-INFORM_USER_COL4-', expand_x=True, expand_y=True),
            sg.Frame('Empty Cells Detected', inform_user_frame_5, size=(MULTILINE_WIDTH,HEIGHT), visible=False, key='-INFORM_USER_COL5-', expand_x=True, expand_y=True)],
            sg.Frame('', button_frame, visible=False, key='-BUTTON_COL-', element_justification='right')
        ]
    ]

    margins = (5, 5)
    return sg.Window('L-QuBE Automated CSV/Excel Data Collation', layout, margins = margins, finalize=True, resizable=True)

# Main function to run the GUI
def interface():
    # config = get_config()
    # Create the window
    window = build()
    window['-ERROR_FILES_LIST-'].expand(True, True)
    window['-DUPLICATE_TIMESTAMPS_LIST-'].expand(True, True)
    window['-MISSING_MINUTES_LIST-'].expand(True, True)
    window['-EMPTY_CELLS_LIST-'].expand(True, True)
    popup_win = None
    layout = 1
    folder = ''
    # Display window
    while True:
        event, values = window.read()
        # End program if user closes window or clicks cancel
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        
        if event == '-FOLDER-':
            folder = values['-FOLDER-']
            print(folder)
            window['-VALID_FILES_LIST-'].update('')
            window['-INVALID_FILES_LIST-'].update('')
            file_name = os.listdir(folder)
            for file in file_name:
                if file.endswith('collated.csv') or file.endswith('collated.xlsx'):
                    window['-INVALID_FILES_LIST-'].update(file + '\n', append=True)
                elif file.endswith('.csv') or file.endswith('.xlsx'):
                    window['-VALID_FILES_LIST-'].update(file + '\n', append=True)
                else:
                    window['-INVALID_FILES_LIST-'].update(file + '\n', append=True)

        if event == 'NO FILES':
            popup_win.close()
            popup_win = None
            window['-PROGRESS_COL-'].update(visible=False)
            sg.popup(title='No Valid Files Found', custom_text = 'No valid files found in the selected folder', button_type=sg.POPUP_BUTTONS_OK, icon='error')

        if event == '-COLLATE_FILES-':
            if folder == '':
                sg.popup(title='No Folder Selected', custom_text = 'Please select a folder first', button_type=sg.POPUP_BUTTONS_OK, icon='error')
            else:
                for i in range(1,6):
                    window[f'-INFORM_USER_COL{i}-'].update(visible=False)
                window['-SUMMARY_LIST-'].update('')
                window['-ERROR_FILES_LIST-'].update('')
                window['-DUPLICATE_TIMESTAMPS_LIST-'].update('')
                window['-MISSING_MINUTES_LIST-'].update('')
                window['-EMPTY_CELLS_LIST-'].update('')
                window['-BUTTON_COL-'].update(visible=False)
                
                popup_win = popup('Please wait while the files are being collated...')
                window.force_focus()
                window['-PROGRESS_COL-'].update(visible=True)
                # Parallel thread to execute the collation on top of the pop up loading
                threading.Thread(target= combined_collation, args=(folder, window, )).start()
        
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

        if event in '12345':
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