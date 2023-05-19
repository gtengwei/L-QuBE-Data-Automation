import os
import pandas as pd
import numpy as np
import datetime as dt
from collections import defaultdict

DATE = ['Date', 'date', 'DATE']
TIME = ['Time', 'time', 'TIME']

DATE_FORMAT = ['%d/%m/%Y', '%d/%m/%y', 
                    '%d-%m-%Y', '%d-%m-%y', 
                    '%d.%m.%Y', '%d.%m.%y', 
                    '%d %m %Y', '%d %m %y',
                    '%d%m%Y', '%d%m%y',
                    '%Y/%m/%d', '%y/%m/%d',
                    '%Y-%m-%d', '%y-%m-%d',
                    '%Y.%m.%d', '%y.%m.%d',
                    '%m/%d/%Y', '%m/%d/%y',
                    '%m-%d-%Y', '%m-%d-%y',
                    '%m.%d.%Y', '%m.%d.%y',
                    '%m %d %Y', '%m %d %y',
                    '%m%d%Y', '%m%d%y']

DATE_AND_TIME = ['Date and Time', 'date and time', 'DATE AND TIME',
                'Date & Time',  'date & time', 'DATE & TIME',
                'Date_Time', 'date_time', 'DATE_TIME',
                'Date Time', 'date time', 'DATE TIME'
                ]

def get_current_date():
    return dt.datetime.now().strftime("%Y-%m-%d")

def insert_empty_slot(df, missing_minutes_dict, file):
    num_of_days = df['Date'].unique()
    hour_minute_list = [[i,j] for i in range(0,24) for j in range(0,60)]
    for i in range(len(hour_minute_list)):
        hour_minute_list[i] = ['%02d' % hour_minute_list[i][0], '%02d' % hour_minute_list[i][1]]

    empty_row = [None for _ in range(len(df.columns))]
    for day in num_of_days:
        temp_hour_minute_list = hour_minute_list.copy()
        for i in range(len(df['Timestamp'])):
            if df['Date'][i] == day:
                temp = df['Timestamp'][i].split(':')
                if [temp[0],temp[1]] in temp_hour_minute_list:
                    temp_hour_minute_list.remove([temp[0],temp[1]])
            else:
                continue
        for i in range(len(temp_hour_minute_list)):
            temp = ':'.join(temp_hour_minute_list[i])
            empty_row[0] = day
            empty_row[1] = temp
            df.loc[len(df)] = empty_row
            missing_minutes_dict[file, empty_row[0]].append(temp)
    # print(hour_minute_list)
    
    # empty_row = [None for _ in range(len(df.columns))]
    # for i in range(len(temp_hour_minute_list)):
    #     hour_minute_list[i] = ':'.join(temp_hour_minute_list[i])
    #     empty_row[0] = df['Date'][0]
    #     empty_row[1] = temp_hour_minute_list[i]
    #     df.loc[len(df)] = empty_row
    #     missing_minutes_dict[file, empty_row[0]].append(temp_hour_minute_list[i])
    df = df.sort_values(by=['Date', 'Timestamp'], ascending=[True,True])
    # df.to_csv('test.csv', index=False)
    return df

def csv_collation(file, collated_df, files_with_errors, files_with_duplicate_timestamp_dict, missing_minutes_dict, empty_cells_timestamp_dict):
    try:
        file_lines = []
        # Open the file in read mode and read the lines
        with open(file, 'r') as f:
            for line in f:
                file_lines.append(line.strip())

        # Split the lines into words, remove empty strings caused by additional columns and add to list
        for i in range(len(file_lines)):
            file_lines[i] = file_lines[i].strip(',').split(',')
            
        for i in range(2):
            for j in range(len(file_lines[i])):
                if file_lines[i][j] == '':
                    file_lines[i][j] = np.nan

        # Read the cleaned list into a Pandas DataFrame
        # For csv files with slot name in the first cell
        if len(file_lines[0]) < 2:
            df = pd.DataFrame(file_lines[2:],columns=file_lines[1])
        # For csv files with no slot name in first cell
        else:
            df = pd.DataFrame(file_lines[1:],columns=file_lines[0])

        try:
            df.columns.get_loc('Timestamp')
        except:
            for time in TIME:
                if time in df.columns:
                    df = df.rename(columns={time: 'Timestamp'})
                    break 
            # df = df.rename(columns={'Time': 'Timestamp'})

        # From here onwards, its the same as excel collation 
        return csv_excel_df_manipulation(file, collated_df, df, files_with_duplicate_timestamp_dict, missing_minutes_dict, empty_cells_timestamp_dict)
        
    except Exception as e:
        print(e)
        files_with_errors.append((file, e, 'There is no column header in the CSV file.'))
        return collated_df

