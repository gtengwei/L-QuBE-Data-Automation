import pandas as pd
import os

def clean_dataframe(csv):
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

    slot_name = result[0]
    slot_name = slot_name.split(':')[1][1:]

    clean_df = temp_df.rename({'Value': slot_name}, axis=1)
    return clean_df

def merge_dataframes(df1,df2):
    df = pd.merge(df1,df2, on=['Date','Timestamp'], how='outer')
    return df

def collate_dataframes():
    path = os.getcwd()
    directory = os.path.join("c:\\",path)
    collated_df = pd.DataFrame(columns=['Date','Timestamp'])
    for root,dirs,files in os.walk(directory):
        for file in files:
            # Ignore collated file to avoid errors
            if file.startswith("collated"):
                continue
            if file.endswith(".csv"):
                    clean_df = clean_dataframe(file)
                    print(clean_df)
                    collated_df = merge_dataframes(collated_df,clean_df)
    collated_df.to_csv('collated.csv', index=False)

# collate_dataframes()