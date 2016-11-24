import time
import pickle
from yahoo_finance import Share
from SP500_DB import cashtag_list
from pprint import pprint
#193.136.221.43

start_time = time.time()

'''
--------------------------------------------------------------------------------
------------------------------- RESTORING DATA ---------------------------------
--------------------------------------------------------------------------------
'''

f = open('stock_market_data.pckl', 'rb')
companies_data = pickle.load(f)
f.close()


elapsed_time = time.time() - start_time
print('\ntime elapsed restoring companies_data: '+ str(elapsed_time)) 

pprint(companies_data[0])



share = Share('MMM')
print('get_change', share.get_change())