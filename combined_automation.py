import os
import pandas as pd
import numpy as np
from collation import *
from configuration import *

def KAL_collation(KAL_directory):
    directory = KAL_directory
    # directory = os.path.join("c:\\",path)
    # print(directory)
    os.chdir(directory)
    collated_df = pd.DataFrame()
    for root,dirs,files in os.walk(directory):
        for file in files:
            
            df = pd.read_excel(file, sheet_name=0)
            # print(df.head(6))
            df = df.reset_index(drop=True)
            df.columns = df.iloc[5]
            df = df.drop(df.index[:6])
            df = df.reset_index()
            df = df.dropna(how='all')
            df.drop(columns=['index', 'Date', 'Time'], axis=1, inplace=True)

            df['date and time'] = df['date and time'].str.split(' ')
            df["Date"] = ""
            df["Timestamp"] = ""
            df['Date'] = df['date and time'][0][0]

            for i in range(len(df['date and time'])):
                try:
                    df['Timestamp'][i] = df['date and time'][i][1][1:6]
                except:
                    pass
            print(df['Date'].head())
            print(df['Timestamp'].head())

            df = df.sort_values(by=['Timestamp'])

            cols_to_move = ['Date','Timestamp']
            df = df[ cols_to_move + [ col for col in df.columns if col not in cols_to_move ] ]
            df.drop(columns=['date and time'], axis=1, inplace=True)
            df['Timestamp'].replace('', np.nan, inplace=True)
            df.dropna(subset=['Timestamp'], inplace=True)
            df = insert_empty_slot_1(df)
            collated_df = pd.concat([collated_df, df], axis=0)

    collated_df.to_excel('KAL_collated.xlsx', index=False)

def KAL_collation_2(KAL_directory, column_header_row):
    directory = KAL_directory
    # directory = os.path.join("c:\\",path)
    # print(directory)
    os.chdir(directory)
    collated_df = pd.DataFrame()
    for root,dirs,files in os.walk(directory):
        for file in files:
            if file.startswith('collated'):
                continue
            try:
                df = pd.read_excel(file, sheet_name=0)
                # print(df.head(6))
                df = df.reset_index(drop=True)
                df.columns = df.iloc[column_header_row-2]
                df = df.drop(df.index[:column_header_row-1])
                df = df.reset_index()
                df = df.dropna(how='all')
                df.drop(columns=['index'], axis=1, inplace=True)

                try:
                    df.columns.get_loc('Timestamp')
                except:
                    df = df.rename(columns={'Time': 'Timestamp'})
                
                df['date and time'] = df['date and time'].str.split(' ')
                # df["Date"] = ""
                # df["Timestamp"] = ""
                # df['Date'] = df['date and time'][0][0]

                for i in range(len(df['date and time'])):
                    try:
                        df['Date'] = df['date and time'][0][0]
                        df['Timestamp'][i] = df['date and time'][i][1][1:6]
                    except:
                        pass
                print(df['Date'].head())
                print(df['Timestamp'].head())

                df = df.sort_values(by=['Timestamp'])

                cols_to_move = ['Date','Timestamp']
                df = df[ cols_to_move + [ col for col in df.columns if col not in cols_to_move ] ]
                df.drop(columns=['date and time'], axis=1, inplace=True)
                df['Timestamp'].replace('', np.nan, inplace=True)
                df.dropna(subset=['Timestamp'], inplace=True)
                df = insert_empty_slot_1(df)
                collated_df = pd.concat([collated_df, df], axis=0)
            except:
                print(file)
                pass

    collated_df.to_excel('collated.xlsx', index=False)

