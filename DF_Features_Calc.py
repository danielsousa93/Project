import pandas as pd
import sys
import time
import numpy as np
from SP500_DB import cashtag_list
import csv
import datetime
start_time = time.time()

#cashtag_list = cashtag_list[:4]
#cashtag_list = ['$A']

#193.136.221.43
#ps auxwww|grep -i 'get_user_details'


'''
--------------------------------------------------------------------------------
--------------------------- CALCULATE COLLECT PERIOD ---------------------------
--------------------------------------------------------------------------------
'''

with open('tweetsDB - newfromremote onemonth.csv', 'r', encoding="utf-8") as file:
    reader = csv.reader(file, delimiter=",")
    min_date = datetime.datetime.now()
    max_date = datetime.datetime.now() - datetime.timedelta(days=3650)
    for line in reader:
        try:
            line_date = datetime.datetime.strptime(line[2], '%Y-%m-%d %H:%M:%S')
        except Exception:
            pass
        
        if line_date < min_date:
            min_date = line_date
        if line_date > max_date:
            max_date = line_date
            
    collect_period = (max_date - min_date).days


elapsed_time = time.time() - start_time
print('\ntime elapsed calculating collect_period: '+ str(elapsed_time))   

'''
--------------------------------------------------------------------------------
------------------------------ LOADING DATAFRAMES ------------------------------
--------------------------------------------------------------------------------
'''
df_user_by_company = {}
newpath1 = r'D:\LiClipse Workspace\Project\DATAFRAMES df_user_by_company'
for cashtag in cashtag_list:
    df_user_by_company[cashtag] = pd.read_pickle(newpath1 + '\df_user_by_company'+ cashtag + '.h5')
    
#df_tweets = pd.read_pickle('df_tweets.h5')

elapsed_time = time.time() - start_time
print('\ntime elapsed to read .h5 files: '+ str(elapsed_time))

'''
--------------------------------------------------------------------------------
--------------------------- LOADING DB USER_DETAILS ----------------------------
--------------------------------------------------------------------------------
'''
with open('DB user_details onemonth.csv', 'r', encoding="utf-8") as file:
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
            print('Cashtag ' + cashtag + ' done.')
            
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
       'likes', 'hashtags', 'retweets_by_tweet', 'retweets_by_user', 'mentions_by_tweet',\
       'mentions_by_user', 'talk'] 

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
        return int(total_nr_of_tweets_ever_done)/int(account_duration)
    
    def calc_popularity(self, followers, following):
        return int(followers) / (int(followers) + int(following))
    
    def calc_topic_connection(self, tweets_on_topic, tweets_on_that_period):
        return tweets_on_topic / tweets_on_that_period
    
    def calc_likes(self, nr_of_likes_in_period, total_nr_of_likes_made, account_duration, collect_period):
        value = nr_of_likes_in_period / (int(total_nr_of_likes_made)*collect_period/account_duration + 1)
        if np.isnan(value):
            return 0
        else:
            return value
    
    def calc_hashtags(self, nr_dif_hashtags):
        if nr_dif_hashtags == 0:
            return 0
        else:
            return 1 / nr_dif_hashtags

    def calc_retweets_by_tweet(self, nr_of_dif_tweets_retweeted, nr_of_tweets_on_topic):
        return nr_of_dif_tweets_retweeted / nr_of_tweets_on_topic
    
    def calc_retweets_by_user(self, nr_of_dif_users_that_retweeted, nr_of_tweets_on_topic):
        return nr_of_dif_users_that_retweeted / nr_of_tweets_on_topic
    
    def calc_mentions_by_tweet(self, nr_of_mentions_done_to_the_user, nr_of_mentions_done_by_the_user):
        value = nr_of_mentions_done_to_the_user / (nr_of_mentions_done_by_the_user + 1)
        if np.isnan(value):
            return 0
        else:
            return value
    
    def calc_mentions_by_user(self, nr_of_dif_users_that_metioned_the_user, nr_of_dif_users_mentioned_by_the_user):
        value = nr_of_dif_users_that_metioned_the_user / (nr_of_dif_users_mentioned_by_the_user + 1)
        if np.isnan(value):
            return 0
        else:
            return value
    
    def calc_talk(self, nr_of_conversation_tweets_done_by_the_user, nr_of_tweets_on_topic):
        return nr_of_tweets_on_topic / (3*nr_of_conversation_tweets_done_by_the_user + 1)
    
