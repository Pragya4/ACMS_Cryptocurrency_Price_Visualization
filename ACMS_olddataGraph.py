
# coding: utf-8

# In[19]:


import os
import numpy as np
import pandas as ps
import pickle
import quandl
from datetime import datetime


# In[20]:


import plotly.offline as py
import plotly.graph_objs as go
import plotly.figure_factory as ff
py.init_notebook_mode(connected=True)


# In[23]:


def get_quandl_data(quandl_id):
    cache_path='{}.pkl'.format(quandl_id).replace('/','-')
    try:
        f=open(cache_path,'rb')
        df=pickle.load(f)
        print('Loaded {} from cache'.format(quandl_id))
    except(OSError,IOError) as e:
        print("Downloading {} from Quandl".format(quandl_id))
        df = quandl.get(quandl_id, returns="pandas")
        df.to_pickle(cache_path)
        print('Cached {} at {}'.format(quandl_id, cache_path))
    return df


# In[24]:


# Pull Kraken BTC price exchange data
btc_usd_price_kraken = get_quandl_data('BCHARTS/KRAKENUSD')


# In[25]:


btc_usd_price_kraken.head()


# In[26]:


btc_trace = go.Scatter(x=btc_usd_price_kraken.index, y=btc_usd_price_kraken['Weighted Price'])
py.iplot([btc_trace])


# In[95]:


import json
def get_json_data(json_url, cache_path):
    '''Download and cache JSON data, return as a dataframe.'''
    try:        
        f = open(cache_path, 'rb')
        df = pickle.load(f)   
        print('Loaded {} from cache'.format(json_url))
    except (OSError, IOError) as e:
        print('Downloading {}'.format(json_url))
        print(json_url)
        #df = pd.read_json(json_url)
        df=json.dumps(json_url)
        print("flag pickle")
        final=pd.read_json(df)
        print(final)
        df.to_pickle(cache_path)
        print(df)
        print('Cached {} at {}'.format(json_url, cache_path))
    return df


# In[96]:


#for other cryptocurrencies, other than bitcoins=altcoins
from datetime import date
from datetime import datetime
import time
base_polo_url = 'https://poloniex.com/public?command=returnChartData&currencyPair={}&start={}&end={}&period={}'
start_date = (datetime.strptime('2015-01-01', '%Y-%m-%d')) # get data from the start of 2015

"""s = "16/08/2013 09:51:43"
>>> d = datetime.strptime(s, "%d/%m/%Y %H:%M:%S")
>>> time.mktime(d.timetuple())"""

print ("startdate")

#start_date=datetime.strptime(start_date,"%Y-%m-%d")
#print(time.mktime(start_date.timetuple()))
start_date=time.mktime(start_date.timetuple())
print(start_date)
end_date = datetime.now() # up until today
print("enddate")
#print(time.mktime(end_date.timetuple()))
end_date=time.mktime(end_date.timetuple())
print(end_date)
pediod = 86400 # pull daily data (86,400 seconds per day)

def get_crypto_data(poloniex_pair):
    '''Retrieve cryptocurrency data from poloniex'''
    json_url = base_polo_url.format(poloniex_pair, start_date, end_date, pediod)
    print("json_url")
    print(json_url)
    data_df = get_json_data(json_url, poloniex_pair)
    print("data_df")
    print(data_df)
    data_df = data_df.set_index('date')
    print("data_df")
    print(data_df)
    return data_df




# In[97]:


import pandas as pd
altcoins = ['ETH','LTC','XRP','ETC','STR','DASH','SC','XMR','XEM']

altcoin_data = {}
for altcoin in altcoins:
    coinpair = 'BTC_{}'.format(altcoin)
    print(coinpair)
    crypto_price_df = get_crypto_data(coinpair)
    altcoin_data[altcoin] = crypto_price_df

