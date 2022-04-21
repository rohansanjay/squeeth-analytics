from operator import iconcat
import requests
import pandas as pd 
import json 
import pickle
import datetime 
import time 

# instrument historical price 
# /historical/options/price/exchange/instrument?date=YYYY-MM-DDTHH

#2022-04-17

def pull(url, headers, start_date, end_date, json_save, df_save): 
    r = requests.get(url=url, headers=headers)

    with open(json_save, 'w') as outfile:
        json.dump(r.json(), outfile)

    df = pd.read_json(json_save)

    df.to_pickle(df_save)

    return df 

def pull_iterate(headers, start_date, end_date, json_save, df_save): 

    start_date = datetime.date(int(start_date[:4]),int(start_date[5:7]),int(start_date[8:10]))
    end_date = datetime.date(int(end_date[:4]),int(end_date[5:7]),int(end_date[8:10]))
    delta = datetime.timedelta(days=1)

    dfs = [] 

    counter =  0 
    while start_date <= end_date: 

        print('\n Pulling historical data: '+str(start_date)+' ...\n')

        url = 'https://gateway.laevitas.ch/historical/power_perp/squeeth/eth?start='+str(start_date)+'&end='+str(start_date) 

        r = requests.get(url=url, headers=headers)

        with open(json_save, 'w') as outfile:
            json.dump(r.json(), outfile)

        df = pd.read_json(json_save)

        dfs.append(df)

        #** 
        counter += 1 
        start_date += delta
        if (counter==4): 
            time.sleep(1) # slow down the api calls to not block key 
            counter = 0 
            print('api break 1 second ...\n')

    df = pd.concat(dfs)

    df = df.reset_index(drop=True) 

    df.to_pickle(df_save)

    return df 