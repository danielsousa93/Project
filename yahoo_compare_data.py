import time
import pickle
from pprint import pprint
import sys
import pandas as pd
from yahoo_data_parser import df_company_data
import matplotlib.pyplot as plt

#193.136.221.43

start_time = time.time()

'''
--------------------------------------------------------------------------------
-------------------------------- LOADING DATA ----------------------------------
--------------------------------------------------------------------------------
'''
f = open('df_features_by_user_by_company.pckl', 'rb')
df_features_by_user_by_company = pickle.load(f)
f.close()

f = open('df_company_data.pckl', 'rb')
df_company_data = pickle.load(f)
f.close()


elapsed_time = time.time() - start_time
print('\ntime elapsed loading df_company_data: '+ str(elapsed_time)) 


'''
--------------------------------------------------------------------------------
----------------------------- DATAFRAME CREATION -------------------------------
--------------------------------------------------------------------------------
'''
sys.exit()
#print(df_company_data.sort_values(by='earnings_share', ascending=0))
#print(df_company_data[df_company_data['cashtag'] == '$XRAY'])


a = df_company_data[['market_cap']].sort_values(by='market_cap', ascending=0)[:10].plot(kind='bar')


b = df_company_data[['market_cap']].sort_values(by='market_cap', ascending=0)[:20].plot(kind='bar')

plt.show(a and b)