'''
--------------------------------------------------------------------------------
----------------- CREATION OF DF_FEATURES_BY_USER_BY_COMPANY -------------------
--------------------------------------------------------------------------------
'''               
for cashtag in cashtag_list:
    names = []
    account_duration = []
    account_activity = []
    popularity = []
    topic_connection = []
    likes = []
    hashtags = []
    retweets_by_tweet = []
    retweets_by_user = []
    mentions_by_tweet = []
    mentions_by_user = []
    talk = []
    for line in df_user_by_company[cashtag].itertuples():
        try:
            names = names + [line[1]]
        except Exception:
            names = names + [line[1]]
        
        try:
            new_account_duration = features().calc_account_duration_days(line[13])
            account_duration = account_duration + [new_account_duration]
        except Exception:
            account_duration = account_duration + [0]
            
        try:  
            account_activity = account_activity + [features().calc_account_activity(line[16], new_account_duration)]
        except Exception:
            account_activity = account_activity + [0]
        
        try:
            popularity = popularity + [features().calc_popularity(line[14], line[15])]
        except Exception:
            popularity = popularity + [0]
            
        try:
            topic_connection = topic_connection + [features().calc_topic_connection(line[2], line[12])]
        except Exception:
            topic_connection = topic_connection + [0]
             
        try:
            likes = likes + [features().calc_likes(line[11], line[18], new_account_duration, collect_period)]
        except Exception:
            likes = likes + [0]
                
        try:
            hashtags = hashtags + [features().calc_hashtags(line[5])]
        except Exception:
            hashtags = hashtags + [0]
            
        try:
            retweets_by_tweet = retweets_by_tweet + [features().calc_retweets_by_tweet(line[4], line[2])]
        except Exception:
            retweets_by_tweet = retweets_by_tweet + [0]
            
        try:
            retweets_by_user = retweets_by_user + [features().calc_retweets_by_user(line[3], line[2])]   
        except Exception:
            retweets_by_user = retweets_by_user + [0]
            
        try:
            mentions_by_tweet = mentions_by_tweet + [features().calc_mentions_by_tweet(line[8], line[6])]
        except Exception:
            mentions_by_tweet = mentions_by_tweet + [0]
            
        try:
            mentions_by_user = mentions_by_user + [features().calc_mentions_by_user(line[9], line[7])]
        except Exception:
            mentions_by_user = mentions_by_user + [0]
            
        try:
            talk = talk + [features().calc_talk(line[10], line[2])]
        except Exception:
            talk = talk + [0]
        
                
    data_user = {'user_name': names, 'account_duration': account_duration, 'account_activity': account_activity,\
                 'popularity': popularity, 'topic_connection': topic_connection, 'likes': likes,\
                 'hashtags': hashtags, 'retweets_by_tweet': retweets_by_tweet,\
                 'retweets_by_user': retweets_by_user, 'mentions_by_tweet': mentions_by_tweet,\
                 'mentions_by_user': mentions_by_user, 'talk': talk} 
    
    try:
        df_features_by_user_by_company[cashtag] = pd.DataFrame(data_user, columns = col)   
        print('Creation with success df_feature_by_user_by_company for ' + cashtag)
    except Exception:
        #pass
        print('Error creating df_feature_by_user_by_company for ' + cashtag)
    
    #df_features_by_user_by_company[cashtag] = pd.DataFrame(data_user, columns = col)     

elapsed_time = time.time() - start_time
print('\ntime elapsed filling df_features_by_user_by_company: '+ str(elapsed_time))
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

print(df_features_by_user_by_company['$MMM'])