def e2i_collation(e2i_directory):
    # path = os.getcwd()
    # directory = os.path.join("c:\\",path)
    # print(directory)
    directory = e2i_directory
    os.chdir(directory)
    collated_df = pd.DataFrame()
    for root,dirs,files in os.walk(directory):
        for file in files:
            # print(file)
            # Ignore collated file to avoid errors
            if file.startswith('CET'):
                try:
                    # df = pd.read_csv('CET WEST Greenmark Data - Chiller 42-2022.csv')
                    df = pd.read_csv(file)
                    cols = list(df.iloc[0].name)
                    to_drop = df.head(0)
                    df = df.drop(to_drop, axis=1)
                    df = df.reset_index()
                    df.columns = cols
                    df = df.drop(df.index[0])
                    df = df.reset_index()
                    df = df.drop(df.columns[0], axis=1)
                    try:
                        df.columns.get_loc('Timestamp')
                    except:
                        df = df.rename(columns={'Time': 'Timestamp'})

                    for i in range(len(df)):
                        temp = df['Timestamp'][i].split(':')
                        hour = str('%02d' % int(temp[0])) + ':'
                        minute = str('%02d' % int(temp[1]))
                        df['Timestamp'][i] = hour + minute
                    df = insert_empty_slot_1(df)
                    collated_df = pd.concat([collated_df, df], axis=0)
                except:
                    print(file)
                    pass
    collated_df.to_excel('e2i_collated.xlsx', index=False)

def e2i_collation_2(e2i_directory):
    directory = e2i_directory
    os.chdir(directory)
    collated_df = pd.DataFrame()
    for root,dirs,files in os.walk(directory):
        for file in files:
            # print(file)
            # Ignore collated file to avoid errors
            if file.endswith('.csv'):
                try:
                    # df = pd.read_csv('CET WEST Greenmark Data - Chiller 42-2022.csv')
                    f = open('CET WEST Greenmark Data - Chiller 42-2022.csv', 'r')
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
                    df.head()
                    try:
                        df.columns.get_loc('Timestamp')
                    except:
                        df = df.rename(columns={'Time': 'Timestamp'})

                    for i in range(len(df)):
                        temp = df['Timestamp'][i].split(':')
                        hour = str('%02d' % int(temp[0])) + ':'
                        minute = str('%02d' % int(temp[1]))
                        df['Timestamp'][i] = hour + minute
                    df = insert_empty_slot_1(df)
                    collated_df = pd.concat([collated_df, df], axis=0)

                except:
                    print(file)
                    pass
    collated_df.to_excel('e2i_collated_2.xlsx', index=False)

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
                df = insert_empty_slot_1(df)
                collated_df = pd.concat([collated_df, df], axis=0)
    current_date = get_current_date()
    collated_df.to_excel(f'{current_date}_collated.xlsx', index=False)

