import time
import pickle
from yahoo_finance import Share
from SP500_DB import cashtag_list

#193.136.221.43
#cashtag_list = ['$MMM']
start_time = time.time()

companies_data = []
for company in cashtag_list:
    try:
        company = company[1:]
        share = Share(company)
        print(company)
        
        open_price = share.get_open()
        price = share.get_price()
        companies_data.append((company, price, open_price))
        #print(companies)
    except Exception:
        print('Error loading share from ', company)

elapsed_time = time.time() - start_time
print('\ntime elapsed with yahoo finance: '+ str(elapsed_time))


'''
--------------------------------------------------------------------------------
-------------------------------- STORING DATA ----------------------------------
--------------------------------------------------------------------------------
'''

f = open('stock_market_data.pckl', 'wb')
pickle.dump(companies_data, f)
f.close()    

elapsed_time = time.time() - start_time
print('\ntime elapsed storing stock market data: '+ str(elapsed_time)) 
