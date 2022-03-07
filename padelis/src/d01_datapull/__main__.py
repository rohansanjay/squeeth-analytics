import os
import sys
from pull import osqueeth_data, eth_data


def main(api_key, uniswap_pool_adress_params, osqueeth_params, data_save_file):

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
    osqueeth_data(api_key, uniswap_pool_endpoint, osqueeth_historical_price_endpoint, data_save_file)

    #for ETH data I am getting the closing $ of WETH so 1 value per day 
    eth_data(api_key, uniswap_pool_endpoint, eth_historical_price_endpoint, data_save_file)


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

    main(api_key, uniswap_pool_adress_params, osqueeth_params, data_save_file)
