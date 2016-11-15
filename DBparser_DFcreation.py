import csv
import pandas as pd
import time
import re
import os
from SP500_DB import cashtag_list

'''
--------------------------------------------------------------------------------
---------------------------- READ FILE FROM REMOTE ----------------------------- 
--------------------------------------------------------------------------------
'''
start_time = time.time()

with open('tweetsDB - newfromremote oneweek.csv', 'r', encoding="utf-8") as file:
    reader = csv.reader(file, delimiter=",")
    
    cashtags_index = []
    user_names = []
    tweet_date = []
    nr_of_retweets_done_to_that_tweet = []
    tweet_text = []
    likes = []
    users_mentioned_by_the_user = []
    for line in reader:
        cashtags_index = cashtags_index + [line[0]]
        user_names = user_names + [line[1]]
        tweet_date = tweet_date + [line[2]]
        nr_of_retweets_done_to_that_tweet = nr_of_retweets_done_to_that_tweet + [line[3]]
        
        tweet_text = tweet_text + [line[5]]
        likes = likes + [int(line[6])]
    
        list = ''
        for word in line[4].split():
            if len(word) > 1 and word[1:5] != 'http':
                list = list + ' ' + word[1:len(word)]
        users_mentioned_by_the_user = users_mentioned_by_the_user + [list]
        
        

elapsed_time = time.time() - start_time
print('\ntime elapsed reading file from remote: '+ str(elapsed_time))
        
'''
--------------------------------------------------------------------------------
------------------------- PREPARING DF_USER_BY_COMPANY -------------------------
--------------------------------------------------------------------------------
'''   
col_user = ['user_name', 'nr_of_tweets', 'nr_of_dif_users_that_retweeted',\
                'nr_of_dif_tweets_retweeted', 'nr_dif_hashtags', 'nr_of_mentions_done_by_the_user',\
                'nr_of_dif_users_mentioned_by_the_user', 'nr_of_mentions_done_to_the_user',\
                'nr_of_dif_users_that_metioned_the_user', 'nr_of_conversation_tweets_done_by_the_user', 'likes',\
                'nr_of_amount_of_tweets_done']


newpath = r'D:\LiClipse Workspace\Project\DATAFRAMES df_user_by_company'

if not os.path.exists(newpath):
    os.makedirs(newpath)

df_user_by_company = {}
for cashtag in cashtag_list:
    df_user_by_company[cashtag] = pd.DataFrame(columns=col_user)


elapsed_time = time.time() - start_time
print('\ntime elapsed preparing df_user_by_company: '+ str(elapsed_time))

'''
--------------------------------------------------------------------------------
------------------------------ CLASS TWEET_PARSER ------------------------------
--------------------------------------------------------------------------------
'''
class tweet_parser:             
    def identify_hashtags(self, text):
        words_array = []
        if ('$' in text) or ('#' in text):
            for word in text.split():
                if (word[0] == '$' or word[0] == '#') and (len(word) > 1) and not word[1].isdigit():
                    word = re.sub('[^a-zA-Z0-9 \n\$#]', '', word)
                    words_array = words_array + [word]
        return words_array
'''
--------------------------------------------------------------------------------
---------------------------- CREATION OF DF_TWEETS -----------------------------
--------------------------------------------------------------------------------
'''
data_tweets = {'user_name': user_names, 'cashtag_index': cashtags_index, 'tweet_date': tweet_date, 'tweet_text': tweet_text,\
               'nr_of_retweets_done_to_that_tweet': nr_of_retweets_done_to_that_tweet, 'hashtags_list': 0,\
               'users_mentioned': users_mentioned_by_the_user,\
               'users_that_mentioned_the_user': '', 'likes': likes}

columns_tweets = ['user_name', 'cashtag_index', 'tweet_date', 'tweet_text', 'nr_of_retweets_done_to_that_tweet',\
                  'hashtags_list', 'users_mentioned',\
                  'users_that_mentioned_the_user', 'likes']

df_tweets_with_cashtag = pd.DataFrame(data_tweets, columns=columns_tweets)


