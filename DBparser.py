import csv
import pandas as pd
import time
import re
import numpy as np
from lib2to3.fixes.fix_asserts import NAMES
start_time = time.time()

with open('tweetsDB - Backup.csv', 'r', encoding="utf-8") as file:
    reader = csv.reader(file, delimiter=",")
    
    user_names = []
    user_followers = []
    tweet_date = []
    tweet_text = []
    for line in reader:
        user_names = user_names + [line[0]]
        user_followers = user_followers + [line[1]]
        tweet_date = tweet_date + [line[2]]
        tweet_text = tweet_text + [line[3]]

'''#COUNT NUMBER OF TWEETS
with open('tweetsDB - Backup.csv', 'r', encoding="utf-8") as file:
    reader = csv.reader(file, delimiter=",")
    row_count = sum(1 for line in reader)        
print('nr of rows:%d' % row_count)
print('user_names:%d' % len(user_names))
print('users_followers:%d' % len(user_followers))
print('tweet_date:%d' % len(tweet_date))
print('tweet_text:%d' % len(tweet_text))
'''

class tweet_parser:
    def calc_nr_links_shared(self, text):
        return text.count("ttps://")
         
    def detect_retweets(self, text):
        if text[:4] == 'RT @': 
            user_name = text.split()[1]
            user_name = user_name[1:len(user_name)-1]
            user_name = re.sub('[^a-zA-Z0-9 \n\_]', '', user_name)
            return (1, user_name) 
        else:
            return (0,'null') 
        
    def identify_hashtags(self, text):
        words_array = []
        if text[:4] != 'RT @': 
            for word in text.split():
                if (word[0] == '$' or word[0] == '#') and (len(word) > 1) and not word[1].isdigit():
                    word = re.sub('[^a-zA-Z0-9 \n\$#]', '', word)
                    words_array = words_array + [word]
        return words_array  

    def detect_mentions(self, text):
        if text[:4] != 'RT @': 
            list_users_mentioned = []
            for word in text.split():
                if word[0] == '@' and len(word) > 1:
                    word = re.sub('[^a-zA-Z0-9 \n\_]', '', word)
                    list_users_mentioned = list_users_mentioned + [word]
                    df_tweets.loc[df_tweets['user_name'] == word, 'mentions_done_with_him'] +=1
                    
            return (len(list_users_mentioned), list_users_mentioned) 
        else:
            return (0, [])
        

data_tweets = {'user_name': user_names, 'user_followers': user_followers, 'tweet_date': tweet_date, 'tweet_text': tweet_text,\
               'retweets_flag': 0, 'ret_orig_user': 0, 'hashtags_list': 0, 'users_mentioned': 0, 'nr_of_users_mentioned': 0, 'mentions_done_with_him': 0}
df_tweets = pd.DataFrame(data_tweets)
columns_tweets = ['user_name', 'user_followers', 'tweet_date', 'tweet_text', 'retweets_flag', 'ret_orig_user', 'hashtags_list', 'users_mentioned'\
                  , 'nr_of_users_mentioned', 'mentions_done_with_him']
df_tweets = df_tweets[columns_tweets]


unique_names = df_tweets['user_name'].unique()


orig_user_of_tweet = []
retweets_flag = []
nr_of_links_shared = []
hashtags_list = []
users_mentioned = []
nr_of_users_mentioned = []

for tweet in df_tweets['tweet_text']:
    #nr_of_links_shared = nr_of_links_shared + [tweet_parser().calc_nr_links_shared(tweet)]
    retweets_flag = retweets_flag + [tweet_parser().detect_retweets(tweet)[0]]
    orig_user_of_tweet = orig_user_of_tweet + [tweet_parser().detect_retweets(tweet)[1]]
    hashtags_list = hashtags_list + [tweet_parser().identify_hashtags(tweet)]
    (new_nr_of_users_mentioned,new_users_mentioned) = tweet_parser().detect_mentions(tweet)
    users_mentioned = users_mentioned + [new_users_mentioned]
    nr_of_users_mentioned = nr_of_users_mentioned + [new_nr_of_users_mentioned]

    
df_tweets['retweets_flag'] = retweets_flag
df_tweets['ret_orig_user'] = orig_user_of_tweet
df_tweets['hashtags_list'] = hashtags_list
df_tweets['users_mentioned'] = users_mentioned
df_tweets['nr_of_users_mentioned'] = nr_of_users_mentioned


#print(df_tweets[df_tweets['user_name'] == 'JustinPulitzer'])

    
    






