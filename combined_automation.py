import os
import pandas as pd
import numpy as np
from collation import insert_empty_slot, get_current_date
from configuration import get_config
from collections import defaultdict


def yishun_collation(yishun_directory):
    directory = yishun_directory
    os.chdir(directory)
    collated_df = pd.DataFrame()
    for root,dirs,files in os.walk(directory):
        for file in files:
            # print(file)
            # Ignore collated file to avoid errors
            if file.endswith('collated.csv'):
                continue

            if file.endswith('.csv'):
                temp_df = pd.read_csv(file)
                # print(df)
                try:
                    temp_df.columns.get_loc('Timestamp')
                except:
                    temp_df = temp_df.rename(columns={'Time': 'Timestamp'})
                print(temp_df.head(5))
                # print(df['Timestamp'])
                for i in range(len(temp_df)):
                    temp = temp_df['Timestamp'][i].split(':')
                    hour = str('%02d' % int(temp[0])) + ':'
                    minute = str('%02d' % int(temp[1]))
                    temp_df['Timestamp'][i] = hour + minute
                    # print(df['Timestamp'])
                print(temp_df)
                df = insert_empty_slot(df)
                collated_df = pd.concat([collated_df, df], axis=0)
    current_date = get_current_date()
    collated_df.to_excel(f'{current_date}_collated.xlsx', index=False)

def e2i_redo_collation():
    import os
    import pandas as pd
    files_with_errors = []
    directory = "C:\\Users\\tengwei.goh\\Desktop\\Sample Data\\e2i_test"
    os.chdir(directory)
    collated_df = pd.DataFrame(columns=['Date','Timestamp'])
    temp_df = pd.DataFrame()
    count = 0
    cols_to_use = ['Date', 'Timestamp']
    # collated_df = pd.DataFrame()
    for root,dirs,files in os.walk(directory):
        for file in files:
            count += 1
            # print(file)
            # Ignore collated file to avoid errors
            if file.endswith('collated.csv'):
                continue

            if file.endswith('.csv'):
                print(file)
                # df = pd.read_csv('CET WEST Greenmark Data - Chiller 42-2022.csv')
                f = open(file, 'r')
                result = []
                for l in f.readlines():
                    vals = [l for l in l.split('#') if l]
                    index = vals[0]
                    result.append(index)
                ...
                # fill dataframe
                f.close()

                for i in range(len(result)):
                    result[i] = result[i].replace('\n','')
                    # result = result.split(',')

                temp = result[1:]

                for i in range(len(temp)):
                    temp[i] = temp[i].split(',')
                df = pd.DataFrame(temp[1:],columns=temp[0])
                # df.head()
                try:
                    df.columns.get_loc('Timestamp')
                except:
                    df = df.rename(columns={'Time': 'Timestamp'})
                # print(file)
                # print(df.head(5))
                for i in range(len(df)):
                    temp = df['Timestamp'][i].split(':')
                    hour = str('%02d' % int(temp[0])) + ':'
                    minute = str('%02d' % int(temp[1]))
                    df['Timestamp'][i] = hour + minute

                    
                #TODO: NEED HELP FROM HERE
                if count > 1:
                    cols_to_use = df.columns.difference(temp_df.columns).tolist()
                    # cols_to_use += temp_cols
                    print(cols_to_use)
                    collated_df.reindex(columns=cols_to_use)
                    print(collated_df.columns)
                # collated_df = pd.merge(collated_df, df[cols_to_use], left_index=True, right_index=True, how='outer')
                try:
                    collated_df = pd.merge(collated_df, df, on=cols_to_use, how='outer', suffixes=('', '_test'))
                except:
                    collated_df = pd.merge(collated_df, df, on=['Date','Timestamp'], how='outer')
                print(collated_df.columns)
                to_drop = [x for x in collated_df if x.endswith('_test')]
                print(to_drop)
                collated_df.drop(to_drop, axis=1, inplace=True)
    print(collated_df.tail())
    collated_df.to_csv('collated.csv', index=False)

