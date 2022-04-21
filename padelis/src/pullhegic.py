import os
from re import L
import sys

from matplotlib.font_manager import json_dump
import requests 

from datetime import date
import pandas as pd 
import json 

#2021-09-07 15:15:00+00

# action = 'price'
# exchange = 'binance'
# instrument = 'BTC-25MAR22-60000-C' # BTC-25MAR22-60000-C
# date_s = '2021-12-22T10' #YYYY-MM-DDTHH


# url = 'https://gateway.laevitas.ch/historical/options/'+action+'/'+exchange+'/'+instrument+'?date='+date_s


# headers = {'Content-Type':'application/json','apiKey':'1fbff1af-511c-4855-b01f-b1ada2ab3941'}

# r = requests.get(url=url, headers=headers)


# with open('./trial.pickle', 'w') as outfile:
#     json.dump(r.json(), outfile)

# df = pd.read_json('./trial.pickle')

# print(df)

df = pd.read_pickle('./hegicdata.pickle')

print(df)