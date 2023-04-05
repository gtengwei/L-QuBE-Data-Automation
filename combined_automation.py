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
    collated_df = pd.DataFrame()
    for root,dirs,files in os.walk(directory):
        for file in files:
            # print(file)
            # Ignore collated file to avoid errors
            if file.endswith('collated.csv'):
                continue

            if file.endswith('.csv'):
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
                    df = insert_empty_slot_1(df)
                    collated_df = pd.concat([collated_df, df], axis=0)
                except:
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
                        except:
                            files_with_errors.append(file)
                            pass
            
            if file.endswith('.xlsx'):
                try:
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
                    files_with_errors.append(file)
                    pass
    print(f'These are the files with errors: {files_with_errors}')
    current_date = get_current_date()
    collated_df.to_excel(f'{vendor}_{current_date}_collated.xlsx', index=False)
    
config = get_config()
# e2i_collation(config.collation['directory'])
one_for_all_collation(config.collation['directory'], config.collation['vendor'], config.collation['excel_column_header_row'])

# issues with excel file: date and time column, and format of date and time(2022-08-26 :23:59:00 PM)
# e2i: 01:50 chiller 41 has duplicate timestamp
# e2i: chiller 217 has no column header
# e2i: mixture of files within
# e2i: MSB has no column header