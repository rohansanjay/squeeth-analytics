from duneanalytics import DuneAnalytics
import json
from numpy import size 
import pandas as pd 
import numpy as np 

# initialize client
dune = DuneAnalytics('pdeligiannis', 'Treloamaksi21!')

# try to login
dune.login()

# fetch token
dune.fetch_auth_token()

# fetch query result id using query id
# query id for any query can be found from the url of the query:
# for example: 
# https://duneanalytics.com/queries/4494/8769 => 4494
# https://duneanalytics.com/queries/3705/7192 => 3705
# https://duneanalytics.com/queries/3751/7276 => 3751

result_id = dune.query_result_id(query_id=623007)

data = dune.query_result(result_id)

# with open('./trial.pickle', 'w') as outfile:
#     json.dump(data, outfile)

# df = pd.read_json('./trial.pickle')

# for k in data.keys(): 
#     print(k)

# print(data.values())

# print(data.values()[0]["data"])

# print(data.items())
# print(dir(data.__getitem__("data").values()))

# print(data.__getitem__("data").values().__reduce__)

# df = pd.DataFrame(np.zeros((len(data), len(list(data[0]['data'].keys())))), columns=list(data[0]['data'].keys())) 

# counter = 0
# for i in data: 
#     df.iloc[counter] = i['data'].values()
#     counter += 1 

#Breakeven Price, Date, Exercise Date, Expiration Date, ID, Size, Status, Strike, USD cost, account, pnl, tx hash, type 
#Date, Status, ID, type, Size, USD cost, Strike, Breakeven Price, pnl, Expiration date, Exercise Date, account, tx hash 

data = data[['Date','Status','ID','type','Size','USD cost','Strike','Breakeven Price','pnl','Expiration Date','Exercise Date','account','tx hash']]
data['Date'] = pd.to_datetime(data['Date']) 
data['Expiration Date'] = pd.to_datetime(data['Expiration Date']) 
data['Exercise Date'] = pd.to_datetime(data['Exercise Date']) 
# data['Status'] = data['Status'].astype(str)
# data['account'] = data['account'].astype(str)
# data['tx hash'] = data['tx hash'].astype(str)
# data['Status'] = data['Status'].astype(str)
# data['type'] = data['type'].astype(str)

data.to_pickle('./hegicdata.pickle')    