def e2i_finally_fixed():
    import os
    import pandas as pd
    files_with_errors = []
    directory = "C:\\Users\\tengwei.goh\\Desktop\\Sample Data\\e2i_test"
    os.chdir(directory)
    collated_df = pd.DataFrame(columns=['Date','Timestamp'])
    collated_df = collated_df.set_index(['Date','Timestamp'])
    count = 0

    for root,dirs,files in os.walk(directory):
        for file in files:
            count += 1
            # print(file)
            # Ignore collated file to avoid errors
            if file.endswith('collated.csv'):
                continue

            if file.endswith('.csv'):
                # print(file)
                # df = pd.read_csv('CET WEST Greenmark Data - Chiller 42-2022.csv')
                f = open(file, 'r')
                result = []
                for l in f.readlines():
                    vals = [l for l in l.split('#') if l]
                    index = vals[0]
                    result.append(index)
                ...
                # fill dataframe
                f.close()

                for i in range(len(result)):
                    result[i] = result[i].replace('\n','')
                    # result = result.split(',')

                temp = result[1:]

                for i in range(len(temp)):
                    temp[i] = temp[i].split(',')
                df = pd.DataFrame(temp[1:],columns=temp[0])
                try:
                    df.columns.get_loc('Timestamp')
                except:
                    df = df.rename(columns={'Time': 'Timestamp'})
                
                for i in range(len(df)):
                    temp = df['Timestamp'][i].split(':')
                    hour = str('%02d' % int(temp[0])) + ':'
                    minute = str('%02d' % int(temp[1]))
                    df['Timestamp'][i] = hour + minute

                #TODO: FINALLY FIXED
                df = df[df['Timestamp'].notna()]
                df = insert_empty_slot(df)
                df = df.set_index(['Date','Timestamp'])
                collated_df = collated_df.combine_first(df)
                
    collated_df.sort_values(by=['Date','Timestamp'], inplace=True)
    collated_df.to_csv('collated.csv')

def KAL_redo_collation():
    import pandas as pd
    import os
    directory = "C:\\Users\\tengwei.goh\\Desktop\\Sample Data\\KAL_test"
    os.chdir(directory)
    files_with_errors = []
    collated_df = pd.DataFrame(columns=['Date','Timestamp'])
    collated_df = collated_df.set_index(['Date','Timestamp'])
                    
    for root,dirs,files in os.walk(directory):
            for file in files:
                if file.endswith('collated.xlsx'):
                    continue
                    
                if file.endswith('.xlsx'):
                    try:
                        df = pd.read_excel(file, sheet_name=0)
                        df = df.reset_index(drop=True)
                        df.columns = df.iloc[7-2]
                        df = df.drop(df.index[:7-1])
                        df = df.reset_index()
                        df = df.dropna(how='all')
                        df.drop(columns=['index'], axis=1, inplace=True)
                        print(file)
                        try:
                            df.columns.get_loc('Timestamp')
                        except:
                            df = df.rename(columns={'Time': 'Timestamp'})

                        df['date and time'] = df['date and time'].str.split(' ')

                        for i in range(len(df['date and time'])):
                            try:
                                df['Date'] = df['date and time'][0][0]
                                df['Timestamp'][i] = df['date and time'][i][1][1:6]
                                
                            except:
                                pass
                            
                        df.drop(columns=['date and time'], axis=1, inplace=True)
                        # NEED TO DROP EMPTY COLUMN NAMES to prevent error
                        df = df.loc[:, df.columns.notna()]
                        df = df[df['Timestamp'].notna()]
                        df = insert_empty_slot(df)
                        df = df.set_index(['Date','Timestamp'])
                        collated_df = collated_df.combine_first(df)
                        collated_df = collated_df.rename_axis(None, axis=1)
                    except Exception as e:
                        print(e)
                        files_with_errors.append(file)
                        continue

                    
    collated_df.sort_values(by=['Date','Timestamp'], inplace=True, ascending=True)
    print(f'These are the files with errors: {files_with_errors}')
    # current_date = get_current_date()
    collated_df.to_excel('collated.xlsx')

