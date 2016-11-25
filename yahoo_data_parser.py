import time
import pickle
from yahoo_finance import Share
from SP500_DB import cashtag_list
from pprint import pprint
import sys
import pandas as pd
#193.136.221.43

start_time = time.time()

'''
--------------------------------------------------------------------------------
-------------------------------- LOADING DATA ----------------------------------
--------------------------------------------------------------------------------
'''

f = open('stock_market_data.pckl', 'rb')
companies_data = pickle.load(f)
f.close()


elapsed_time = time.time() - start_time
print('\ntime elapsed restoring companies_data: '+ str(elapsed_time)) 

#pprint(companies_data[0][10][0]['Symbol'])
pprint(companies_data[0][0] == '$MMM')
for data in companies_data:
    if data[0][0] == '$MMM':
        pprint(data)


'''
--------------------------------------------------------------------------------
----------------------------- DATAFRAME CREATION -------------------------------
--------------------------------------------------------------------------------
'''
sys.exit()

cashtag = []
stock_exchange = []
market_cap = []
avg_daily_volume = []
ebitda = []
year_lowest_value = []
year_highest_value = []
dividend_share = []
dividend_yield = []
earnings_share = []
hist_date = []
hist_open = []
hist_close = []
hist_adj_Close = []
hist_low = []    
hist_high = []
hist_volume = []
 
for company_data in companies_data:
    cashtag = cashtag + [company_data[0]]
    stock_exchange = stock_exchange + [company_data[1]]
    market_cap = market_cap + [company_data[2]]
    avg_daily_volume = avg_daily_volume + [company_data[3]]
    ebitda = ebitda + [company_data[4]]
    year_lowest_value = year_lowest_value + [company_data[5]]
    year_highest_value = year_highest_value + [company_data[6]]
    dividend_share = dividend_share + [company_data[7]]
    dividend_yield = dividend_yield + [company_data[8]]
    earnings_share = earnings_share + [company_data[9]]
    
    date = []
    open = []
    close = []
    adj_close = []
    low = []    
    high = []
    volume = []
    for day_data in company_data[10]:
        print(day_data)
        date = date + [day_data['Date']]
        open = open + [day_data['Open']]
        close = close + [day_data['Close']]
        adj_close = adj_close + [day_data['Adj_Close']]
        low = low + [day_data['Low']]
        high = high + [day_data['High']]
        volume = volume + [day_data['Volume']]
    
    hist_date = hist_date + [date]
    hist_open = hist_open + [open]
    hist_close = hist_close + [close]
    hist_adj_Close = hist_adj_Close + [adj_close]
    hist_low = hist_low + [low]
    hist_high = hist_high + [high]
    hist_volume = hist_volume + [volume]
    


    data_user = {'cashtag': cashtag, 'stock_exchange': stock_exchange,\
                 'market_cap': market_cap, 'avg_daily_volume': avg_daily_volume,\
                  'ebitda': ebitda, 'year_lowest_value': year_lowest_value,\
                  'year_highest_value': year_highest_value, 'dividend_share': dividend_share,\
                  'dividend_yield': dividend_yield, 'earnings_share': earnings_share,\
                  'hist_date': hist_date, 'hist_open': hist_open, 'hist_close': hist_close,\
                  'hist_adj_Close': hist_adj_Close, 'hist_low': hist_low,\
                  'hist_high': hist_high, 'hist_volume': hist_volume}
    columns_tweets = ['cashtag', 'stock_exchange', 'market_cap', 'avg_daily_volume',\
                  'ebitda', 'year_lowest_value', 'year_highest_value',\
                  'dividend_share', 'dividend_yield', 'earnings_share',\
                  'hist_date', 'hist_open', 'hist_close', 'hist_adj_Close',\
                  'hist_low', 'hist_high', 'hist_volume']
    df_company_data = pd.DataFrame(data_user, columns = columns_tweets)
    
    