df_tweets = df_tweets_with_cashtag[['user_name', 'tweet_date', 'tweet_text',\
                                    'nr_of_retweets_done_to_that_tweet', 'hashtags_list',\
                                    'users_mentioned', 'users_that_mentioned_the_user',\
                                    'likes']].drop_duplicates()
                                    
hashtags_list = []    
for tweet in df_tweets.itertuples():        
        hashtags_list = hashtags_list + [tweet_parser().identify_hashtags(tweet[3])]
    
df_tweets['hashtags_list'] = hashtags_list


elapsed_time = time.time() - start_time
print('\ntime elapsed creating df_tweets: '+ str(elapsed_time))

'''
--------------------------------------------------------------------------------
----------------------------- CLASS USER_DETAILS -------------------------------
--------------------------------------------------------------------------------
'''
class user_details:   
    def return_names(self, cashtag):
        return df_tweets_with_cashtag[cashtag].loc[df_tweets_with_cashtag[cashtag]['cashtag_index'] == cashtag, 'user_name']
    
    def calc_nr_of_conversation_tweets_done_by_the_user(self, user_name, df_inst):
        i = 0
        for line in df_inst.itertuples():
            if line[4][1:2] == '@' and line[1] == user_name and len(line[7]) > 0: 
                i += 1  
        return i
        
    def calc_nr_tweets(self, user_name, df_inst):
        return df_inst['user_name'].value_counts()[user_name]
 
    def calc_nr_tweets_dif_retweeted(self, user_name, df_inst): 
        i = 0
        sum = 0
        df = df_inst.loc[df_inst['user_name'] == user_name, 'nr_of_retweets_done_to_that_tweet']
        for value in df:
            sum = sum + int(value)
            if value != '0':
                i += 1
        return (i, sum)           
      
    def calc_nr_dif_hashtags(self, user_name):
        array = []
        for line in df_tweets.loc[df_tweets['user_name'] == user_name, 'hashtags_list']:
            array = array + line
        return len(set(array))

    def calc_nr_mentions_done_by_the_user(self, user_name, df_inst):
        i= 0
        for word in df_inst.loc[df_inst['user_name'] == user_name, 'users_mentioned'].sum().split():
            i += 1
        return i
         
    
    def calc_nr_of_mentions_done_with_dif_users(self, user_name,df_inst):
        users_list = []
        for word in df_inst.loc[df_inst['user_name'] == user_name, 'users_mentioned'].sum().split():
            users_list = users_list + [word]
        return len(set(users_list))
    
    def calc_nr_of_mentions_done_to_the_user(self, user_name, df_inst):
        i = 0
        for word in df_inst['users_mentioned'].sum().split():
            if user_name == word:
                i += 1
        return i
    
    def calc_nr_of_dif_users_that_metioned_the_user(self, user_name, df_inst):
        users_list = []
        for line in df_inst.itertuples():
            if user_name in line[7]:
                users_list = users_list + [line[1]]
        return len(set(users_list))
                
    def calc_nr_total_of_likes(self, user_name, df_inst):
        return df_inst.loc[df_inst['user_name'] == user_name, 'likes'].sum()              
    
    def calc_nr_of_amount_of_tweets_done(self, user_name):
        return df_tweets.loc[df_tweets['user_name'] == user_name, 'user_name'].count()
        

'''
--------------------------------------------------------------------------------
------------------------ CREATION OF DF_USER_BY_COMPANY ------------------------
--------------------------------------------------------------------------------
'''
print('df_user_by_company filling started...')
i = 0