def csv_collation(file, collated_df, files_with_errors, files_with_duplicate_timestamp, date_format_list, missing_minutes_dict, empty_cells_timestamp_dict):
    try:
        file_lines = []
        # Open the file in read mode and read the lines
        with open(file, 'r') as f:
            for line in f:
                file_lines.append(line.strip())

        # Split the lines into words, remove empty strings caused by additional columns and add to list
        for i in range(len(file_lines)):
            file_lines[i] = file_lines[i].strip(',').split(',')
            # print(file_lines[i])
            # file_lines[i] = [i for i in file_lines[i] if i != '']

        if len(file_lines[0]) < 2:
            df = pd.DataFrame(file_lines[2:],columns=file_lines[1])
        else:
            df = pd.DataFrame(file_lines[1:],columns=file_lines[0])
        # Read the cleaned list into a Pandas DataFrame
        # df = pd.DataFrame(file_lines[1:],columns=file_lines[0])
        # print(df.head())
        
        try:
            df.columns.get_loc('Timestamp')
        except:
            df = df.rename(columns={'Time': 'Timestamp'})

        df['Timestamp'] = df['Timestamp'].astype(str)
        for i in range(len(df)):
            temp = df['Timestamp'][i].split(':')
            hour = str('%02d' % int(temp[0])) + ':'
            minute = str('%02d' % int(temp[1]))
            df['Timestamp'][i] = hour + minute

        # From here onwards, its the same as excel collation 
        return csv_excel_df_manipulation(file, collated_df, df, files_with_duplicate_timestamp, date_format_list, missing_minutes_dict, empty_cells_timestamp_dict)
        df = df.replace(r'^\s*$', np.nan, regex=True)
        df = df.replace('None', np.nan, regex=True)
        df = df[df['Timestamp'].notna()]
        df = df.reset_index(drop=True)   

        for date_format in date_format_list:
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
        date = df.Date[0]

        # NEED TO DROP EMPTY COLUMN NAMES AND CELLS to prevent error
        df = df.loc[:, df.columns.notna()]
        df = df[df['Timestamp'].notna()]

        # Tracking of duplicate timestamp
        duplicate_df = df[df.duplicated(subset=['Timestamp'])]
        duplicate_timestamp = duplicate_df['Timestamp'].tolist()
        duplicate_timestamp = [str(date) +' {} '.format(timestamp) for timestamp in duplicate_timestamp]

        # Locate and inform user about missing value in cells
        empty_cells_location = np.where(pd.isnull(df))
        timestamp_column_index = df.columns.get_loc('Timestamp')
        empty_cells_timestamp[date].extend([df.iloc[i,timestamp_column_index] for i,j in zip(*empty_cells_location)])
        # print(empty_cells_timestamp)
        
        
        df = insert_empty_slot(df, missing_minutes_dict)
        df = df.set_index(['Date','Timestamp'])
        # print(df.head())
        collated_df = collated_df.combine_first(df).reindex(columns=cols)
        files_with_duplicate_timestamp.append((file, duplicate_timestamp))
        return collated_df
    except Exception as e:
        print(e)
        files_with_errors.append(file)
        return collated_df
    # try:
    #     f = open(file, 'r')
    #     result = []
    #     for l in f.readlines():
    #         vals = [l for l in l.split('#') if l]
    #         index = vals[0]
    #         result.append(index)
    #     ...
    #     # fill dataframe
    #     f.close()

    #     for i in range(len(result)):
    #         result[i] = result[i].replace('\n','')
    #         # result = result.split(',')
    #         # print(result[i])

    #     temp = result[1:]
    #     # print(temp[0])
    #     for i in range(len(temp)):
    #         temp[i] = temp[i].split(',')
    #     df = pd.DataFrame(temp[1:],columns=temp[0])
    #     try:
    #         df.columns.get_loc('Timestamp')
    #     except:
    #         df = df.rename(columns={'Time': 'Timestamp'})

    #     df = df.replace(r'^\s*$', np.nan, regex=True)
    #     df = df[df['Timestamp'].notna()]
    #     df = df.reset_index(drop=True)

    #     try:
    #         df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%y')
    #     except:
    #         df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')
        
    #     for i in range(len(df)):
    #         temp = df['Timestamp'][i].split(':')
    #         hour = str('%02d' % int(temp[0])) + ':'
    #         minute = str('%02d' % int(temp[1]))
    #         df['Timestamp'][i] = hour + minute
    #     # print(df.head())
    #     #TODO: FINALLY FIXED
    #     # Need these columns to keep original column order
    #     cols = collated_df.columns.append(df.columns).unique()
    #     cols = cols.drop(['Date','Timestamp'])

    #     # NEED TO DROP EMPTY COLUMN NAMES AND CELLS to prevent error
    #     df = df.loc[:, df.columns.notna()]
    #     df = df[df['Timestamp'].notna()]
    #     # print(df.head())
    #     df = insert_empty_slot(df)
    #     # print(df.head())
    #     df = df.set_index(['Date','Timestamp'])
    #     # print(df.head())
    #     collated_df = collated_df.combine_first(df).reindex(columns=cols)
    #     return collated_df, files_with_errors
    # except:
    #     try:
    #         file_lines = []
    #         # Open the file in read mode and read the lines
    #         with open(file, 'r') as f:
    #             for line in f:
    #                 file_lines.append(line.strip())

    #         # Split the lines into words, remove empty strings caused by additional columns and add to list
    #         for i in range(len(file_lines)):
    #             file_lines[i] = file_lines[i].split(',')
    #             file_lines[i] = [i for i in file_lines[i] if i != '']

    #         # Read the cleaned list into a Pandas DataFrame
    #         df = pd.DataFrame(file_lines[1:],columns=file_lines[0])
    #         print(df.head())
    #         # df = pd.read_csv(file)
    #         # print(df.columns)
    #         # df = df.reset_index(drop=True)
    #         # f = open(file, 'r')
    #         # result = []
    #         # for l in f.readlines():
    #         #     vals = [l for l in l.split('#') if l]
    #         #     index = vals[0]
    #         #     # print(index)
    #         #     result.append(index)
    #         # ...
    #         # # fill dataframe
    #         # f.close()
    #         # # print(result)
    #         # for i in range(len(result)):
    #         #     result[i] = result[i].replace('\n','')
    #         #     # result = result.split(',')

    #         # cols = result[0].split(',')
    #         # temp = result[1:]
    #         # # print(temp[0])
    #         # for i in range(len(temp)):
    #         #     temp[i] = temp[i].split(',')
    #         # df = pd.DataFrame(temp[1:],columns=cols)
    #         # # print(df.head())
    #         try:
    #             df.columns.get_loc('Timestamp')
    #         except:
    #             df = df.rename(columns={'Time': 'Timestamp'})

    #         df = df.replace(r'^\s*$', np.nan, regex=True)
    #         df = df.replace('None', np.nan, regex=True)
    #         df = df[df['Timestamp'].notna()]
    #         df = df.reset_index(drop=True)   
                     
    #         try:
    #             df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%y')
    #         except:
    #             df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')
    #         # print(df.Date)
    #         # for i in range(len(df)):
    #         #     temp = df['Date'][i].split('/')
    #         #     day = str('%02d' % int(temp[0])) + '/'
    #         #     month = str('%02d' % int(temp[1])) + '/'
    #         #     year = str('%04d' % int(temp[2]))
    #         #     df['Date'][i] = day + month + year
    #         # print(df.Date)
    #         df['Timestamp'] = df['Timestamp'].astype(str)
    #         # print(df['Timestamp'])
    #         for i in range(len(df)):
    #             temp = df['Timestamp'][i].split(':')
    #             hour = str('%02d' % int(temp[0])) + ':'
    #             minute = str('%02d' % int(temp[1]))
    #             df['Timestamp'][i] = hour + minute
    #             # print(df['Timestamp'])

    #         # Need these columns to keep original column order
    #         cols = collated_df.columns.append(df.columns).unique()
    #         cols = cols.drop(['Date','Timestamp'])

    #         # NEED TO DROP EMPTY COLUMN NAMES AND CELLS to prevent error
    #         df = df.loc[:, df.columns.notna()]
    #         df = df[df['Timestamp'].notna()]
    #         df = insert_empty_slot(df)
    #         # print(df.Date)
    #         df = df.set_index(['Date','Timestamp'])
    #         # print(df.head())
    #         collated_df = collated_df.combine_first(df).reindex(columns=cols)
    #         return collated_df, files_with_errors
    #     except Exception as e:
    #         print(e)
    #         files_with_errors.append(file)
    #         return collated_df, files_with_errors

