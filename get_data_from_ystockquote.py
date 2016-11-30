import time
import pickle
import ystockquote as ysq
from SP500_DB import cashtag_list
import sys 
from pprint import pprint

#193.136.221.43

start_time = time.time()

cashtag_list = ['$XRAY', '$IP', '$MON', '$AJG']

start_date = '2016-08-01'
finish_date = '2016-11-04'
companies_data = []
for cashtag in cashtag_list:
    try:
        company = cashtag[1:]
        print(company)
        
        
        historical = ysq.get_historical_prices(company, start_date, finish_date)
        dividend_share = ysq.get_dividend_per_share(company)
        dividend_yield = ysq.get_dividend_yield(company)
        earnings_share = ysq.get_earnings_per_share(company)
        year_highest_value = ysq.get_52_week_high(company)
        year_lowest_value = ysq.get_52_week_low(company)
        ebitda = ysq.get_ebitda(company)
        market_cap = ysq.get_market_cap(company)
        stock_exchange = ysq.get_stock_exchange(company)
        avg_daily_volume = ysq.get_avg_daily_volume(company)  

        
        companies_data.append((cashtag, stock_exchange, market_cap, avg_daily_volume,\
                               ebitda, year_lowest_value, year_highest_value,\
                               dividend_share, dividend_yield, earnings_share, historical))
        #print(companies)
    except Exception:
        print('Error loading data from ', company)

elapsed_time = time.time() - start_time
print('\ntime elapsed with ystockquote: '+ str(elapsed_time))


'''
--------------------------------------------------------------------------------
-------------------------------- STORING DATA ----------------------------------
--------------------------------------------------------------------------------
'''
f = open('stock_market_data_ystockquote.pckl', 'wb')
pickle.dump(companies_data, f)
f.close()    

elapsed_time = time.time() - start_time
print('\ntime elapsed storing stock market data: '+ str(elapsed_time)) 


#print(companies_data)
