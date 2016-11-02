import pandas as pd
import time
import numpy as np
from SP500_DB import cashtag_list
from collections import Counter

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

unique_names = df_tweets['user_name'].unique()



old_user_name = []
words_list = []
score_array = []
old_user_name_array = []
i=0
for line in df_tweets.sort_values(by=['user_name', 'tweet_date']).itertuples():
    text = line[4]
    if line[1] != old_user_name:
        if i > 0:
            count = Counter(words_list).values()
            if len(count) == 0:
                score = 0
            else:
                score = 1 - ((sum(count) - len(count)) / len(count))
        else:
            score = 0        
        
        old_user_name_array = old_user_name_array + [old_user_name]
        score_array = score_array + [score]
        

        old_user_name = line[1]
        words_list = []
        for word in text.split():
            if word[0] != '$' and word[0] != '#' and ('⛱' not in word) and word[0] != '@' and word != 'RT' and word[1:8] != 'ttps://':
                words_list = [word] + words_list
        i = 0
    else:
        i += 1  
        for word in text.split():
            if word[0] != '$' and word[0] != '#' and word[0] != '@' and word != 'RT' and word[1:8] != 'ttps://':
                words_list = [word] + words_list
            

data_score = {'user_name': old_user_name_array, 'score': score_array}
df_score = pd.DataFrame(data_score)
df_score = df_score.ix[1:]
elapsed_time = time.time() - start_time
print('\ntime elapsed creating df_scores: '+ str(elapsed_time))


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
        
    def calc_mentions(self, nr_of_mentions_done_by_the_user, nr_of_dif_users_mentioned_by_the_user, nr_of_mentions_done_to_the_user, nr_of_dif_users_that_metioned_the_user):
        if (nr_of_mentions_done_by_the_user == 0 or nr_of_dif_users_mentioned_by_the_user == 0) and (nr_of_mentions_done_to_the_user == 0 or nr_of_dif_users_that_metioned_the_user == 0):
            return 0
        elif nr_of_mentions_done_by_the_user == 0 or nr_of_dif_users_mentioned_by_the_user == 0:
            return nr_of_mentions_done_to_the_user*(np.log10(nr_of_dif_users_that_metioned_the_user)) 
        elif nr_of_mentions_done_to_the_user == 0 or nr_of_dif_users_that_metioned_the_user == 0:
            return -nr_of_mentions_done_by_the_user*(np.log10(nr_of_dif_users_mentioned_by_the_user)) 
        else:
            return nr_of_mentions_done_to_the_user*(np.log10(nr_of_dif_users_that_metioned_the_user)) - nr_of_mentions_done_by_the_user*(np.log10(nr_of_dif_users_mentioned_by_the_user))
    
    def calc_hashtags(self, nr_of_original_tweets_done, nr_dif_hashtags):
        return (nr_of_original_tweets_done - nr_dif_hashtags + 1) / nr_of_original_tweets_done 
    
    def calc_topic_tweets_ratio(self, nr_of_original_tweets_done, nr_dif_hashtags):
        return nr_of_original_tweets_done / nr_dif_hashtags       
    
    def find_score_for_a_user(self, user_name):  
        return df_score.loc[df_score['user_name'] == user_name, 'score'].tolist()
        
#print(df_score)  
    
#print(df_user_by_company['$WFC'])       
              
for cashtag in cashtag_list:
    names = []
    topic_connection = []
    topic_attitude = []
    no_talk = []
    retweets = []
    mentions = []
    hashtags = []
    no_similarity_between_tweets = []
    topic_tweets_ratio = []
    for line in df_user_by_company[cashtag].itertuples():
        names = names + [line[1]]
        topic_connection = topic_connection + [features().calc_topic_connection(line[13], line[14], line[4], line[2])]
        topic_attitude = topic_attitude + [features().calc_topic_attitude(line[13], line[4])]
        no_talk = no_talk + [features().calc_no_talk(line[13], line[14])]
        retweets = retweets + [features().calc_retweets(line[5], line[6])]
        mentions = mentions + [features().calc_mentions(line[9], line[10], line[11], line[12])]
        hashtags = hashtags + [features().calc_hashtags(line[13], line[8])]
        no_similarity_between_tweets = no_similarity_between_tweets + [features().find_score_for_a_user(line[1])]   
        topic_tweets_ratio = topic_tweets_ratio + [features().calc_topic_tweets_ratio(line[13], line[8])]
        
                  
    data_user = {'user_name': names, 'topic_connection': topic_connection, 'topic_attitude': topic_attitude, 'no_talk': no_talk, 'retweets': retweets,\
                 'mentions': mentions, 'hashtags': hashtags, 'no_similarity_between_tweets': no_similarity_between_tweets, 'topic_tweets_ratio': topic_tweets_ratio} 
    
    df_features_by_company[cashtag] = pd.DataFrame(data_user, columns = col)       
        #topic_connection = topic_connection + [features().calc_topic_connection(line[13], line[14], line[4], line[2])]


#for name, df in df_companies.items():
    #print(name)
    # operate on DataFrame df for company name

#print(df_companies['$MMM'].loc[df_companies['$MMM']['user_name'] == 'DougKass', 'topic_attitude'])
#print(df_features_by_company['$WFC'][:100])

elapsed_time = time.time() - start_time
print('\ntime elapsed filling df_features_by_company: '+ str(elapsed_time))

for cashtag in cashtag_list:
    df_features_by_company[cashtag].to_pickle('df_features_by_company'+ cashtag + '.h5')


elapsed_time = time.time() - start_time
print('\ntime elapsed saving file of df_features_by_company: '+ str(elapsed_time))