def excel_collation(file, collated_df, files_with_errors, files_with_duplicate_timestamp, date_format_list, missing_minutes_dict, empty_cells_timestamp_dict):
    try:
        date_and_time_format = ''
        date_and_time_column_name_list = ['Date and Time', 'date and time', 'DATE AND TIME',
                                        'Date & Time',  'date & time', 'DATE & TIME',
                                        'Date_Time', 'date_time', 'DATE_TIME',
                                        'Date Time', 'date time', 'DATE TIME'
                                        ]
        df = pd.read_excel(file, sheet_name=0)
        df = df.reset_index(drop=True)
        # Able to locate column names IF previous rows are all empty
        df.dropna(inplace = True, axis=0, thresh=5)
        df = df.replace(r'^\s*$', np.nan, regex=True)
        df = df.replace('None', np.nan, regex=True)
        df.columns = df.iloc[0]
        df = df.drop(df.index[0])

        # df.columns = df.iloc[int(excel_column_header_row)-2]
        # df = df.drop(df.index[:int(excel_column_header_row)-1])
        df = df.reset_index()
        df = df.dropna(how='all')
        df.drop(columns=['index'], axis=1, inplace=True)
        print(file)
        try:
            df.columns.get_loc('Timestamp')
        except:
            df = df.rename(columns={'Time': 'Timestamp'})

        for date_time in date_and_time_column_name_list:
            try:
                df[date_time] = df[date_time].str.split(' ')
                date_and_time_format = date_time
                break
            except:
                pass

        for i in range(len(df[date_and_time_format])):
            try:
                df['Date'] = df[date_and_time_format][0][0]
                temp = df[date_and_time_format][i][1].split(':')
                # Ensure that there are no empty strings in the list that will cause error
                temp = [i for i in temp if i != '']
                hour = str('%02d' % int(temp[0])) + ':'
                minute = str('%02d' % int(temp[1]))
                df['Timestamp'][i] = hour + minute
            except:
                pass
        df.drop(columns=[date_and_time_format], axis=1, inplace=True)

        # From here onwards, its the same as csv collation
        return csv_excel_df_manipulation(file, collated_df, df, files_with_duplicate_timestamp, date_format_list, missing_minutes_dict, empty_cells_timestamp_dict)
        for date_format in date_format_list:
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

        # NEED TO DROP EMPTY COLUMN NAMES AND CELLS to prevent error
        df = df.loc[:, df.columns.notna()]
        df = df[df['Timestamp'].notna()]

        # Tracking of duplicate timestamp
        duplicate_df = df[df.duplicated(subset=['Timestamp'])]
        print(duplicate_df)
        duplicate_timestamp = duplicate_df['Timestamp'].tolist()
        # print(duplicate_timestamp)
        duplicate_timestamp = [str(df.Date[0]) +' {} '.format(timestamp) for timestamp in duplicate_timestamp]

        # Locate and inform user about missing value in cells
        empty_cells_location = np.where(pd.isnull(df))
        date_column_index, timestamp_column_index = df.columns.get_loc('Date'), df.columns.get_loc('Timestamp')
        empty_cells_timestamp_dict[df.Date[0]].extend([(df.iloc[i,date_column_index], df.iloc[i,timestamp_column_index]) for i,j in zip(*empty_cells_location)])
        # print(empty_cells_timestamp)

        
        df = insert_empty_slot(df, missing_minutes_dict)
        df = df.set_index(['Date','Timestamp'])
        collated_df = collated_df.combine_first(df).reindex(columns=cols)
        collated_df = collated_df.rename_axis(None, axis=1)
        files_with_duplicate_timestamp.append((file, duplicate_timestamp))
        return collated_df 
    except Exception as e:
        print(e)
        files_with_errors.append(file)
        return collated_df