def excel_collation(file, collated_df, files_with_errors, files_with_duplicate_timestamp_dict, missing_minutes_dict, empty_cells_timestamp_dict):
    try: 
        date_and_time_format = ''
        df = pd.read_excel(file, sheet_name=0, header=None)
        df = df.reset_index(drop=True)
        # print(df.head())
        df = df.replace(r'^\s*$', np.nan, regex=True)
        df = df.replace('None', np.nan, regex=True)
        number_of_columns = len(df.columns)
        for i, row in df.iterrows():
            # print(row.isnull().sum())
            if row.isnull().sum() >= number_of_columns-5:
                df.drop(i,inplace=True)
            else:
                break
        
        
        df.columns = df.iloc[0]
        df = df.drop(df.index[0])
        df = df.reset_index()
        df = df.dropna(how='all')
        df.drop(columns=['index'], axis=1, inplace=True)
        print(file)
        try:
            df.columns.get_loc('Timestamp')
        except:
            for time in TIME:
                if time in df.columns:
                    df = df.rename(columns={time: 'Timestamp'})
                    break
            
        try:
            # Check if there is a Date column
            df.columns.get_loc('Date')
        except:
            # If there is no Date column, check for date column name in DATE
            for date in DATE:
                if date in df.columns:
                    df = df.rename(columns={date: 'Date'})
                    break

        for date_time in DATE_AND_TIME:
            try:
                df[date_time] = df[date_time].str.split(' ')
                df['Date'] = df[date_time].str[0]
                date_and_time_format = date_time

                timestamp_split = df[date_time].str[1].str.strip(':')
                timestamp_split = timestamp_split.str.split(':')
                df['Timestamp'] = timestamp_split.apply(lambda x: str('%02d' % int(x[0])) + ':' + str('%02d' % int(x[1])))
                break
            except:
                pass
        
        if date_and_time_format != '':
            df.drop(columns=[date_and_time_format], axis=1, inplace=True)
        print(df.columns)

        # From here onwards, its the same as csv collation
        return csv_excel_df_manipulation(file, collated_df, df, files_with_duplicate_timestamp_dict, missing_minutes_dict, empty_cells_timestamp_dict)
        
    except Exception as e:
        print(e)
        files_with_errors.append((file, e, 'There is no column header in the CSV file.'))
        return collated_df

