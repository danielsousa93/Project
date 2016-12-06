import time
import pickle
from yahoo_finance import Share
from SP500_DB import cashtag_list
import sys 

#193.136.221.43


start_time = time.time()

start_date = '2016-08-01'
finish_date = '2016-11-15'
companies_data = []
for cashtag in cashtag_list:
    try:
        company = cashtag[1:]
        share = Share(company)
        print(company)
        
        
        historical = share.get_historical(start_date, finish_date)
        dividend_share = share.get_dividend_share()
        dividend_yield = share.get_dividend_yield()
        earnings_share = share.get_earnings_share()
        year_highest_value = share.get_year_high()
        year_lowest_value = share.get_year_low()
        ebitda = share.get_ebitda()
        market_cap = share.get_market_cap()
        stock_exchange = share.get_stock_exchange()
        avg_daily_volume = share.get_avg_daily_volume()
        
        
        companies_data.append((cashtag, stock_exchange, market_cap, avg_daily_volume,\
                               ebitda, year_lowest_value, year_highest_value,\
                               dividend_share, dividend_yield, earnings_share, historical))
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
#sys.exit()
f = open('stock_market_data.pckl', 'wb')
pickle.dump(companies_data, f)
f.close()    

elapsed_time = time.time() - start_time
print('\ntime elapsed storing stock market data: '+ str(elapsed_time)) 


#print(companies_data)