def csv_excel_df_manipulation(file, collated_df, df, files_with_duplicate_timestamp, date_format_list, missing_minutes_dict, empty_cells_timestamp_dict):
    df = df.replace(r'^\s*$', np.nan, regex=True)
    df = df.replace('None', np.nan, regex=True)
    df = df[df['Timestamp'].notna()]
    df = df.reset_index(drop=True)   

    for date_format in date_format_list:
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
    date = df.Date[0]

    # NEED TO DROP EMPTY COLUMN NAMES AND CELLS to prevent error
    df = df.loc[:, df.columns.notna()]
    df = df[df['Timestamp'].notna()]

    # Tracking of duplicate timestamp
    duplicate_df = df[df.duplicated(subset=['Timestamp'])]
    duplicate_timestamp = duplicate_df['Timestamp'].tolist()
    duplicate_timestamp = [str(date) +' {} '.format(timestamp) for timestamp in duplicate_timestamp]

    # Locate and inform user about missing value in cells
    empty_cells_location = np.where(pd.isnull(df))
    timestamp_column_index = df.columns.get_loc('Timestamp')
    empty_cells_timestamp_dict[date].extend([df.iloc[i,timestamp_column_index] for i,j in zip(*empty_cells_location)])
    # print(empty_cells_timestamp)
    
    
    df = insert_empty_slot(df, missing_minutes_dict)
    df = df.set_index(['Date','Timestamp'])
    collated_df = collated_df.combine_first(df).reindex(columns=cols)
    files_with_duplicate_timestamp.append((file, duplicate_timestamp))
    return collated_df

