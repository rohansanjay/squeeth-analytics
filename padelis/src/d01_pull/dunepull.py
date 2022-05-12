# -*- coding: utf-8 -*- #
from requests import Session
import pandas as pd
import numpy as np
import re

# Global URL Endpoints

# ** Connect go GRAPH QL api backend and fetch result of queries

# https://gist.github.com/mkwatson/faa70abe23f79b9c54556cf4ac92f1d7

"""
Shell Script to pull raw dune data from backend query 


curl 'https://core-hsr.duneanalytics.com/v1/graphql' \
  --data-raw $'
  {
    "operationName": "FindResultDataByResult",
    "variables": { "result_id": "f0de20b7-fad3-4b20-adcd-4f8885292b7c" },
    "query":"query FindResultDataByResult($result_id: uuid\u0021) {\\n  query_results(where: {id: {_eq: $result_id}}) {\\n    id\\n    job_id\\n    error\\n    runtime\\n    generated_at\\n    columns\\n    __typename\\n  }\\n  get_result_by_result_id(args: {want_result_id: $result_id}) {\\n    data\\n    __typename\\n  }\\n}\\n"}
'
https://gist.github.com/mkwatson/faa70abe23f79b9c54556cf4ac92f1d7

"""

BASE_URL = "https://dune.xyz"
GRAPH_URL = 'https://core-hsr.duneanalytics.com/v1/graphql'


class DuneAnalytics:
    """
    Acts as a client for Dune Analytics 
    Authorization Code Request 
    https://www.oauth.com/oauth2-servers/access-tokens/
    """

    def __init__(self, username, password):
        """
        Initialize the object
        :param username: username for duneanalytics.com
        :param password: password for duneanalytics.com
        """
        self.csrf = None
        self.auth_refresh = None
        self.token = None
        self.username = username
        self.password = password
        self.session = Session()
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'dnt': '1',
            'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'origin': BASE_URL,
            'upgrade-insecure-requests': '1'
        }
        self.session.headers.update(headers)

    def login(self):
        """
        Try to login to duneanalytics.com & get the token --> prevent getting blocked requests 
        :return:
        """
        login_url = BASE_URL + '/auth/login'
        csrf_url = BASE_URL + '/api/auth/csrf'
        auth_url = BASE_URL + '/api/auth'

        # fetch login page
        self.session.get(login_url)

        # get csrf token
        self.session.post(csrf_url)
        self.csrf = self.session.cookies.get('csrf')

        # try to login
        form_data = {
            'action': 'login',
            'username': self.username,
            'password': self.password,
            'csrf': self.csrf,
            'next': BASE_URL
        }

        self.session.post(auth_url, data=form_data)
        self.auth_refresh = self.session.cookies.get('auth-refresh')

    def fetch_auth_token(self):
        """
        Fetch authorization token for the user
        :return:
        """
        session_url = BASE_URL + '/api/auth/session'

        response = self.session.post(session_url)
        if response.status_code == 200:
            self.token = response.json().get('token')
        else:
            print(response.text)

    def query_result_id(self, url):
        """
        Fetch the query result id for a query

        :param url: provide the url 
        :return:
        """

        # Fetches the Query ID from the URL
        try:
            query_id = int(re.findall(r'\d+', url)[0])
        except:
            print('Wrong URL!')
            return None

        query_data = {"operationName": "GetResult", "variables": {"query_id": query_id},
                      "query": "query GetResult($query_id: Int!, $parameters: [Parameter!]) "
                               "{\n  get_result(query_id: $query_id, parameters: $parameters) "
                               "{\n    job_id\n    result_id\n    __typename\n  }\n}\n"
                      }

        self.session.headers.update({'authorization': f'Bearer {self.token}'})

        response = self.session.post(GRAPH_URL, json=query_data)
        if response.status_code == 200:
            data = response.json()
            if 'errors' in data:
                return None
            result_id = data.get('data').get('get_result').get('result_id')
            return result_id
        else:
            print(response.text)
            return None

    def query_result_json(self, url):
        """
        :return: (json object of data return)
        """

        result_id = self.query_result_id(url)

        query_data = {"operationName": "FindResultDataByResult",
                      "variables": {"result_id": result_id},
                      "query": "query FindResultDataByResult($result_id: uuid!) "
                               "{\n  query_results(where: {id: {_eq: $result_id}}) "
                               "{\n    id\n    job_id\n    error\n    runtime\n    generated_at\n    columns\n    __typename\n  }"
                               "\n  get_result_by_result_id(args: {want_result_id: $result_id}) {\n    data\n    __typename\n  }\n}\n"
                      }

        self.session.headers.update({'authorization': f'Bearer {self.token}'})

        response = self.session.post(GRAPH_URL, json=query_data)
        if response.status_code == 200:
            r = response.json()
            return r
        else:
            print(response.text)
            return None

    def query_result_df(self, url):
        """
        :return: (dataframe object of data return)
        """

        result_id = self.query_result_id(url)

        query_data = {"operationName": "FindResultDataByResult",
                      "variables": {"result_id": result_id},
                      "query": "query FindResultDataByResult($result_id: uuid!) "
                               "{\n  query_results(where: {id: {_eq: $result_id}}) "
                               "{\n    id\n    job_id\n    error\n    runtime\n    generated_at\n    columns\n    __typename\n  }"
                               "\n  get_result_by_result_id(args: {want_result_id: $result_id}) {\n    data\n    __typename\n  }\n}\n"
                      }

        self.session.headers.update({'authorization': f'Bearer {self.token}'})

        response = self.session.post(GRAPH_URL, json=query_data)
        if response.status_code == 200:
            r = response.json()
            df = pd.DataFrame({i: r['data']['get_result_by_result_id'][i]['data']
                               for i in range(len(r['data']['get_result_by_result_id']))}).T
            return df
        else:
            print(response.text)
            return None
