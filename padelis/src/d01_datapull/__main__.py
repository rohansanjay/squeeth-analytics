import os
from re import L
import sys

from matplotlib.font_manager import json_dump
from requests import head
from pull import osqueeth_data, eth_data
import laevitasapi

from datetime import date
import pandas as pd 


def main(api_key, uniswap_pool_adress_params, osqueeth_params, data_save_file, json_dump_save_file, df_save_file, url, headers, pull_data_bool) :

    uniswap_pool_endpoint = 'https://api.covalenthq.com/v1/1/uniswap_v3/swaps/address/{_address}/?quote-currency={_quote_currency}&format={_format}&page-number={_page_number}&page-size={_pag_size}&key={_key}'.format(
        _address=uniswap_pool_adress_params['osqueeth_pool_address'],
        _quote_currency=uniswap_pool_adress_params['quote_curency'],
        _format=uniswap_pool_adress_params['output_format'],
        _page_number=uniswap_pool_adress_params['page_number'],
        _pag_size=uniswap_pool_adress_params['page_size'],
        _key=api_key
    )

    osqueeth_historical_price_endpoint = 'https://api.covalenthq.com/v1/pricing/historical_by_addresses_v2/1/USD/{_address}/?quote-currency={_quote_currency}&format={_format}&from={_from}&to={_to}&key={_key}'.format(
        _address=osqueeth_params['osqueeth_adress'],
        _quote_currency=osqueeth_params['quote_currency'],
        _format=osqueeth_params['output_format'],
        _from=osqueeth_params['from_date'],
        _to=osqueeth_params['to_date'],
        _key=api_key
    )

    eth_historical_price_endpoint = 'https://api.covalenthq.com/v1/pricing/historical_by_addresses_v2/1/USD/{_address}/?quote-currency={_quote_currency}&format={_format}&from={_from}&to={_to}&key={_key}'.format(
        _address=osqueeth_params['eth_address'],
        _quote_currency=osqueeth_params['quote_currency'],
        _format=osqueeth_params['output_format'],
        _from=osqueeth_params['from_date'],
        _to=osqueeth_params['to_date'],
        _key=api_key
    )

    #Data for the past year 

    #for OSQUEETH I assume I am also getting 1 value per day 

    # osqueeth_data(api_key, uniswap_pool_endpoint, osqueeth_historical_price_endpoint, data_save_file)

    #for ETH data I am getting the closing $ of WETH so 1 value per day 

    # eth_data(api_key, uniswap_pool_endpoint, eth_historical_price_endpoint, data_save_file)


    # LAEVITAS API PULL 

    # df = laevitasapi.pull(url, headers, start_date, end_date, json_dump_save_file, df_save_file) 

    # print(df)

    if pull_data_bool: 
        df = laevitasapi.pull_iterate(headers, start_date, end_date, json_dump_save_file, df_save_file) 
    else: 
        df = pd.read_pickle(df_save_file)

    print(df) 


if __name__ == "__main__":

    try:
        api_key = sys.argv[1]
    except:
        api_key = 'ckey_219fe432bc83419181e988fade9'

    try:
        uniswap_pool_adress_params = sys.argv[2]
    except:
        uniswap_pool_adress_params = {
            'osqueeth_pool_address': '0x82c427AdFDf2d245Ec51D8046b41c4ee87F0d29C', 'quote_curency': 'USD',
            'output_format': 'csv', 'page_number': '1', 'page_size': '1'}

    try:
        osqueeth_params = sys.argv[3]
    except:
        #that is the Uniswap Osqueeth pool which has approx 60% of osqueeth 
        #8,500 oSqueeth tokens approx 
        # SQUEETH-ETH pool 
        osqueeth_params = {'osqueeth_adress': '0xf1B99e3E573A1a9C5E6B2Ce818b617F0E664E86B',
                           'eth_address': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 'quote_currency': 'USC',
                           'output_format': 'JSON', 'from_date': '2021-03-06', 'to_date': '2022-03-06'}

    try:
        data_save_file = sys.argv[4]
    except:
        data_save_file = './data/'


    # headers = {'Content-Type':'application/json','apiKey':'1fbff1af-511c-4855-b01f-b1ada2ab3941'}

    try: 
        start_date = sys.argv[5]
    except:  # '2022-02-27' --> first day of data 
        start_date = '2022-02-27'
    
    try: 
        end_date = sys.argv[6]
    except: 
        end_date= str(date.today())

    try: 
        url = sys.argv[7]
    except: 
        url = 'https://gateway.laevitas.ch/historical/power_perp/squeeth/eth?start='+start_date+'&end='+end_date

    try: 
        json_dump_savefile = sys.argv[8]
    except: 
        json_dump_save_file = data_save_file+'historical.json'

    try: 
        df_save_file = sys.argv[9]
    except: 
        df_save_file = data_save_file+'historical.pickle'
    
    try: 
        headers = sys.argv[10]
    except: 
        headers = {'Content-Type':'application/json','apiKey':'1fbff1af-511c-4855-b01f-b1ada2ab3941'}

    try: 
        pull_data_bool = sys.argv[11]
    except: 
        pull_data_bool = False 

    


    main(api_key, uniswap_pool_adress_params, osqueeth_params, data_save_file, json_dump_save_file, df_save_file, url, headers, pull_data_bool) 
