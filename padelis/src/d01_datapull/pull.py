import os
import numpy as np
import pandas as pd
import requests as r
import json


def osqueeth_data(api_key,uniswap_pool_endpoint,osqueeth_historical_price_endpoint,data_save_file):
    
    res = r.get(osqueeth_historical_price_endpoint)

    osqueeth_json = res.json()['data'][0] #nested dict object of data 

    osqueeth_df = pd.DataFrame(np.zeros((len(osqueeth_json['prices']), 6)),columns=['Date','Contract_Name','Contract_Address','Ticker_Symbol','Currency','Price'])
    
    osqueeth_df['Contract_Name'] = osqueeth_json['contract_name']
    osqueeth_df['Contract_Address'] = osqueeth_json['contract_address']
    osqueeth_df['Ticker_Symbol'] = osqueeth_json['contract_ticker_symbol']
    osqueeth_df['Currency'] = osqueeth_json['quote_currency']

    prices = [i['price'] for i in osqueeth_json['prices']]
    dates = [i['date'] for i in osqueeth_json['prices']]

    osqueeth_df['Price'] = prices
    osqueeth_df['Date'] = dates

    osqueeth_df.to_pickle(data_save_file+'osqueeth_historical.pickle')

def eth_data(api_key, uniswap_pool_endpoint, eth_historical_price_endpoint, data_save_file): 

    res = r.get(eth_historical_price_endpoint)

    eth_json = res.json()['data'][0] #nested dict object of data 

    eth_df = pd.DataFrame(np.zeros((len(eth_json['prices']), 6)),columns=['Date','Contract_Name','Contract_Address','Ticker_Symbol','Currency','Price'])
    
    eth_df['Contract_Name'] = eth_json['contract_name']
    eth_df['Contract_Address'] = eth_json['contract_address']
    eth_df['Ticker_Symbol'] = eth_json['contract_ticker_symbol']
    eth_df['Currency'] = eth_json['quote_currency']

    prices = [i['price'] for i in eth_json['prices']]
    dates = [i['date'] for i in eth_json['prices']]

    eth_df['Price'] = prices
    eth_df['Date'] = dates

    print(eth_df)

    eth_df.to_pickle(data_save_file+'eth_historical.pickle')
    