def csv_excel_df_manipulation(file, collated_df, df, files_with_duplicate_timestamp_dict, missing_minutes_dict, empty_cells_timestamp_dict):
    
    # Replace blank/None cells with NaN
    df = df.replace(r'^\s*$', np.nan, regex=True)
    df = df.replace('None', np.nan, regex=True)
    df = df[df['Timestamp'].notna()]
    df = df.reset_index(drop=True)   

    # Optimised code for timestamp manipulation
    df['Timestamp'] = df['Timestamp'].astype(str)
    df['Timestamp'] = df['Timestamp'].str.split(':')
    df['Timestamp'] = df['Timestamp'].apply(lambda x: str('%02d' % int(x[0])) + ':' + str('%02d' % int(x[1])))

    try:
        # Check if there is a Date column
        df.columns.get_loc('Date')
    except:
        # If there is no Date column, check for date column name in DATE
        for date in DATE:
            if date in df.columns:
                df = df.rename(columns={date: 'Date'})
                break
    for date_format in DATE_FORMAT:
        try:
            df['Date'] = pd.to_datetime(df['Date'], format=date_format)
            break
        except:
            continue       
    
    # Need these columns to keep original column order
    cols = collated_df.columns.append(df.columns).unique()
    cols = cols.drop(['Date','Timestamp'])

    # Convert Date datetime to str before proceeding
    df['Date'] = df['Date'].dt.strftime('%d/%m/%Y')

    # Will be used to locate duplicate timestamps and empty cells
    timestamp_column_index = df.columns.get_loc('Timestamp')
    date_column_index = df.columns.get_loc('Date')

    # NEED TO DROP EMPTY COLUMN NAMES AND CELLS to prevent error
    df = df.loc[:, df.columns.notna()]
    df = df[df['Timestamp'].notna()]

    # Tracking of duplicate timestamp
    duplicate_df = df[df.duplicated(subset=['Date', 'Timestamp'])]
    # print(duplicate_df.head())
    # print((duplicate_df[['Date','Timestamp']]).values.tolist())
    duplicate_date_timestamp = duplicate_df[['Date','Timestamp']].values.tolist()
    # duplicate_timestamp = [str(date) +' {} '.format(timestamp) for timestamp in duplicate_timestamp]
    if duplicate_date_timestamp:
        for date_timestamp in duplicate_date_timestamp:
            date = str(date_timestamp[0])
            timestamp = str(date_timestamp[1])
            files_with_duplicate_timestamp_dict[file, date].extend(['{} '.format(timestamp)])
        # files_with_duplicate_timestamp_dict[file].extend(['{} '.format(timestamp) for timestamp in duplicate_timestamp])

    # Locate and inform user about missing value in cells
    empty_cells_location = np.where(pd.isnull(df))
    unique_empty_cells_location = np.unique(empty_cells_location[0])
    # print(unique_empty_cells_location)
    if empty_cells_location[0].size != 0:
        for index in unique_empty_cells_location:
            empty_cells_timestamp_dict[file, df.iloc[index, date_column_index]].extend(['{} '. format(df.iloc[index,timestamp_column_index])])
        # empty_cells_timestamp_dict[file, date].extend(['{} '. format(df.iloc[i,timestamp_column_index]) for i in unique_empty_cells_location])
    # print(empty_cells_timestamp)
    
    
    df = insert_empty_slot(df, missing_minutes_dict, file)
    df = df.set_index(['Date','Timestamp'])
    collated_df = collated_df.combine_first(df).reindex(columns=cols)
    # files_with_duplicate_timestamp_dict.append((file, duplicate_timestamp))
    return collated_df

