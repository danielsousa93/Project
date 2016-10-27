import pandas as pd
import time
import numpy as np
from SP500_DB import cashtag_list
start_time = time.time()


df_tweets = pd.read_pickle('df_tweets.h5')
df_user_by_company = {}
df_tweets_company = {}
for cashtag in cashtag_list:
    df_tweets_company[cashtag] = pd.read_pickle('df_tweets_company' + cashtag + '.h5')
    df_user_by_company[cashtag] = pd.read_pickle('df_user_by_company'+ cashtag + '.h5')

elapsed_time = time.time() - start_time
print('\ntime elapsed to read .h5 files: '+ str(elapsed_time))

col = ['user_name', 'topic_connection', 'topic_attitude', 'no_talk', 'retweets', 'mentions', 'hashtags',\
           'no_similarity_between_tweets', 'topic_tweets_ratio']

df_features_by_company = {}
#for cashtag in cashtag_list:
#    df_features_by_company[cashtag] = pd.DataFrame(columns=col)

elapsed_time = time.time() - start_time
print('\ntime elapsed creating df_features_by_company empty: '+ str(elapsed_time))




class features:
    def calc_topic_connection(self, nr_of_original_tweets_done, nr_of_conversation_tweets_done_by_the_user, nr_of_retweets_done, nr_of_tweets):
        return (nr_of_original_tweets_done + nr_of_conversation_tweets_done_by_the_user + nr_of_retweets_done)/nr_of_tweets
    
    def calc_topic_attitude(self, nr_of_original_tweets_done, nr_of_retweets_done):
        return nr_of_original_tweets_done / (nr_of_original_tweets_done + nr_of_retweets_done)
    
    def calc_no_talk(self, nr_of_original_tweets_done, nr_of_conversation_tweets_done_by_the_user):
        if nr_of_original_tweets_done == 0:
            return 0
        else:
            return nr_of_original_tweets_done / (nr_of_original_tweets_done + nr_of_conversation_tweets_done_by_the_user)
    
    def calc_retweets(self, nr_retweet_dif_users, nr_of_dif_tweets_retweeted):
        if nr_retweet_dif_users == 0 or nr_of_dif_tweets_retweeted == 0: 
            return 0
        else:
            return nr_of_dif_tweets_retweeted*(np.log10(nr_retweet_dif_users))

for cashtag in cashtag_list:
    names = []
    topic_connection = []
    topic_attitude = []
    no_talk = []
    retweets = []
    for line in df_user_by_company[cashtag].itertuples():
        names = names + [line[1]]
        topic_connection = topic_connection + [features().calc_topic_connection(line[13], line[14], line[4], line[2])]
        topic_attitude = topic_attitude + [features().calc_topic_attitude(line[13], line[4])]
        no_talk = no_talk + [features().calc_no_talk(line[13], line[14])]
        retweets = retweets + [features().calc_retweets(line[5], line[6])]
                    #row = [1,2,1,1,1,1,1,1,1]
                    #df_companies[cashtag].loc[len(df_features)] = row
                    #df_companies[cashtag]
                    #df.loc[len(df)] = row
                  
    data_user = {'user_name': names, 'topic_connection': topic_connection, 'topic_attitude': topic_attitude, 'no_talk': no_talk, 'retweets': retweets, 'mentions': 0, 'hashtags': 0,\
           'no_similarity_between_tweets': 0, 'topic_tweets_ratio': 0} 
    
    df_features_by_company[cashtag] = pd.DataFrame(data_user, columns = col)       
        #topic_connection = topic_connection + [features().calc_topic_connection(line[13], line[14], line[4], line[2])]
    
'''
data = {'user_name': user_names[:3], 'topic_connection': 0, 'topic_attitude': 0, 'no_talk': 0, 'retweets':0, 'mentions': 0, 'hashtags': 0,\
        'no_similarity_between_tweets': 0, 'topic_tweets_ratio': 0}
columns = ['user_name', 'topic_connection', 'topic_attitude', 'no_talk', 'retweets', 'mentions', 'hashtags',\
           'no_similarity_between_tweets', 'topic_tweets_ratio']
''' 
#df_features = pd.DataFrame(data)
#df_features = df_features[columns]



#for name, df in df_companies.items():
    #print(name)
    # operate on DataFrame df for company name

#print(df_companies['$MMM'].loc[df_companies['$MMM']['user_name'] == 'DougKass', 'topic_attitude'])
print(df_features_by_company['$MMM'][:10])

elapsed_time = time.time() - start_time
print('\ntime elapsed filling df_features_by_company: '+ str(elapsed_time))