def combined_collation(collation, window):
    directory = collation['directory']
    vendor = os.path.basename(directory)
    os.chdir(directory)

    count = 0
    files_with_errors = []
    files_with_duplicate_timestamp = []
    missing_minutes_dict = defaultdict(list)
    empty_cells_timestamp = []

    date_format_list = ['%d/%m/%Y', '%d/%m/%y', 
                        '%d-%m-%Y', '%d-%m-%y', 
                        '%d.%m.%Y', '%d.%m.%y', 
                        '%d %m %Y', '%d %m %y',
                        '%d%m%Y', '%d%m%y',
                        '%Y-%m-%d', '%y-%m-%d',
                        '%Y/%m/%d', '%y/%m/%d']
    collated_df = pd.DataFrame(columns=['Date','Timestamp'])
    collated_df['Date'] = pd.to_datetime(collated_df['Date'], format='%d/%m/%Y')
    collated_df = collated_df.set_index(['Date','Timestamp'])
                    
    for root,dirs,files in os.walk(directory):            
            for file in files[:]:
                if file.endswith('collated.xlsx') or file.endswith('collated.csv'):
                    files.pop(files.index(file))

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
                    collated_df = csv_collation(file, collated_df, files_with_errors, files_with_duplicate_timestamp, date_format_list, missing_minutes_dict, empty_cells_timestamp)

                if file.endswith('.xlsx'):
                    collated_df = excel_collation(file, collated_df, files_with_errors, files_with_duplicate_timestamp, date_format_list, missing_minutes_dict, empty_cells_timestamp)

                if not files_with_duplicate_timestamp:
                    continue 
                
                if files_with_duplicate_timestamp[-1][1] == []:
                    files_with_duplicate_timestamp.pop()
    print(missing_minutes_dict)
    collated_df.reset_index(inplace=True)
    collated_df = collated_df.sort_values(by=['Date','Timestamp'], ascending=True)
    # collated_df['Date'] = collated_df['Date'].dt.strftime('%d/%m/%Y')
    # collated_df = collated_df.sort_index(axis=1, ascending=True)
    print(f'These are the files with errors: {files_with_errors}')
    print('These are the files with duplicate timestamp: ')
    for file, duplicate_timestamp in files_with_duplicate_timestamp:
        temp = ''.join(duplicate_timestamp)
        print(f'{file}: {temp}')
    current_date = get_current_date()
    collated_df.to_excel(f'{vendor}_{current_date}_collated.xlsx', index=False)
    # collated_df.to_csv(f'{vendor}_{current_date}_collated.csv')
    writer = pd.ExcelWriter(f'{vendor}_{current_date}_collated.xlsx',
                        engine='xlsxwriter',
                        date_format='d/m/yyyy')
    collated_df.to_excel(writer, sheet_name='Sheet1', index=False)
    worksheet = writer.sheets['Sheet1']
    worksheet.set_column('A:B', 15)
    writer.save()
    window.write_event_value('EXECUTION DONE', None)

