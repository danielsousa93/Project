import time
import pickle
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

#f = open('stock_market_data_ystockquote.pckl', 'rb')
f = open('stock_market_data.pckl', 'rb')
companies_data = pickle.load(f)
f.close()


elapsed_time = time.time() - start_time
print('\ntime elapsed loading stock market data: '+ str(elapsed_time)) 


#pprint(companies_data)

'''
--------------------------------------------------------------------------------
----------------------------- DATAFRAME CREATION -------------------------------
--------------------------------------------------------------------------------
'''
#sys.exit()

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
    
    
    if company_data[1] == 'NYQ':
        stock_exchange = stock_exchange + ['NYSE']
    elif company_data[1] == 'NMS':
        stock_exchange = stock_exchange + ['NASDAQ']
    else:
        stock_exchange = stock_exchange + [company_data[1]]
          
    
    try:
        if company_data[2][-1:] == 'B':
            market_cap = market_cap + [float(company_data[2][:-1])*1000000000]
        elif company_data[2][-1:] == 'M':
            market_cap = market_cap + [float(company_data[2][:-1])*1000000]
        else:
            market_cap = market_cap + [0]
    except Exception:
        market_cap = market_cap + [0]

    try:
        avg_daily_volume = avg_daily_volume + [float(company_data[3])]
    except Exception:
        avg_daily_volume = avg_daily_volume + [0]

    try:
        if company_data[4][-1:] == 'B':
            ebitda = ebitda + [float(company_data[4][:-1])*1000000000]
        elif company_data[4][-1:] == 'M':
            ebitda = ebitda + [float(company_data[4][:-1])*1000000]
        else:
            ebitda = ebitda + [0]
    except Exception:
        ebitda = ebitda + [0]
    
    year_lowest_value = year_lowest_value + [float(company_data[5])]
    year_highest_value = year_highest_value + [float(company_data[6])]
    
    
    if company_data[7] is not None:
        dividend_share = dividend_share + [float(company_data[7])]
        dividend_yield = dividend_yield + [float(company_data[8])]
    else:
        dividend_share = dividend_share + [0]
        dividend_yield = dividend_yield + [0]
        
    earnings_share = earnings_share + [float(company_data[9])]
    
    date = []
    open_ = []
    close = []
    adj_close = []
    low = []    
    high = []
    volume = []
    for day_data in company_data[10]:
        try:
            date = date + [day_data['Date']]
            open_ = open_ + [float(day_data['Open'])]
            close = close + [float(day_data['Close'])]
            adj_close = adj_close + [float(day_data['Adj_Close'])]
            low = low + [float(day_data['Low'])]
            high = high + [float(day_data['High'])]
            volume = volume + [float(day_data['Volume'])]
        except Exception:
            try:
                date = date + [day_data['col0']]
                open_ = open_ + [float(day_data['col1'])]
                close = close + [float(day_data['col4'])]
                adj_close = adj_close + [float(day_data['col4'])]
                low = low + [float(day_data['col3'])]
                high = high + [float(day_data['col2'])]
                volume = volume + [float(day_data['col5'])]
            except Exception:
                print('Error reading historical values of ', company_data[0])
                pass
            
    hist_date = hist_date + [date]
    hist_open = hist_open + [open_]
    hist_close = hist_close + [close]
    hist_adj_Close = hist_adj_Close + [adj_close]
    hist_low = hist_low + [low]
    hist_high = hist_high + [high]
    hist_volume = hist_volume + [volume]
    


    data_user = {'stock_exchange': stock_exchange,\
                 'market_cap': market_cap, 'avg_daily_volume': avg_daily_volume,\
                  'ebitda': ebitda, 'year_lowest_value': year_lowest_value,\
                  'year_highest_value': year_highest_value, 'dividend_share': dividend_share,\
                  'dividend_yield': dividend_yield, 'earnings_share': earnings_share,\
                  'hist_date': hist_date, 'hist_open': hist_open, 'hist_close': hist_close,\
                  'hist_adj_Close': hist_adj_Close, 'hist_low': hist_low,\
                  'hist_high': hist_high, 'hist_volume': hist_volume}
    columns_tweets = ['stock_exchange', 'market_cap', 'avg_daily_volume',\
                  'ebitda', 'year_lowest_value', 'year_highest_value',\
                  'dividend_share', 'dividend_yield', 'earnings_share',\
                  'hist_date', 'hist_open', 'hist_close', 'hist_adj_Close',\
                  'hist_low', 'hist_high', 'hist_volume']
    df_company_data = pd.DataFrame(data_user, columns = columns_tweets)
    df_company_data.index = cashtag
    
    '''
--------------------------------------------------------------------------------
-------------------------------- STORING DATA ----------------------------------
--------------------------------------------------------------------------------
'''

f = open('df_company_data.pckl', 'wb')
pickle.dump(df_company_data, f)
f.close()    

elapsed_time = time.time() - start_time
print('\ntime elapsed storing df_company_data: '+ str(elapsed_time)) 
    
    