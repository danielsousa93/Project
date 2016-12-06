import time
import pickle
import sys
import pandas as pd
from SP500_DB import cashtag_list

#193.136.221.43

start_time = time.time()

'''
--------------------------------------------------------------------------------
-------------------------------- LOADING DATA ----------------------------------
--------------------------------------------------------------------------------
'''
f = open('df_company_data.pckl', 'rb')
df_company_data = pickle.load(f)
f.close()

f = open('df_tweets_by_company_with_sentiment_analysis.pckl', 'rb')
df_tweets_by_company_updated = pickle.load(f)
f.close()

elapsed_time = time.time() - start_time
print('\ntime elapsed loading data: '+ str(elapsed_time)) 


'''
--------------------------------------------------------------------------------
----------------------- CREATE DF_COLLECTION_BY_COMPANY ------------------------
--------------------------------------------------------------------------------
'''
(date_set,hist_adj_close) = df_company_data[['hist_date', 'hist_adj_close']].ix['$FB']


df_collection_by_company = {}
for cashtag in cashtag_list:
    df_collection_by_company[cashtag] = pd.DataFrame(0, index=date_set, columns=['sentiment_coef'])

#print(df_collection_by_company['$ZTS'])
#sys.exit()

#print(df_tweets_by_company_updated['$ZTS'])

#print(df_collection_by_company['$FB']['sentiment_coef'].ix['2016-11-01'])
#sys.exit()

cashtag_list = cashtag_list[:5]

for cashtag in cashtag_list:
    i=0
    for line in df_tweets_by_company_updated[cashtag].itertuples():
        date = line[2]
        try:
            if date[:10] in date_set:
                df_collection_by_company[cashtag]['sentiment_coef'].ix[date[:10]] = line[5] + df_collection_by_company[cashtag]['sentiment_coef'].ix[date[:10]]
            else:
                old_date = '2018-12-25'
                for date_inst in date_set:
                    if date_inst > date[:10]:
                        old_date = date_inst
                    else: 
                        df_collection_by_company[cashtag]['sentiment_coef'].ix[old_date] = line[5] + df_collection_by_company[cashtag]['sentiment_coef'].ix[old_date]
        except Exception:
            if i == 0:
                print(cashtag)
                i = 1
        
elapsed_time = time.time() - start_time
print('\ntime elapsed creating df_collection_by_company: '+ str(elapsed_time))                 


#sys.exit()
f = open('df_collection_by_company.pckl', 'wb')
pickle.dump(df_collection_by_company, f)
f.close() 

#print(df_collection_by_company['$MMM'][df_collection_by_company['$MMM']['sentiment_coef'] != 0])

 

