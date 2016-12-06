import time
import pickle
from pprint import pprint
import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from SP500_DB import cashtag_list

#193.136.221.43

start_time = time.time()

'''
--------------------------------------------------------------------------------
-------------------------------- LOADING DATA ----------------------------------
--------------------------------------------------------------------------------
'''
f = open('df_tweets_by_cashtag.h5', 'rb')
df_tweets_by_cashtag = pickle.load(f)
f.close()

elapsed_time = time.time() - start_time
print('\ntime elapsed loading data: '+ str(elapsed_time)) 

'''
--------------------------------------------------------------------------------
------------------------- CREATE DF_TWEETS_BY_COMPANY --------------------------
--------------------------------------------------------------------------------
'''
#cashtag_list = cashtag_list[:5]

df_tweets_by_company = {}
for cashtag in cashtag_list:
    print(cashtag)
    df_tweets_by_company[cashtag] = df_tweets_by_cashtag[df_tweets_by_cashtag['cashtag_index'] == cashtag][['user_name', 'tweet_date', 'tweet_text']].copy()

f = open('df_tweets_by_company.pckl', 'wb')
pickle.dump(df_tweets_by_company, f)
f.close() 

#print(df_tweets_by_company['$ZTS'])

elapsed_time = time.time() - start_time
print('\ntime elapsed creating df_tweets_by_company: '+ str(elapsed_time)) 


 

