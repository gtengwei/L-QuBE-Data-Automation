import pandas as pd
import os
import time
import datetime as dt

main_directory = os.getcwd()
change_directory = ''

def clean_dataframe(csv, option):
    f = open(csv, 'r')
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

    temp = result[1:]

    for i in range(len(temp)):
        temp[i] = temp[i].split(',')

    temp_df = pd.DataFrame(temp[1:],columns=temp[0])
    
    temp_df['Timestamp'] = temp_df['Timestamp'].str.split(':')
    temp_df['Timestamp'] = temp_df['Timestamp'].str[0] + ':' + temp_df['Timestamp'].str[1]
    
    slot_name = result[0]
    slot_name = slot_name.split(':')[1][1:]
    count = 1
    if option == 'all' or option == 'choose' or option == 'today':
        current_date = get_current_date()
        try:
            os.rename(csv, f"{current_date}_{slot_name}.csv")
        except:
            while True:
                try:
                    os.rename(csv, f"{current_date}_{slot_name}_({count}).csv")
                    break
                except:
                    count += 1

    elif option == 'daily' or option == 'daily_selected':
        yesterday_date = get_yesterday_date()
        try:
            os.rename(csv, f"{yesterday_date}_{slot_name}.csv")
        except:
            while True:
                try:
                    os.rename(csv, f"{yesterday_date}_{slot_name}_({count}).csv")
                    break
                except:
                    count += 1
                
    clean_df = temp_df.rename({'Value': slot_name}, axis=1)
    return clean_df

def merge_dataframes(df1,df2):
    df = pd.merge(df1,df2, on=['Date','Timestamp'], how='outer')
    return df

def get_current_date():
    return dt.datetime.now().strftime("%Y-%m-%d")

def get_yesterday_date():
    return (dt.datetime.now() - dt.timedelta(days=1)).strftime("%Y-%m-%d")

def get_current_datetime():
    return dt.datetime.now().strftime("%Y-%m-%d_%H-%M")

def create_new_directory(ip, user_directory, option):
    if option == 'all':
        current_date = get_current_date()
        path = user_directory
        directory = os.path.join("c:\\",path)
        temp_directory = os.path.join(directory, ip)
        change_directory = os.path.join(temp_directory, 'All_Collation')
        new_directory = os.path.join(change_directory, current_date)
        if not os.path.exists(new_directory):
            os.makedirs(new_directory)
    
    elif option == 'daily':
        yesterday_date = get_yesterday_date()
        path = user_directory
        directory = os.path.join("c:\\",path)
        temp_directory = os.path.join(directory, ip)
        change_directory = os.path.join(temp_directory, 'Daily_Collation')
        new_directory = os.path.join(change_directory, yesterday_date)
        if not os.path.exists(new_directory):
            os.makedirs(new_directory)
    
    elif option == 'choose':
        current_datetime = get_current_datetime()
        path = user_directory
        directory = os.path.join("c:\\",path)
        temp_directory = os.path.join(directory, ip)
        change_directory = os.path.join(temp_directory, 'Selected_Collation')
        new_directory = os.path.join(change_directory, current_datetime)
        if not os.path.exists(new_directory):
            os.makedirs(new_directory)

    elif option == 'daily_selected':
        yesterday_date = get_yesterday_date()
        path = user_directory
        directory = os.path.join("c:\\",path)
        temp_directory = os.path.join(directory, ip)
        change_directory = os.path.join(temp_directory, 'Daily_Selected_Collation')
        new_directory = os.path.join(change_directory, yesterday_date)
        if not os.path.exists(new_directory):
            os.makedirs(new_directory)
    
    elif option == 'today':
        current_date = get_current_date()
        path = user_directory
        directory = os.path.join("c:\\",path)
        temp_directory = os.path.join(directory, ip)
        change_directory = os.path.join(temp_directory, 'Today_Collation')
        new_directory = os.path.join(change_directory, current_date)
        if not os.path.exists(new_directory):
            os.makedirs(new_directory)

    print(f"New Directory {new_directory} Created")
    os.chdir(new_directory)
    return change_directory


def insert_empty_slot(df):
    hour_minute_list = [[i,j] for i in range(0,24) for j in range(0,60)]
    for i in range(len(hour_minute_list)):
        hour_minute_list[i] = ['%02d' % hour_minute_list[i][0], '%02d' % hour_minute_list[i][1]]
    for i in range(len(df['Timestamp'])):
        temp = df['Timestamp'][i].split(':')
        if [temp[0],temp[1]] in hour_minute_list:
            hour_minute_list.remove([temp[0],temp[1]])

    empty_row = [None for _ in range(len(df.columns))]
    for i in range(len(hour_minute_list)):
        hour_minute_list[i] = ':'.join(hour_minute_list[i])
        empty_row[0] = df['Date'][0]
        empty_row[1] = hour_minute_list[i]
        df.loc[len(df)] = empty_row
    df = df.sort_values(by=['Timestamp'], ascending=True)
    return df

def collate_dataframes(option, change_directory):
    time.sleep(0.5)
    path = os.getcwd()
    directory = os.path.join("c:\\",path)
    collated_df = pd.DataFrame(columns=['Date','Timestamp'])
    for root,dirs,files in os.walk(directory):
        for file in files:
            # Ignore collated file to avoid errors
            if file.endswith("collated.csv"):
                continue
            if file.endswith(".csv"):
                    clean_df = clean_dataframe(file, option)
                    if option == 'all' or option == 'choose':
                        continue
                    collated_df = merge_dataframes(collated_df,clean_df)

    if option == 'all' or option == 'choose':
        os.chdir(main_directory)
        return
    collated_df = collated_df.sort_values(by=['Date','Timestamp'], ascending=[True,True])


    # Name files based on option
    # Do not need to collate files for all and choose option
    # if option == 'all':
    #     os.chdir(change_directory)
    #     current_date = get_current_date()
    #     collated_df.to_excel(f"AllData_{current_date}_collated.xlsx", index = False)
    
    # elif option == 'choose':
    #     os.chdir(change_directory)
    #     current_datetime = get_current_datetime()
    #     filled_collated_df.to_excel(f"SelectedData_{current_datetime}_collated.xlsx", index = False)

    # Insert empty slots for missing minutes
    filled_collated_df = insert_empty_slot(collated_df)
    filled_collated_df = filled_collated_df.sort_values(by=['Date','Timestamp'], ascending=[True,True])

    if option == 'daily':
        os.chdir(change_directory)
        yesterday_date = get_yesterday_date()
        filled_collated_df.to_excel(f"Daily_{yesterday_date}_collated.xlsx", index = False)
    

    
    elif option == 'daily_selected':
        os.chdir(change_directory)
        yesterday_date = get_yesterday_date()
        filled_collated_df.to_excel(f"Daily_Selected_{yesterday_date}_collated.xlsx", index = False)
    
    elif option == 'today':
        os.chdir(change_directory)
        current_date = get_current_date()
        filled_collated_df.to_excel(f"Today_{current_date}_collated.xlsx", index = False)
    print("Collation Complete")
    os.chdir(main_directory)
