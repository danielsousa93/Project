'''
Created on 28/09/2016

@author: Daniel
'''
consumer_key = 'KC6IsDx3WRW1u67vCqo1fwnYu';
consumer_secret = 'oaZtZ5a0C8REssUSjJkzqWUOo2jgtg5ru5AhHz1hpJMczcMQ5q'
access_token =  '4925695673-E10TzlWIJljYEvglKsxeBqt4j0bvAO0dPIXUZMT';
access_token_secret =  'IhZrrcyeyvMfjpYMWyaS6stdmfgak7SwzP7SpEEmvMNH2';

from SP500_DB import *
import tweepy
import csv
import time


timeout_value_sec = 30


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
csvfile = open('tweetsDB.csv','wb')

#override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):
    def __init__(self, time_limit):
        self.start_time = time.time()
        self.limit = time_limit
        super(MyStreamListener, self).__init__()
    
    def on_status(self, status):
        print (status.text)
        print (status.author.screen_name)
        print (status.created_at)
        print (status.author.followers_count)
        
        
        with open('tweetsDB.csv', 'a', encoding='utf-8') as csvfile:
            tweetwriter = csv.writer(csvfile, lineterminator='\n', delimiter = ',')
            tweetwriter.writerow([status.author.screen_name, status.author.followers_count,\
                                   status.created_at, status.text])
    
        print(self.limit)
        print(time.time() - self.start_time)
        if (time.time() - self.start_time) < self.limit:
            return True
        else:
            return False
            
    def on_error(self, status_code):
        print(status_code)
        
        

#myStream = tweepy.Stream(auth=api.auth, listener=MyStreamListener(time_limit=20))
myStreamListener = MyStreamListener(time_limit=timeout_value_sec)
myStream = tweepy.Stream(auth , listener=myStreamListener)


myStream.filter(track = cashtag_list, languages=['en'])



#print(timeout)
