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
        
    def identify_users_that_mentioned_the_user(self, user_name, users_mentioned):
        for name in users_mentioned:
            if name in unique_names:
                df_tweets.loc[df_tweets['user_name'] == name, 'users_that_mentioned_the_user'] = user_name +  ' ' + df_tweets.loc[df_tweets['user_name'] == name, 'users_that_mentioned_the_user']    
    
    def detect_conversations(self, text, user_name):
        if text[:1] == '@': 
            df_tweets.loc[df_tweets['user_name'] == user_name, 'nr_of_conversation_tweets_done_by_the_user'] +=1
               
              

data_tweets = {'user_name': user_names, 'user_followers': user_followers, 'tweet_date': tweet_date, 'tweet_text': tweet_text,\
               'retweets_flag': 0, 'ret_orig_user': 0, 'hashtags_list': 0, 'users_mentioned': 0, 'nr_of_users_mentioned': 0,\
               'mentions_done_with_him': 0, 'users_that_mentioned_the_user': '', 'nr_of_conversation_tweets_done_by_the_user': 0}
df_tweets = pd.DataFrame(data_tweets)
columns_tweets = ['user_name', 'user_followers', 'tweet_date', 'tweet_text', 'retweets_flag', 'ret_orig_user', 'hashtags_list', 'users_mentioned'\
                  , 'nr_of_users_mentioned', 'mentions_done_with_him', 'users_that_mentioned_the_user', 'nr_of_conversation_tweets_done_by_the_user']
df_tweets = df_tweets[columns_tweets]


unique_names = df_tweets['user_name'].unique()


orig_user_of_tweet = []
retweets_flag = []
nr_of_links_shared = []
hashtags_list = []
nr_of_users_mentioned = []
users_mentioned = []


    
for tweet in df_tweets.itertuples():
        #nr_of_links_shared = nr_of_links_shared + [tweet_parser().calc_nr_links_shared(tweet[4])]
        (new_retweets_flag, new_orig_user_of_tweet) = tweet_parser().detect_retweets(tweet[4])
        retweets_flag = retweets_flag + [new_retweets_flag]
        orig_user_of_tweet = orig_user_of_tweet + [new_orig_user_of_tweet]
        
        hashtags_list = hashtags_list + [tweet_parser().identify_hashtags(tweet[4])]
        
        (new_nr_of_users_mentioned,new_users_mentioned) = tweet_parser().detect_mentions(tweet[4])
        users_mentioned = users_mentioned + [new_users_mentioned]
        nr_of_users_mentioned = nr_of_users_mentioned + [new_nr_of_users_mentioned]
        
        tweet_parser().detect_conversations(tweet[4], tweet[1])
        
    
df_tweets['retweets_flag'] = retweets_flag
df_tweets['ret_orig_user'] = orig_user_of_tweet
df_tweets['hashtags_list'] = hashtags_list
df_tweets['nr_of_users_mentioned'] = nr_of_users_mentioned
df_tweets['users_mentioned'] = users_mentioned

for tweet in df_tweets.itertuples():  
        if tweet[9] != 0:
            tweet_parser().identify_users_that_mentioned_the_user(tweet[1], tweet[8])
            

elapsed_time = time.time() - start_time
print('\ntime elapsed in df_tweets: '+ str(elapsed_time))

#print(df_tweets)


class user_details:     
    def calc_nr_tweets(self, user_name):
        return df_tweets['user_name'].value_counts()[user_name]
    
    def calc_nr_of_original_tweets(self, user_name):
        retweets_nr = len(df_tweets[(df_tweets['user_name'] == user_name) & (df_tweets['retweets_flag'] == 1)])
        orig_tweet_nr = user_details().calc_nr_tweets(user_name)
        return orig_tweet_nr - retweets_nr

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
        return df_tweets.loc[df_tweets['user_name'] == user_name, 'mentions_done_with_him'].iloc[0]
    
    def calc_nr_of_dif_users_that_metioned_the_user(self, user_name):
        users_list = df_tweets.loc[df_tweets['user_name'] == user_name, 'users_that_mentioned_the_user']
        users_list = users_list.unique()
        final_users_list = 0
        if users_list != '':
            array = []
            users_list = ''.join(users_list)
            for word in users_list.split():
                if word not in array:
                    array = array + [word]
            final_users_list = len(list(set(array)))
        return final_users_list
        
    def calc_nr_of_conversation_tweets_done_by_the_user(self, user_name):
        return df_tweets.loc[df_tweets['user_name'] == user_name, 'nr_of_conversation_tweets_done_by_the_user'].iloc[0]
      
