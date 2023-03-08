import pandas as pd
import os
import time
import datetime as dt

main_directory = os.getcwd()
change_diretory = ''

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
    # result = result.split(',')

    temp = result[1:]

    for i in range(len(temp)):
        temp[i] = temp[i].split(',')

    temp_df = pd.DataFrame(temp[1:],columns=temp[0])
    
    for i in range(len(temp_df['Timestamp'])):
        temp_df['Timestamp'][i] = temp_df['Timestamp'][i].split(':')
        temp_df['Timestamp'][i] = temp_df['Timestamp'][i][0] + ':' + temp_df['Timestamp'][i][1]
    
        slot_name = result[0]
    slot_name = slot_name.split(':')[1][1:]
    count = 1
    if option == 'all':
        currentDateTime = get_current_date()
        try:
            os.rename(csv, f"{currentDateTime}_{slot_name}.csv")
        except:
            while True:
                try:
                    os.rename(csv, f"{currentDateTime}_{slot_name}_({count}).csv")
                    break
                except:
                    count += 1

    elif option == 'daily':
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
    return dt.datetime.now().strftime("%Y-%m-%d %H.%M")

def create_new_directory(ip, user_directory, option):
    if option == 'all':
        currentDateTime = get_current_date()
        path = user_directory
        directory = os.path.join("c:\\",path)
        temp_directory = os.path.join(directory, ip)
        change_directory = os.path.join(temp_directory, 'All_Collation')
        new_directory = os.path.join(change_directory, currentDateTime)
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
    os.chdir(new_directory)
    return change_directory

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
                    collated_df = merge_dataframes(collated_df,clean_df)

    collated_df = collated_df.sort_values(by=['Date','Timestamp'], ascending=True)
    if option == 'all':
        os.chdir(change_directory)
        currentDateTime = get_current_date()
        collated_df.to_excel(f"AllData_{currentDateTime}_collated.xlsx", index = False)
    
    elif option == 'daily':
        os.chdir(change_directory)
        yesterdayDate = get_yesterday_date()
        collated_df.to_excel(f"{yesterdayDate}_collated.xlsx", index = False)
    
    elif option == 'choose':
        os.chdir(change_directory)
        current_datetime = get_current_date()
        collated_df.to_excel(f"SelectedData_{current_datetime}_collated.xlsx", index = False)
    # collated_df.to_csv('collated.csv', index=False)
    print("Collation Complete")
    os.chdir(main_directory)

# collate_dataframes()
