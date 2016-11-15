import pandas as pd
import sys
import time
import numpy as np
from SP500_DB import cashtag_list
from collections import Counter
import csv
import datetime
start_time = time.time()


#193.136.221.43
#ps auxwww|grep -i 'get_user_details'

'''
--------------------------------------------------------------------------------
------------------------------ LOADING DATAFRAMES ------------------------------
--------------------------------------------------------------------------------
'''

i=0

df_user_by_company = {}
newpath1 = r'D:\LiClipse Workspace\Project\DATAFRAMES df_user_by_company'
for cashtag in cashtag_list:
    df_user_by_company[cashtag] = pd.read_pickle(newpath1 + '\df_user_by_company'+ cashtag + '.h5')


df_tweets = pd.read_pickle('df_tweets.h5')


elapsed_time = time.time() - start_time
print('\ntime elapsed to read .h5 files: '+ str(elapsed_time))

for cashtag in cashtag_list:
    for line in df_user_by_company[cashtag].itertuples():
        i += 1

print(i)
'''
--------------------------------------------------------------------------------
--------------------------- LOADING DB USER_DETAILS ----------------------------
--------------------------------------------------------------------------------
'''
with open('DB user_details oneweek.csv', 'r', encoding="utf-8") as file:
#with open('DB user_details.csv', 'r', encoding="utf-8") as file:
    reader = csv.reader(file, delimiter=",")
    
    created_at = []
    followers = []
    following = []
    total_nr_of_tweets_ever_done = []
    lists_in = []
    total_nr_of_likes = []

    cashtag = 'initial'
    for line in reader:
        if cashtag == 'initial':
            cashtag = line[0]
            
            created_at = created_at + [line[2]]
            followers = followers + [line[3]]
            following = following + [line[4]]
            total_nr_of_tweets_ever_done = total_nr_of_tweets_ever_done + [line[5]]
            lists_in = lists_in + [line[6]]
            total_nr_of_likes = total_nr_of_likes + [line[7]]
            
        elif line[0] == cashtag:
            created_at = created_at + [line[2]]
            followers = followers + [line[3]]
            following = following + [line[4]]
            total_nr_of_tweets_ever_done = total_nr_of_tweets_ever_done + [line[5]]
            lists_in = lists_in + [line[6]]
            total_nr_of_likes = total_nr_of_likes + [line[7]]
            
        elif line[0] != cashtag:
            
            data_user = {'created_at': created_at, 'followers': followers,\
             'following': following, 'total_nr_of_tweets_ever_done': total_nr_of_tweets_ever_done,\
             'lists_in': lists_in, 'total_nr_of_likes': total_nr_of_likes}
            columns_tweets = ['created_at', 'followers', 'following', 'total_nr_of_tweets_ever_done', 'lists_in',\
                      'total_nr_of_likes']
            df_aux = pd.DataFrame(data_user, columns = columns_tweets)
            
            df_user_by_company[cashtag] = pd.concat([df_user_by_company[cashtag], df_aux], axis=1)
            
            cashtag = line[0]
            
            created_at = []
            followers = []
            following = []
            total_nr_of_tweets_ever_done = []
            lists_in = []
            total_nr_of_likes = []
            
            created_at = created_at + [line[2]]
            followers = followers + [line[3]]
            following = following + [line[4]]
            total_nr_of_tweets_ever_done = total_nr_of_tweets_ever_done + [line[5]]
            lists_in = lists_in + [line[6]]
            total_nr_of_likes = total_nr_of_likes + [line[7]]
        
        else:
            print('Error reading DB user_details.csv')
            sys.exit()
            
    data_user = {'created_at': created_at, 'followers': followers,\
             'following': following, 'total_nr_of_tweets_ever_done': total_nr_of_tweets_ever_done,\
             'lists_in': lists_in, 'total_nr_of_likes': total_nr_of_likes}
    columns_tweets = ['created_at', 'followers', 'following', 'total_nr_of_tweets_ever_done', 'lists_in',\
                      'total_nr_of_likes']
    df_aux = pd.DataFrame(data_user, columns = columns_tweets)
            
    df_user_by_company[cashtag] = pd.concat([df_user_by_company[cashtag], df_aux], axis=1)        



elapsed_time = time.time() - start_time
print('\ntime elapsed loading user_details file and filling df_user_by_company: '+ str(elapsed_time))