#print(len(df_tweets[(df_tweets['user_name'] == 'LloydCreekStock') & (df_tweets['retweets_flag'] == 1)]))  
#print((user_details().calc_nr_of_mentions_done_to_the_user('JustinPulitzer')))
#print(user_details().nr_of_dif_users_that_metioned_the_user('JustinPulitzer'))


 
nr_of_tweets = []
nr_of_original_tweets_done = []
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
nr_of_conversation_tweets_done_by_the_user = []





for name in unique_names:
    '''-- nr of tweets --'''
    nr_of_tweets = nr_of_tweets + [user_details().calc_nr_tweets(name)] 
    indexes = indexes + [user_details().set_tweet_indexes(name)] 
    
    '''-- O1 --'''
    nr_of_original_tweets_done = nr_of_original_tweets_done + [user_details().calc_nr_of_original_tweets(name)]
    
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
    nr_of_dif_users_that_metioned_the_user = nr_of_dif_users_that_metioned_the_user + [user_details().calc_nr_of_dif_users_that_metioned_the_user(name)]
    
    '''-- C1 --'''
    nr_of_conversation_tweets_done_by_the_user = nr_of_conversation_tweets_done_by_the_user + [user_details().calc_nr_of_conversation_tweets_done_by_the_user(name)]
    

    
data_user = {'user_name': unique_names, 'nr_of_tweets': nr_of_tweets, 'indexes_of_tweets_in_.csv':indexes, 'nr_of_retweets_done': nr_of_retweets_done,\
             'nr_of_dif_users_that_retweeted': nr_retweet_dif_users, 'nr_of_dif_tweets_retweeted': nr_of_dif_tweets_retweeted,\
             'dif_hashtags': dif_hashtags, 'nr_dif_hashtags': nr_dif_hashtags, 'nr_of_mentions_done_by_the_user': nr_of_mentions_done_by_the_user,\
             'nr_of_dif_users_mentioned_by_the_user': nr_of_dif_users_mentioned_by_the_user,\
             'nr_of_mentions_done_to_the_user': nr_of_mentions_done_to_the_user,\
             'nr_of_dif_users_that_metioned_the_user': nr_of_dif_users_that_metioned_the_user,\
             'nr_of_original_tweets_done': nr_of_original_tweets_done,\
             'nr_of_conversation_tweets_done_by_the_user': nr_of_conversation_tweets_done_by_the_user}
columns_user = ['user_name', 'nr_of_tweets', 'indexes_of_tweets_in_.csv', 'nr_of_retweets_done', 'nr_of_dif_users_that_retweeted',\
                'nr_of_dif_tweets_retweeted', 'dif_hashtags', 'nr_dif_hashtags', 'nr_of_mentions_done_by_the_user',\
                'nr_of_dif_users_mentioned_by_the_user', 'nr_of_mentions_done_to_the_user',\
                'nr_of_dif_users_that_metioned_the_user', 'nr_of_original_tweets_done', 'nr_of_conversation_tweets_done_by_the_user']
   
df_user = pd.DataFrame(data_user)
df_user = df_user[columns_user]



    


#print(df_user.iloc[1:500, : len(columns_user)]['nr_of_conversation_tweets_done_by_the_user'])
#print(df_user[df_user['nr_of_conversation_tweets_done_by_the_user'] ])

elapsed_time = time.time() - start_time
print('\ntime elapsed in df_tweets + df_users: '+ str(elapsed_time))

df_tweets.to_pickle('df_tweets.h5')
df_user.to_pickle('df_user.h5')

elapsed_time = time.time() - start_time
print('\ntime elapsed saving files: '+ str(elapsed_time))