def combined_collation(collation):
    directory = collation['directory']
    vendor = os.path.basename(directory)
    os.chdir(directory)

    count = 0
    files_with_errors = []
    files_with_duplicate_timestamp = []
    missing_minutes_dict = defaultdict(list)
    empty_cells_timestamp_dict = defaultdict(list)

    date_format_list = ['%d/%m/%Y', '%d/%m/%y', 
                        '%d-%m-%Y', '%d-%m-%y', 
                        '%d.%m.%Y', '%d.%m.%y', 
                        '%d %m %Y', '%d %m %y',
                        '%d%m%Y', '%d%m%y',
                        '%Y-%m-%d', '%y-%m-%d',
                        '%Y/%m/%d', '%y/%m/%d']
    collated_df = pd.DataFrame(columns=['Date','Timestamp'])
    collated_df['Date'] = pd.to_datetime(collated_df['Date'], format='%d/%m/%Y')
    collated_df = collated_df.set_index(['Date','Timestamp'])
                    
    for root,dirs,files in os.walk(directory):            
            for file in files[:]:
                if file.endswith('collated.xlsx') or file.endswith('collated.csv'):
                    files.pop(files.index(file))

            for file in files:
                if file.endswith('.csv'):
                    collated_df = csv_collation(file, collated_df, files_with_errors, files_with_duplicate_timestamp, date_format_list, missing_minutes_dict, empty_cells_timestamp_dict)

                if file.endswith('.xlsx'):
                    collated_df = excel_collation(file, collated_df, files_with_errors, files_with_duplicate_timestamp, date_format_list, missing_minutes_dict, empty_cells_timestamp_dict)

                if not files_with_duplicate_timestamp:
                    continue 
                
                if files_with_duplicate_timestamp[-1][1] == []:
                    files_with_duplicate_timestamp.pop()
    print(missing_minutes_dict)
    print(empty_cells_timestamp_dict)
    collated_df.reset_index(inplace=True)
    collated_df = collated_df.sort_values(by=['Date','Timestamp'], ascending=True)
    # collated_df['Date'] = collated_df['Date'].dt.strftime('%d/%m/%Y')
    # collated_df = collated_df.sort_index(axis=1, ascending=True)
    print(f'These are the files with errors: {files_with_errors}')
    print('These are the files with duplicate timestamp: ')
    for file, duplicate_timestamp in files_with_duplicate_timestamp:
        temp = ''.join(duplicate_timestamp)
        print(f'{file}: {temp}')
    current_date = get_current_date()
    collated_df.to_excel(f'{vendor}_{current_date}_collated.xlsx', index=False)
    # collated_df.to_csv(f'{vendor}_{current_date}_collated.csv')
    writer = pd.ExcelWriter(f'{vendor}_{current_date}_collated.xlsx',
                        engine='xlsxwriter',
                        date_format='d/m/yyyy')
    collated_df.to_excel(writer, sheet_name='Sheet1', index=False)
    worksheet = writer.sheets['Sheet1']
    worksheet.set_column('A:B', 15)
    writer.save()

config = get_config()
combined_collation(config.collation)

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