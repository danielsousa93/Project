import csv
import tweepy
from SP500_DB import *
import time
import os


consumer_key = 'KC6IsDx3WRW1u67vCqo1fwnYu';
consumer_secret = 'oaZtZ5a0C8REssUSjJkzqWUOo2jgtg5ru5AhHz1hpJMczcMQ5q'
access_token =  '4925695673-E10TzlWIJljYEvglKsxeBqt4j0bvAO0dPIXUZMT';
access_token_secret =  'IhZrrcyeyvMfjpYMWyaS6stdmfgak7SwzP7SpEEmvMNH2';

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)


api = tweepy.API(auth)
csvfile = open('tweetsDB.csv','wb')

#override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):
    
    def on_status(self, status):
        print (status.author.screen_name)
        print (status.created_at)
        print (status.text)
        
        
        
        with open('tweetsDB.csv', 'a', encoding='utf-8') as csvfile:
            tweetwriter = csv.writer(csvfile, lineterminator='\n', delimiter = ',')
            tweetwriter.writerow([status.author.screen_name, status.author.followers_count,\
                                   status.created_at, status.text])
        
        statinfo = os.stat('tweetsDB.csv')
            
    def on_error(self, status_code):
        print(status_code)
        
        

#myStream = tweepy.Stream(auth=api.auth, listener=MyStreamListener(time_limit=20))
#myStreamListener = MyStreamListener(size_limit = size_limit_value)
#myStream = tweepy.Stream(auth , listener=myStreamListener)


#myStream.filter(track = cashtag_list, languages=['en'])

user = api.get_user('@business')
print('username: ' + user.screen_name)
print('followers: ', user.followers_count)

friends_list = api.friends_ids('@business')
print('following: ',len(friends_list))

print('account created at: ', user.created_at)

print('lists in: ', user.listed_count)