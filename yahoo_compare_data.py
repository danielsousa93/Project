import time
import pickle
from pprint import pprint
import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from SP500_DB import cashtag_list

#193.136.221.43
bound = 0.2
start_time = time.time()

'''
--------------------------------------------------------------------------------
-------------------------------- LOADING DATA ----------------------------------
--------------------------------------------------------------------------------
'''
f = open('df_collection_by_company.pckl', 'rb')
df_collection_by_company = pickle.load(f)
f.close()

f = open('df_company_data.pckl', 'rb')
df_company_data = pickle.load(f)
f.close()

f = open('df_tweets_by_company_with_sentiment_analysis.pckl', 'rb')
df_tweets_by_company_updated = pickle.load(f)
f.close()

elapsed_time = time.time() - start_time
print('\ntime elapsed loading data: '+ str(elapsed_time)) 

#print(df_tweets['$MMM' in df_tweets['hashtags_list']])

'''
--------------------------------------------------------------------------------
------------ CREATE COLUMN WITH TWEET DAY & GET HISTORICAL VALUES --------------
--------------------------------------------------------------------------------
'''
#cashtag_list = ['$MMM']
cashtag_list = cashtag_list[:5]

companies_hist_adj_close = {}

for cashtag in cashtag_list:
    tweet_day = []
    for line in df_tweets_by_company_updated[cashtag].itertuples():
        tweet_day = tweet_day + [line[2][:10]]
    df_tweets_by_company_updated[cashtag]['tweet_day'] = tweet_day
    #print(df_tweets_by_company_updated['$MMM'])
    #sys.exit()
     
    try:
        companies_hist_adj_close[cashtag] = df_company_data['hist_adj_close'].ix[cashtag]
    except Exception:
        print('ERROR: ', cashtag)
        pass


'''
--------------------------------------------------------------------------------
-------- CREATE NEW DATAFRAME WITH THE DAILY SENTIMENT COEFICIENT SUM ----------
--------------------------------------------------------------------------------
'''   
new_df = {}
for cashtag in cashtag_list:
    new_df[cashtag] = df_tweets_by_company_updated[cashtag][['user_name','tweet_day', 'sentiment_coef']].groupby(['user_name','tweet_day']).sum().copy()

#print(new_df['$MMM'])
#sys.exit()

for cashtag in cashtag_list:
    sentiment_classification = []
    for value in new_df[cashtag]['sentiment_coef']:
        if -0.2 < value < 0.2:
            sentiment_classification = sentiment_classification + ['neutral']
        elif value > 0.2:
            sentiment_classification = sentiment_classification + ['positive']
        else:
            sentiment_classification = sentiment_classification + ['negative']
    
    new_df[cashtag]['sentiment'] = sentiment_classification
    
#print(new_df['$MMM'])
#sys.exit()

'''
--------------------------------------------------------------------------------
------------------ CREATE CHANGE_ADJ_CLOSE FOR EACH CASHTAG --------------------
--------------------------------------------------------------------------------
'''
date_set = df_company_data['hist_date'].ix['$FB']
companies_hist_adj_close = {}
change_adj_close = {}
change_adj_close_per = {}
for cashtag in cashtag_list:
    try:
        companies_hist_adj_close[cashtag] = df_company_data['hist_adj_close'].ix[cashtag]
    
        change_adj_close[cashtag] = [(0, date_set[0])]
        change_adj_close_per[cashtag] = [(0, date_set[0])]
        
        for i in range(0,len(companies_hist_adj_close[cashtag])-1):
            value = companies_hist_adj_close[cashtag][i+1] - companies_hist_adj_close[cashtag][i]
            change_adj_close[cashtag].append((value, date_set[i+1]))
            change_adj_close_per[cashtag].append((value/companies_hist_adj_close[cashtag][i], date_set[i+1]))
    
        change_adj_close[cashtag] = np.array(change_adj_close[cashtag])
        change_adj_close_per[cashtag] = np.array(change_adj_close_per[cashtag])
    
    except Exception:
        print('ERROR: ', cashtag)
        pass

#print(change_adj_close['$MMM'][0][1])
#print(change_adj_close['$MMM'])
#sys.exit()


'''
--------------------------------------------------------------------------------
------------------ CREATE CHANGE_ADJ_CLOSE FOR EACH CASHTAG --------------------
--------------------------------------------------------------------------------
'''
for cashtag in cashtag_list:
    for line in new_df[cashtag].itertuples():
        date = line[0][1]
        for pair in change_adj_close_per[cashtag]:
        #for pair in change_adj_close[cashtag]:
            if pair[1] == date:
                #print(line[0][0], date, line[2], pair[0])
                a = 1



print(df_collection_by_company['$MMM'])
print(df_company_data.ix['$MMM'])
print(new_df)

sys.exit()
'''
--------------------------------------------------------------------------------
------------------------------ DATA FOR IMAGES ---------------------------------
--------------------------------------------------------------------------------
'''

date_set = df_company_data['hist_date'].ix['$FB']

companies_hist_adj_close = {}
for cashtag in cashtag_list:
    try:
        companies_hist_adj_close[cashtag] = df_company_data['hist_adj_close'].ix[cashtag]
    except Exception:
        print('ERROR: ', cashtag)
        pass


hist_adj_close = {}
sentiment_data_set = {}
min_array = np.empty(8)
cashtag_array = []
for i in range(0,8):
    min = 100
    for cashtag in cashtag_list:
        val = df_collection_by_company[cashtag]['sentiment_coef'].ix['2016-11-11':'2016-11-04'].sum()
        if val < min:
            min = val
            min_cashtag = cashtag
    cashtag_list.remove(min_cashtag)
    min_array[i] = min
    cashtag_array = cashtag_array + [min_cashtag] 
    
    sentiment_data_set[min_cashtag] = np.array(df_collection_by_company[min_cashtag]['sentiment_coef'])
    hist_adj_close[min_cashtag] = np.array(companies_hist_adj_close[min_cashtag])
       

'''
--------------------------------------------------------------------------------
----------------------------- COMPARATION IMAGES -------------------------------
--------------------------------------------------------------------------------
'''
date_set = np.array(date_set)

'''
change_adj_close = {}
for cashtag in cashtag_array:
    change_adj_close[cashtag] = [0]
    for i in range(0,len(hist_adj_close[cashtag])-2):
        change_adj_close[cashtag].append(hist_adj_close[cashtag][i+1] - hist_adj_clos[cashtag]e[i])

    change_adj_close[cashtag] = np.array(change_adj_close[cashtag])
'''

y = np.empty(len(hist_adj_close[cashtag_array[0]]))
y.fill(0)


for cashtag in cashtag_array:
    plt.figure()
    
    plt.title(cashtag)
    plt.plot(hist_adj_close[cashtag], 'b-',\
             sentiment_data_set[cashtag] , 'g-',\
             y, 'r-')
    plt.show()

'''
--------------------------------------------------------------------------------
------------------------------ DATAFRAME IMAGES --------------------------------
--------------------------------------------------------------------------------
'''
sys.exit()
#print(df_company_data.sort_values(by='earnings_share', ascending=0))
#print(df_company_data[df_company_data['cashtag'] == '$XRAY'])


a = df_company_data[['market_cap']].sort_values(by='market_cap', ascending=0)[:10].plot(kind='bar')


b = df_company_data[['market_cap']].sort_values(by='market_cap', ascending=0)[:20].plot(kind='bar')

plt.show(a and b)