def combined_collation(path, window):
    # directory = collation['directory']
    directory = path
    vendor = os.path.basename(directory)
    os.chdir(directory)

    count = 0
    files_with_errors = []
    files_with_duplicate_timestamp_dict = defaultdict(list)
    missing_minutes_dict = defaultdict(list)
    empty_cells_timestamp_dict = defaultdict(list)

    
    
    collated_df = pd.DataFrame(columns=['Date','Timestamp'])
    collated_df['Date'] = pd.to_datetime(collated_df['Date'], format='%d/%m/%Y')
    collated_df = collated_df.set_index(['Date','Timestamp'])
                    
    for root,dirs,files in os.walk(directory):            
            for file in files[:]:
                if file.endswith('collated.xlsx') or file.endswith('collated.csv'):
                    files.pop(files.index(file))
                if file.endswith('.csv') or file.endswith('.xlsx'):
                    continue
                else:
                    files.pop(files.index(file))

            if len(files) == 0:
                window.write_event_value('NO FILES', None)
                return
            percentage_of_one_file = int(100/len(files))

            for file in files:
                count += 1
                progress = count * percentage_of_one_file
                window['-PROGRESS_BAR-'].update_bar(progress)
                if count == len(files):
                    window['-PROGRESS_BAR-'].update_bar(100)
                    window['-PROGRESS_TEXT-'].update('Saving collated file...')
                else:
                    window['-PROGRESS_TEXT-'].update(str(progress) + '% completed')
                # if file.endswith('collated.xlsx') or file.endswith('collated.csv'):
                #     continue
                
                if file.endswith('.csv'):
                    collated_df = csv_collation(file, collated_df, files_with_errors, files_with_duplicate_timestamp_dict, missing_minutes_dict, empty_cells_timestamp_dict)

                if file.endswith('.xlsx'):
                    collated_df = excel_collation(file, collated_df, files_with_errors, files_with_duplicate_timestamp_dict, missing_minutes_dict, empty_cells_timestamp_dict)
         
    collated_df.reset_index(inplace=True)
    collated_df['Date'] = pd.to_datetime(collated_df['Date'], format='%d/%m/%Y')
    collated_df = collated_df.sort_values(by=['Date','Timestamp'], ascending=[True,True])
    collated_df['Date'] = collated_df['Date'].dt.strftime('%d/%m/%Y')
    
    print(f'These are the files with errors: {files_with_errors}')
    if files_with_errors:
        window['-SUMMARY_LIST-'].update('These are the files with errors: \n', append=True)
    for file in files_with_errors:
        window['-ERROR_FILES_LIST-'].update(f'{file}\n', append=True)
        window['-SUMMARY_LIST-'].update(f'{file}\n', append=True)

    print('These are the files with duplicate timestamp: ')
    print(files_with_duplicate_timestamp_dict)
    if files_with_duplicate_timestamp_dict:
        window['-SUMMARY_LIST-'].update('\nThese are the files with duplicate timestamp detected: \n', append=True)
    for file, duplicate_timestamp in files_with_duplicate_timestamp_dict.items():
        # print(''.join(duplicate_timestamp))
        temp = ''.join(duplicate_timestamp)
        # print(f'{file}: {temp}')
        window['-DUPLICATE_TIMESTAMPS_LIST-'].update(f'{file}: Timestamp {temp}\n\n', append=True)
        window['-SUMMARY_LIST-'].update(f'{file}: Timestamp {temp}\n\n', append=True)
    
    print('These are the files with missing minutes: ')
    if missing_minutes_dict:
        window['-SUMMARY_LIST-'].update('\nThese are the files with missing minutes added: \n', append=True)
    for file, missing_minutes in missing_minutes_dict.items():
        temp = ' '.join(missing_minutes)
        # print(f'{file}: {temp}')
        window['-MISSING_MINUTES_LIST-'].update(f'{file}: Timestamp {temp}\n\n', append=True)
        window['-SUMMARY_LIST-'].update(f'{file}: Timestamp {temp}\n\n', append=True)
    
    print('These are the files with empty cells: ')
    if empty_cells_timestamp_dict:
        window['-SUMMARY_LIST-'].update('\nThese are the files with empty cells detected: \n', append=True)
    for file, empty_cells_timestamp in empty_cells_timestamp_dict.items():
        temp = ''.join(empty_cells_timestamp)
        # print(f'{file}: {temp}')
        window['-EMPTY_CELLS_LIST-'].update(f'{file}: Timestamp {temp}\n\n', append=True)
        window['-SUMMARY_LIST-'].update(f'{file}: Timestamp {temp}\n\n', append=True)


    current_date = get_current_date()
    collated_df.to_excel(f'{vendor}_{current_date}_collated.xlsx', index=False)
    # collated_df.to_csv(f'{vendor}_{current_date}_collated.csv', index=False)
    writer = pd.ExcelWriter(f'{vendor}_{current_date}_collated.xlsx',
                        engine='xlsxwriter',
                        date_format='d/m/yyyy')
    collated_df.to_excel(writer, sheet_name='Sheet1', index=False)
    worksheet = writer.sheets['Sheet1']
    worksheet.set_column('A:B', 15)
    writer.save()
    if not files_with_errors and not files_with_duplicate_timestamp_dict and not missing_minutes_dict and not empty_cells_timestamp_dict:
        window.write_event_value('COLLATION SUCCESSFUL', None)
    else:
        window.write_event_value('EXECUTION DONE', None)


# issues with excel file: date and time column, and format of date and time(2022-08-26 :23:59:00 PM)
# e2i: 01:50 chiller 41 has duplicate timestamp
# e2i: chiller 217 has no column header
# e2i: mixture of files within
# e2i: MSB has no column header
# e2i: date format changes when there is no slot name

# hybrid(some has missing slot name)
# missing data
# missing slot name and missing data
# missing slot name in first cell
# normal