'''
--------------------------------------------------------------------------------
----------------------- PREPARING df_features_by_user_by_company -----------------------
--------------------------------------------------------------------------------
'''
col = ['user_name', 'account_duration', 'account_activity', 'popularity', 'topic_connection',\
           'likes', 'hashtags', 'retweets_by_tweets', 'retweets_by_user', 'mentions', 'talk'] 

df_features_by_user_by_company = {}

elapsed_time = time.time() - start_time
print('\ntime elapsed creating df_features_by_user_by_company empty: '+ str(elapsed_time))


'''
--------------------------------------------------------------------------------
--------------------------------- SIMILARITY -----------------------------------
--------------------------------------------------------------------------------
'''
''' SIMILARITY
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
'''
'''
--------------------------------------------------------------------------------
------------------------------- CLASS FEATURES ---------------------------------
--------------------------------------------------------------------------------
'''
class features:
    def calc_account_duration_days(self, time_stamp):
        start = datetime.datetime.strptime(time_stamp, '%Y-%m-%d %H:%M:%S')
        ends = datetime.datetime.now()
        return (ends - start).days
    
    def calc_account_activity(self, total_nr_of_tweets_ever_done, account_duration):
        print('entrou')
        a = total_nr_of_tweets_ever_done/account_duration
        print(a)
        return total_nr_of_tweets_ever_done/account_duration

        
'''
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
'''  

'''
--------------------------------------------------------------------------------
----------------- CREATION OF DF_FEATURES_BY_USER_BY_COMPANY -------------------
--------------------------------------------------------------------------------
'''            
cashtag_list = ['$IRM']    
for cashtag in cashtag_list:
    names = []
    account_duration = []
    account_activity = []
    popularity = []
    topic_connection = []
    likes = []
    hashtags = []
    retweets_by_tweets = []
    retweets_by_user = []
    mentions = []
    talk = []
    for line in df_user_by_company[cashtag].itertuples():
        try:
            names = names + [line[1]]
            
            new_account_duration = features().calc_account_duration_days(line[13])
            account_duration = account_duration + [new_account_duration]
            #print(new_account_duration)
            #print(features().calc_account_activity(line[16], new_account_duration))
            account_activity = account_activity + [features().calc_account_activity(line[16], new_account_duration)]
            #popularity = popularity + [features().calc_topic_attitude(line[13], line[4])]
            #topic_connection = topic_connection + [features().calc_no_talk(line[13], line[14])]
            #likes = likes + [features().calc_retweets(line[5], line[6])]
            #hashtags = hashtags + [features().calc_mentions(line[9], line[10], line[11], line[12])]
            #retweets_by_tweets = retweets_by_tweets + [features().calc_hashtags(line[13], line[8])]
            #retweets_by_user = retweets_by_user + [features().find_score_for_a_user(line[1])]   
            #mentions = mentions + [features().calc_topic_tweets_ratio(line[13], line[8])]
            #talk = talk + [features().calc_topic_tweets_ratio(line[13], line[8])]
        except Exception:
            names = names + [line[1]]
            account_duration = account_duration + [0]
            account_activity = account_activity + [0]
            #print(cashtag, line[1])
                 
    data_user = {'user_name': names, 'account_duration': account_duration, 'account_activity': account_activity,\
                 'popularity': 0, 'topic_connection': 0, 'likes': 0,\
                 'hashtags': 0, 'retweets_by_tweets': 0,\
                 'retweets_by_user': 0, 'mentions': 0, 'talk': 0} 
    try:
        df_features_by_user_by_company[cashtag] = pd.DataFrame(data_user, columns = col)       
    except Exception:
        pass
        #print(cashtag)
    
print(df_features_by_user_by_company['$IRM'])

elapsed_time = time.time() - start_time
print('\ntime elapsed filling df_features_by_user_by_company: '+ str(elapsed_time))

sys.exit()

'''
--------------------------------------------------------------------------------
-------------------------- SAVING FILES IN .h5 FORMAT --------------------------
--------------------------------------------------------------------------------
'''
newpath = r'D:\LiClipse Workspace\Project\DATAFRAMES df_features_by_user_by_company'

for cashtag in cashtag_list:
    df_features_by_user_by_company[cashtag].to_pickle(newpath + '\df_features_by_user_by_company'+ cashtag + '.h5')


elapsed_time = time.time() - start_time
print('\ntime elapsed saving files of df_features_by_user_by_company: '+ str(elapsed_time))


