import csv
import pandas as pd
import time
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
            return (1, user_name) 
        else:
            return (0,'null')   

data_tweets = {'user_name': user_names, 'user_followers': user_followers, 'tweet_date': tweet_date, 'tweet_text': tweet_text, 'retweet': 0, 'ret_orig_user': 0}
df_tweets = pd.DataFrame(data_tweets)
columns_tweets = ['user_name', 'user_followers', 'tweet_date', 'tweet_text', 'retweet', 'ret_orig_user']
df_tweets = df_tweets[columns_tweets]


unique_names = df_tweets['user_name'].unique()

orig_user_of_tweet = []
retweets = []
nr_of_links_shared = []
for tweet in df_tweets['tweet_text']:
    #nr_of_links_shared = nr_of_links_shared + [tweet_parser().calc_nr_links_shared(tweet)]
    retweets = retweets + [tweet_parser().detect_retweets(tweet)[0]]
    orig_user_of_tweet = orig_user_of_tweet + [tweet_parser().detect_retweets(tweet)[1]]

df_tweets['retweet'] = retweets
df_tweets['ret_orig_user'] = orig_user_of_tweet
#print(df_tweets)

    
    






class user_details:
    def calc_nr_tweets(self, user_name):
        return df_tweets['user_name'].value_counts()[user_name]

    def set_tweet_indexes(self, user_name):
        return df_tweets[df_tweets['user_name'] == user_name].index.tolist()
        
    def calc_nr_retweets_done(self, user_name):
        return df_tweets.loc[df_tweets['user_name'] == user_name, 'retweet'].sum()
            
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
            #if user_name == 'bfsi_financial':
            #    print(df_text[df_tweets['ret_orig_user'] == user_name]['tweet_text'].nunique())
            #    print(df_text[df_tweets['ret_orig_user'] == user_name]['tweet_text'].unique())  
            #    print(user_name)
            return df_text[df_tweets['ret_orig_user'] == user_name]['tweet_text'].nunique()
        
        else:
            return 0
        
       

#word = 'ttps://'
#print(df_tweets['tweet_text'][0].replace(word, ""))

 
nr_of_tweets = []
indexes = []
nr_of_retweets_done = []                
nr_retweet_dif_users = []                
nr_of_dif_tweets_retweeted= []

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
    
  
     
    
data_user = {'user_name': unique_names, 'nr_of_tweets': nr_of_tweets, 'indexes_of_tweets_in_.csv':indexes, 'nr_of_retweets_done': nr_of_retweets_done,\
             'nr_of_dif_users_that_retweeted': nr_retweet_dif_users, 'nr_of_dif_tweets_retweeted': nr_of_dif_tweets_retweeted}
columns_user = ['user_name', 'nr_of_tweets', 'indexes_of_tweets_in_.csv', 'nr_of_retweets_done', 'nr_of_dif_users_that_retweeted',\
                'nr_of_dif_tweets_retweeted']
   
df_user = pd.DataFrame(data_user)
df_user = df_user[columns_user]






print(df_user.iloc[:12, :7])


elapsed_time = time.time() - start_time
print('\ntime elapsed: '+ str(elapsed_time))