def one_for_all_collation(user_directory, vendor, excel_column_header_row):
    files_with_errors = []
    directory = user_directory
    os.chdir(directory)
    collated_df = pd.DataFrame(columns=['Date','Timestamp'])
    # collated_df = pd.DataFrame()
    for root,dirs,files in os.walk(directory):
        for file in files:
            # print(file)
            # Ignore collated file to avoid errors
            if file.endswith('collated.csv'):
                continue

            if file.endswith('.csv'):
                print(file)
                try:
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
                    # cols_to_use = df.columns.difference(collated_df.columns)
                    # print(cols_to_use)
                    # collated_df = pd.merge(collated_df, df[cols_to_use], left_index=True, right_index=True, how='outer')
                    collated_df = pd.merge(collated_df, df, on=['Date','Timestamp'], how='outer', suffixes=('', '_test'))
                    # print(collated_df)
                    to_drop = [x for x in collated_df if x.endswith('_test')]
                    print(to_drop)
                    collated_df.drop(to_drop, axis=1, inplace=True)
                    # collated_df = collated_df.sort_values(by=['Date','Timestamp'], ascending=True)
                    # df = insert_empty_slot_1(df)
                    # collated_df = pd.concat([collated_df, df], ignore_index=False)
                except Exception as e:
                        print(e)
                        try:
                            df = pd.read_csv(file, index_col=False)
                            # print(df)
                            try:
                                df.columns.get_loc('Timestamp')
                            except:
                                df = df.rename(columns={'Time': 'Timestamp'})
                            # print(df.head(5))
                            # print(df['Timestamp'])
                            for i in range(len(df)):
                                temp = df['Timestamp'][i].split(':')
                                hour = str('%02d' % int(temp[0])) + ':'
                                minute = str('%02d' % int(temp[1]))
                                df['Timestamp'][i] = hour + minute
                                # print(df['Timestamp'])
                            # print(df)
                            df = insert_empty_slot_1(df)
                            collated_df = pd.concat([collated_df, df], axis=0)
                        except Exception as e:
                            files_with_errors.append((file, e))
                            pass
            
            if file.endswith('.xlsx'):
                try:
                    date_and_time = ''
                    date_and_time_column_name_list = ['Date and Time', 'date and time', 'DATE AND TIME',
                                                      'Date & Time',  'date & time', 'DATE & TIME',
                                                      'Date_Time', 'date_time', 'DATE_TIME',
                                                      'Date Time', 'date time', 'DATE TIME'
                                                       ]
                    df = pd.read_excel(file, sheet_name=0)
                    # print(df.head(6))
                    df = df.reset_index(drop=True)
                    df.columns = df.iloc[int(excel_column_header_row)-2]
                    df = df.drop(df.index[:int(excel_column_header_row)-1])
                    df = df.reset_index()
                    df = df.dropna(how='all')
                    df.drop(columns=['index'], axis=1, inplace=True)

                    try:
                        df.columns.get_loc('Timestamp')
                    except:
                        df = df.rename(columns={'Time': 'Timestamp'})
                    
                    for date_time in date_and_time_column_name_list:
                        try:
                            df[date_time] = df[date_time].str.split(' ')
                            date_and_time = date_time
                            break
                        except:
                            pass
                    # df['date and time'] = df['date and time'].str.split(' ')
                    # df["Date"] = ""
                    # df["Timestamp"] = ""
                    # df['Date'] = df['date and time'][0][0]

                    for i in range(len(df[date_and_time])):
                        try:
                            df['Date'] = df[date_and_time][0][0]
                            df['Timestamp'][i] = df[date_and_time][i][1][1:6]
                        except:
                            pass
                    print(df['Date'].head())
                    print(df['Timestamp'].head())

                    df = df.sort_values(by=['Timestamp'])

                    cols_to_move = ['Date','Timestamp']
                    df = df[ cols_to_move + [ col for col in df.columns if col not in cols_to_move ] ]
                    df.drop(columns=[date_and_time], axis=1, inplace=True)
                    df['Timestamp'].replace('', np.nan, inplace=True)
                    df.dropna(subset=['Timestamp'], inplace=True)
                    df = insert_empty_slot_1(df)
                    collated_df = pd.concat([collated_df, df], axis=0)
                except Exception as e:
                    files_with_errors.append((file, e))
                    pass
    
    # for col in collated_df:
    #     if col.endswith('_x'):
    #         collated_df.rename(columns={col:col.rstrip('_x')}, inplace=True)
    collated_df = collated_df.sort_values(by=['Date','Timestamp'], ascending=True)
    print(f'These are the files with errors: {files_with_errors}')
    current_date = get_current_date()
    collated_df.to_excel(f'{vendor}_{current_date}_collated.xlsx', index=False)

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
                df = insert_empty_slot_1(df)
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
                        df = insert_empty_slot_1(df)
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

# config = get_config()
# # e2i_collation(config.collation['directory'])
# one_for_all_collation(config.collation['directory'], config.collation['vendor'], config.collation['excel_column_header_row'])

# issues with excel file: date and time column, and format of date and time(2022-08-26 :23:59:00 PM)
# e2i: 01:50 chiller 41 has duplicate timestamp
# e2i: chiller 217 has no column header
# e2i: mixture of files within
# e2i: MSB has no column header

KAL_redo_collation()