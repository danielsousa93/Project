import csv
import tweepy
from SP500_DB import cashtag_list
import time
import pandas as pd

start_time = time.time()

MODE = 0

df_user_by_company = {}
newpath1 = r'/home/dsousa/DATAFRAMES df_user_by_company'
for cashtag in cashtag_list:
    df_user_by_company[cashtag] = pd.read_pickle(newpath1 + '/df_user_by_company'+ cashtag + '.h5')


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
if MODE == 0:
    csvfile = open('DB user_details onemonth onemonth.csv','wb')
    
    for cashtag in cashtag_list:
        for name in df_user_by_company[cashtag]['user_name']:
            try:
                user = api.get_user(name)
                with open('DB user_details onemonth.csv', 'a', encoding='utf-8') as csvfile:
                    tweetwriter = csv.writer(csvfile, lineterminator='\n', delimiter = ',')
                    tweetwriter.writerow([cashtag, name, user.created_at, user.followers_count, user.friends_count,\
                                          user.statuses_count, user.listed_count, user.favourites_count])
            
            except Exception:
                with open('DB user_details onemonth.csv', 'a', encoding='utf-8') as csvfile:
                    tweetwriter = csv.writer(csvfile, lineterminator='\n', delimiter = ',')
                    tweetwriter.writerow([cashtag, name, 'NULL', 'NULL', 'NULL',\
                                          'NULL', 'NULL', 'NULL'])
else:
    csvfile = open('DB user_details onemonth.csv','a')
    i = 0
    with open('DB user_details onemonth.csv', 'r', encoding="utf-8") as file:
        reader = csv.reader(file, delimiter=",")
        for i in reader:
            line = i
        print(line)
            
        cashtag = line[0]    
        index = cashtag_list.index(cashtag)
        user_name = line[1]
        
        
        index_df = df_user_by_company[cashtag][df_user_by_company[cashtag]['user_name'] == user_name].index.tolist()
        
        for name in df_user_by_company[cashtag]['user_name'].loc[index_df[0]+1:]:
            try:
                user = api.get_user(name)
                with open('DB user_details onemonth.csv', 'a', encoding='utf-8') as csvfile:
                    tweetwriter = csv.writer(csvfile, lineterminator='\n', delimiter = ',')
                    tweetwriter.writerow([cashtag, name, user.created_at, user.followers_count, user.friends_count,\
                                          user.statuses_count, user.listed_count, user.favourites_count])
            except Exception:
                with open('DB user_details onemonth.csv', 'a', encoding='utf-8') as csvfile:
                    tweetwriter = csv.writer(csvfile, lineterminator='\n', delimiter = ',')
                    tweetwriter.writerow([cashtag, name, 'NULL', 'NULL', 'NULL',\
                                          'NULL', 'NULL', 'NULL'])
                    
        for cashtag in cashtag_list[(index+1):]:
            for name in df_user_by_company[cashtag]['user_name']:
                try:
                    user = api.get_user(name)
                    with open('DB user_details onemonth.csv', 'a', encoding='utf-8') as csvfile:
                        tweetwriter = csv.writer(csvfile, lineterminator='\n', delimiter = ',')
                        tweetwriter.writerow([cashtag, name, user.created_at, user.followers_count, user.friends_count,\
                                              user.statuses_count, user.listed_count, user.favourites_count])
                except Exception:
                    with open('DB user_details onemonth.csv', 'a', encoding='utf-8') as csvfile:
                        tweetwriter = csv.writer(csvfile, lineterminator='\n', delimiter = ',')
                        tweetwriter.writerow([cashtag, name, 'NULL', 'NULL', 'NULL',\
                                              'NULL', 'NULL', 'NULL'])
                        
                    
                    