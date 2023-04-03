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

# config = get_config()
# KAL_collation(config.collation['KAL_directory'])