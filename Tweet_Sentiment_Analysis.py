import pandas as pd
import time
from SP500_DB import cashtag_list

start_time = time.time()


df_tweets = pd.read_pickle('df_tweets.h5')
df_user_by_company = {}
df_tweets_company = {}
df_features_by_company = {}
for cashtag in cashtag_list:
    df_tweets_company[cashtag] = pd.read_pickle('df_tweets_company' + cashtag + '.h5')
    df_user_by_company[cashtag] = pd.read_pickle('df_user_by_company'+ cashtag + '.h5')
    df_features_by_company[cashtag] = pd.read_pickle('df_features_by_company'+ cashtag + '.h5')


elapsed_time = time.time() - start_time
print('\ntime elapsed to read .h5 files: '+ str(elapsed_time))


print(df_tweets_company['$WFC'])
#print(df_features_by_company['$WFC'])