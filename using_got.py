from SP500_DB import *
import time
import csv
start_time = time.time()
i=0
csvfile = open('tweetsDB new_with_got.csv','wb')
csvfile = open('state_of_stream.csv','wb')

#193.136.221.43
import got3 as got
#import got3 as got
#tweetCriteria = got.manager.TweetCriteria().setQuerySearch('$WFC').setUntil("2016-11-02").setSince("2016-09-01")
for cashtag in cashtag_list:
    i += 1 
    print('loading '+ cashtag)
    #tweetCriteria = got.manager.TweetCriteria().setQuerySearch(cashtag).setSince("2016-11-1").setUntil("2016-11-5")
    tweetCriteria = got.manager.TweetCriteria().setQuerySearch(cashtag).setUntil("2016-11-12").setSince("2016-11-01")
    tweets = got.manager.TweetManager.getTweets(tweetCriteria)
   
    for tweet in tweets:
        text = ''
        for word in tweet.text.split():
            if word == '$':
                text = text
            elif tweet.text.split()[tweet.text.split().index(word) - 1] == '$':
                text = text + ' $' + word 
            else:
                text = text + ' ' + word
                
        #print(text)
        #print(cashtag)
        with open('tweetsDB new_with_got.csv', 'a', encoding='utf-8') as csvfile:
            tweetwriter = csv.writer(csvfile, lineterminator='\n', delimiter = ',')
            tweetwriter.writerow([cashtag, tweet.username, tweet.date, tweet.retweets,\
                                  tweet.mentions, text, tweet.favorites])
            
    with open('state_of_stream.csv', 'a', encoding='utf-8') as csvfile:
        tweetwriter = csv.writer(csvfile, lineterminator='\n', delimiter = ',')
        tweetwriter.writerow([cashtag, i])
