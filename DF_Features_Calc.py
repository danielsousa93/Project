import pandas as pd
import time
from DBparser import unique_names

start_time = time.time()


df_tweets = pd.read_pickle('df_tweets - Backup.h5')
df_user = pd.read_pickle('df_user - Backup.h5')


user_names = df_user['user_name']

class features:
    def calc_topic_connection(self, user_name):
        O1 = 




topic_connection = []
for line in df_user.itertuples()
    topic_connection = topic_connection + [features().calc_topic_connection(line[1])]
    

data = {'user_name': user_names, 'topic_connection': 0, 'topic_attitude': 0, 'no_talk': 0, 'retweets':0, 'mentions': 0, 'hashtags': 0,\
        'no_similarity_between_tweets': 0, 'topic_tweets_ratio': 0}
columns = ['user_name', 'topic_connection', 'topic_attitude', 'no_talk', 'retweets', 'mentions', 'hashtags',\
           'no_similarity_between_tweets', 'topic_tweets_ratio']
   
df_features = pd.DataFrame(data)
df_features = df_features[columns]




print(df_features)

elapsed_time = time.time() - start_time
print('\ntime elapsed: '+ str(elapsed_time))