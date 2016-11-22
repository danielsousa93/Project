import time
import csv
import pickle
import got3 as got

start_time = time.time()

#193.136.221.43

f = open('pos_stock_words.pckl', 'rb')
pos_words = pickle.load(f)
f.close()

f = open('neg_stock_words.pckl', 'rb')
neg_words = pickle.load(f)
f.close()  

csvfile = open('tweetsDB sentiment_analysis pos_stock_market twoyears.csv','wb')
csvfile = open('tweetsDB sentiment_analysis neg_stock_market twoyears.csv','wb')
csvfile = open('state_of_stream sentiment_analysis stock_market.csv','wb')


i=0
for word in pos_words:
    i += 1 
    print('Positive: loading '+ word)
    try:
        #tweetCriteria = got.manager.TweetCriteria().setQuerySearch(word).setSince("2016-10-01").setUntil("2016-11-02")
        tweetCriteria = got.manager.TweetCriteria().setQuerySearch(word).setSince("2014-11-15").setUntil("2016-11-17").setMaxTweets(1000)
        tweets = got.manager.TweetManager.getTweets(tweetCriteria)
    except Exception:
        print('Error in word: ' + word)
        pass
    
    for tweet in tweets:
        with open('tweetsDB sentiment_analysis pos_stock_market twoyears.csv', 'a', encoding='utf-8') as csvfile:
            tweetwriter = csv.writer(csvfile, lineterminator='\n', delimiter = ',')
            tweetwriter.writerow([word, tweet.username, tweet.date, tweet.text])
            
    with open('state_of_stream sentiment_analysis stock_market.csv', 'a', encoding='utf-8') as csvfile:
        tweetwriter = csv.writer(csvfile, lineterminator='\n', delimiter = ',')
        tweetwriter.writerow(['positive',word, i])
        
for word in neg_words:
    i += 1 
    print('Negative: loading '+ word)
    try:
        #tweetCriteria = got.manager.TweetCriteria().setQuerySearch(word).setSince("2016-10-01").setUntil("2016-11-02")
        tweetCriteria = got.manager.TweetCriteria().setQuerySearch(word).setSince("2014-11-15").setUntil("2016-11-17").setMaxTweets(250)
        tweets = got.manager.TweetManager.getTweets(tweetCriteria)
    except Exception:
        print('-> Error in word: ' + word)
        pass
    
    
    for tweet in tweets:
        with open('tweetsDB sentiment_analysis neg_stock_market twoyears.csv', 'a', encoding='utf-8') as csvfile:
            tweetwriter = csv.writer(csvfile, lineterminator='\n', delimiter = ',')
            tweetwriter.writerow([word, tweet.username, tweet.date, tweet.text])
            
    with open('state_of_stream sentiment_analysis stock_market.csv', 'a', encoding='utf-8') as csvfile:
        tweetwriter = csv.writer(csvfile, lineterminator='\n', delimiter = ',')
        tweetwriter.writerow(['negative',word, i])