for cashtag in cashtag_list:
    i +=1
    names = []
    nr_of_dif_tweets_retweeted= []
    nr_of_dif_users_that_retweeted = [] 
    nr_of_original_tweets_done = [] 
    nr_dif_hashtags = []
    nr_of_conversation_tweets_done_by_the_user = []
    nr_of_mentions_done_by_the_user = []
    nr_of_dif_users_mentioned_by_the_user = []
    nr_of_mentions_done_to_the_user = []
    nr_of_dif_users_that_metioned_the_user = []
    nr_total_of_likes = []
    nr_of_amount_of_tweets_done = []
    
    df_inst = df_tweets_with_cashtag[df_tweets_with_cashtag['cashtag_index'] == cashtag]
    names = df_inst['user_name'].unique()
    for name in names:
        #R2 e R3
        (new_nr_of_dif_tweets_retweeted, new_nr_of_dif_users_that_retweeted)  = user_details().calc_nr_tweets_dif_retweeted(name, df_inst)
        nr_of_dif_tweets_retweeted = nr_of_dif_tweets_retweeted + [new_nr_of_dif_tweets_retweeted]
        nr_of_dif_users_that_retweeted = nr_of_dif_users_that_retweeted + [new_nr_of_dif_users_that_retweeted]
        #O1
        nr_of_original_tweets_done = nr_of_original_tweets_done + [user_details().calc_nr_tweets(name, df_inst)]
        #O4
        nr_dif_hashtags = nr_dif_hashtags + [user_details().calc_nr_dif_hashtags(name)]
        #C1
        nr_of_conversation_tweets_done_by_the_user = nr_of_conversation_tweets_done_by_the_user + [user_details().calc_nr_of_conversation_tweets_done_by_the_user(name, df_inst)]
        #M1
        nr_of_mentions_done_by_the_user = nr_of_mentions_done_by_the_user + [user_details().calc_nr_mentions_done_by_the_user(name, df_inst)]
        #M2
        nr_of_dif_users_mentioned_by_the_user = nr_of_dif_users_mentioned_by_the_user + [user_details().calc_nr_of_mentions_done_with_dif_users(name, df_inst)]
        #M3
        nr_of_mentions_done_to_the_user = nr_of_mentions_done_to_the_user + [user_details().calc_nr_of_mentions_done_to_the_user(name, df_inst)]
        #M4
        nr_of_dif_users_that_metioned_the_user = nr_of_dif_users_that_metioned_the_user + [user_details().calc_nr_of_dif_users_that_metioned_the_user(name, df_inst)]   
        #likes
        nr_total_of_likes = nr_total_of_likes + [user_details().calc_nr_total_of_likes(name, df_inst)] 
        #total nr of tweets
        nr_of_amount_of_tweets_done = nr_of_amount_of_tweets_done + [user_details().calc_nr_of_amount_of_tweets_done(name)] 
        
         
    data_user = {'user_name': names, 'nr_of_tweets': nr_of_original_tweets_done,\
             'nr_of_dif_users_that_retweeted': nr_of_dif_users_that_retweeted, 'nr_of_dif_tweets_retweeted': nr_of_dif_tweets_retweeted,\
             'nr_dif_hashtags': nr_dif_hashtags, 'nr_of_mentions_done_by_the_user': nr_of_mentions_done_by_the_user,\
             'nr_of_dif_users_mentioned_by_the_user': nr_of_dif_users_mentioned_by_the_user,\
             'nr_of_mentions_done_to_the_user': nr_of_mentions_done_to_the_user,\
             'nr_of_dif_users_that_metioned_the_user': nr_of_dif_users_that_metioned_the_user,\
             'nr_of_conversation_tweets_done_by_the_user': nr_of_conversation_tweets_done_by_the_user,\
             'likes': nr_total_of_likes, 'nr_of_amount_of_tweets_done': nr_of_amount_of_tweets_done}
    
    df_user_by_company[cashtag] = pd.DataFrame(data_user, columns = col_user)    
    
    elapsed_time = time.time() - start_time
    print(str(i) + '. DONE cashtag ' + cashtag + '. time: '+ str(elapsed_time))
    

elapsed_time = time.time() - start_time
print('\ntime elapsed filling df_user_by_company: '+ str(elapsed_time))

'''
--------------------------------------------------------------------------------
-------------------------- SAVING FILES IN .h5 FORMAT --------------------------
--------------------------------------------------------------------------------
'''
df_tweets.to_pickle('df_tweets.h5')

for cashtag in cashtag_list:
    df_user_by_company[cashtag].to_pickle(newpath + '\df_user_by_company'+ cashtag + '.h5')

elapsed_time = time.time() - start_time
print('\ntime elapsed saving files in .h5 format: '+ str(elapsed_time))