class user_details:
    def calc_nr_tweets(self, user_name):
        return df_tweets['user_name'].value_counts()[user_name]

    def set_tweet_indexes(self, user_name):
        return df_tweets[df_tweets['user_name'] == user_name].index.tolist()
        
    def calc_nr_retweets_done(self, user_name):
        return df_tweets.loc[df_tweets['user_name'] == user_name, 'retweets_flag'].sum()
            
    def calc_nr_retweet_dif_users(self, user_name):
        return df_tweets.loc[df_tweets['ret_orig_user'] == user_name, 'user_name'].nunique()
 
    def calc_nr_tweets_dif_retweeted(self, user_name):
        df_text = df_tweets
        if len(df_text) > 0:
            for row in df_text[df_text['ret_orig_user'] == user_name]['tweet_text']:
                for word in row.split():
                    if word[1:8] == 'ttps://': 
                        new_row = row.replace(word, "")
                        df_text.loc[df_text['tweet_text'] == row,'tweet_text'] = new_row 
            return df_text[df_tweets['ret_orig_user'] == user_name]['tweet_text'].nunique()
        
        else:
            return 0
    
    def calc_nr_dif_hashtags(self, user_name):  
        return list(set(sum(df_tweets.loc[df_tweets['user_name'] == user_name, 'hashtags_list'],[])))

    def calc_nr_total_of_mentions_done(self, user_name):
        return df_tweets.loc[df_tweets['user_name'] == user_name, 'nr_of_users_mentioned'].sum()
    
    def calc_nr_of_mentions_done_with_dif_users(self, user_name):
        return list(set(sum(df_tweets.loc[df_tweets['user_name'] == user_name, 'users_mentioned'],[])))
    
    def calc_nr_of_mentions_done_to_the_user(self, user_name):
        return df_tweets[df_tweets['user_name'] == user_name]['mentions_done_with_him'].unique()

    def nr_of_dif_users_that_metioned_the_user(self, user_name):
        users = []
        for i in df_tweets['users_mentioned'].index:
            if user_name in df_tweets['users_mentioned'][i]:
                users = users + [df_tweets['user_name'][i]]
        size = len(set(users))
        return size   
        
           
        
#print(user_details().nr_of_dif_users_that_metioned_the_user('JustinPulitzer'))


 
nr_of_tweets = []
indexes = []
nr_of_retweets_done = []                
nr_retweet_dif_users = []                
nr_of_dif_tweets_retweeted= []
nr_dif_hashtags = []
dif_hashtags = []
nr_of_mentions_done_by_the_user = []
nr_of_dif_users_mentioned_by_the_user = []
nr_of_mentions_done_to_the_user = []
nr_of_dif_users_that_metioned_the_user = []

for name in unique_names:
    '''-- O1 --'''
    nr_of_tweets = nr_of_tweets + [user_details().calc_nr_tweets(name)] 
    indexes = indexes + [user_details().set_tweet_indexes(name)] 
    
    '''-- R1 --'''
    nr_of_retweets_done = nr_of_retweets_done + [user_details().calc_nr_retweets_done(name)]
    
    '''-- R2 --'''
    nr_of_dif_tweets_retweeted = nr_of_dif_tweets_retweeted + [user_details().calc_nr_tweets_dif_retweeted(name)]
    
    '''-- R3 --'''
    nr_retweet_dif_users = nr_retweet_dif_users + [user_details().calc_nr_retweet_dif_users(name)]
   
    '''-- O4 --'''
    dif_hashtags = dif_hashtags + [user_details().calc_nr_dif_hashtags(name)]
    nr_dif_hashtags = nr_dif_hashtags + [len(user_details().calc_nr_dif_hashtags(name))]
    
    '''-- M1 --'''
    nr_of_mentions_done_by_the_user = nr_of_mentions_done_by_the_user + [user_details().calc_nr_total_of_mentions_done(name)]
    
    '''-- M2 --'''
    nr_of_dif_users_mentioned_by_the_user = nr_of_dif_users_mentioned_by_the_user + [user_details().calc_nr_of_mentions_done_with_dif_users(name)]
    
    '''-- M3 --'''
    nr_of_mentions_done_to_the_user = nr_of_mentions_done_to_the_user + [user_details().calc_nr_of_mentions_done_to_the_user(name)]
    
    '''-- M4 --'''
    nr_of_dif_users_that_metioned_the_user = nr_of_dif_users_that_metioned_the_user + [user_details().nr_of_dif_users_that_metioned_the_user(name)]
    
data_user = {'user_name': unique_names, 'nr_of_tweets': nr_of_tweets, 'indexes_of_tweets_in_.csv':indexes, 'nr_of_retweets_done': nr_of_retweets_done,\
             'nr_of_dif_users_that_retweeted': nr_retweet_dif_users, 'nr_of_dif_tweets_retweeted': nr_of_dif_tweets_retweeted,\
             'dif_hashtags': dif_hashtags, 'nr_dif_hashtags': nr_dif_hashtags, 'nr_of_mentions_done_by_the_user': nr_of_mentions_done_by_the_user,\
             'nr_of_dif_users_mentioned_by_the_user': nr_of_dif_users_mentioned_by_the_user,
             'nr_of_mentions_done_to_the_user': nr_of_mentions_done_to_the_user,\
             'nr_of_dif_users_that_metioned_the_user' :nr_of_dif_users_that_metioned_the_user}
columns_user = ['user_name', 'nr_of_tweets', 'indexes_of_tweets_in_.csv', 'nr_of_retweets_done', 'nr_of_dif_users_that_retweeted',\
                'nr_of_dif_tweets_retweeted', 'dif_hashtags', 'nr_dif_hashtags', 'nr_of_mentions_done_by_the_user',\
                'nr_of_dif_users_mentioned_by_the_user', 'nr_of_mentions_done_to_the_user', 'nr_of_dif_users_that_metioned_the_user']
   
df_user = pd.DataFrame(data_user)
df_user = df_user[columns_user]





#print(df_user.iloc[18:23, : len(columns_user)])


elapsed_time = time.time() - start_time
print('\ntime elapsed: '+ str(elapsed_time))
