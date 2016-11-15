import csv
import tweepy
from SP500_DB import cashtag_list
import time
import pandas as pd

start_time = time.time()




#elapsed_time = time.time() - start_time
#print('\ntime elapsed to read .h5 files: '+ str(elapsed_time))


consumer_key = 'KC6IsDx3WRW1u67vCqo1fwnYu';
consumer_secret = 'oaZtZ5a0C8REssUSjJkzqWUOo2jgtg5ru5AhHz1hpJMczcMQ5q'
access_token =  '4925695673-E10TzlWIJljYEvglKsxeBqt4j0bvAO0dPIXUZMT';
access_token_secret =  'IhZrrcyeyvMfjpYMWyaS6stdmfgak7SwzP7SpEEmvMNH2';

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit = True)

#elapsed_time = time.time() - start_time
#print('\ntime elapsed connecting: '+ str(elapsed_time))

try: 
    user = api.get_user('Street_Oracle')
except Exception:
    print('next')


    