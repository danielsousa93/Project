import pandas as pd
import time
import nltk
import nltk.sentiment
from SP500_DB import cashtag_list
from nltk.corpus import twitter_samples

start_time = time.time()


df_tweets = pd.read_pickle('df_tweets.h5')
df_tweets_company = {}
df_user_by_company = {}
df_features_by_company = {}
for cashtag in cashtag_list:
    df_tweets_company[cashtag] = pd.read_pickle('df_tweets_company' + cashtag + '.h5')
    df_user_by_company[cashtag] = pd.read_pickle('df_user_by_company'+ cashtag + '.h5')
    df_features_by_company[cashtag] = pd.read_pickle('df_features_by_company'+ cashtag + '.h5')


elapsed_time = time.time() - start_time
print('\ntime elapsed to read .h5 files: '+ str(elapsed_time))
twitter_samples.fileids()
print(twitter_samples)
#print(df_tweets_company['$WFC'])
#print(df_features_by_company['$WFC'])