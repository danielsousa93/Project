import time
import csv
import got3 as got
import sys

start_time = time.time()

#193.136.221.43



pos_words = ['#elated','#overjoyed','#enjoy','#excited','#proud','#joyful','#feelhappy','#sohappy',
           '#veryhappy','#happy','#superhappy','#happytweet','#feelblessed','#blessed','#amazing',
           '#wonderful','#excelent','#delighted','#enthusiastic',
           '#calm','#calming','#peaceful','#quiet','#silent','#serene','#convinced','#consent',
           '#contented','#contentment','#satisfied','#relax','#relaxed','#relaxing','#sleepy',
           '#sleepyhead','#asleep','#resting','#restful','#placid']
           
neg_words = ['#nervous','#anxious','#tension','#afraid','#fearful','#angry','#annoyed','#annoying',
           '#stress','#distressed','#distress','#stressful','#stressed','#worried','#tense','#bothered',
           '#disturbed','#irritated','#mad','#furious',
           '#sad','#ifeelsad','#feelsad','#sosad','#verysad','#sorrow','#disappointed','#supersad',
           '#miserable','#hopeless','#depress','#depressed','#depression','#fatigued','#gloomy',
           '#nothappy','#unhappy','#suicidal','#downhearted','#hapless','#dispirited',
           '#hope','#fear','#worry','#upset','#positive','#negative']


with open('state_of_stream sentiment_analysis.csv', 'r', encoding="utf-8") as file:
    reader = csv.reader(file, delimiter=",")
    for i in reader:
        line = i

i = int(line[2])
pos_words = pos_words[i:]
'''
if line[0] == 'positive':
    i = int(line[2])
    pos_words = pos_words[i:]
elif line[0] == 'negative':
    i = int(line[2])
    neg_words = neg_words[(i-len(pos_words)):]
else:
    sys.exit()
'''
if i < len(pos_words):
    for word in pos_words:
        i += 1 
        print('Positive: loading '+ word)
        try:
            #tweetCriteria = got.manager.TweetCriteria().setQuerySearch(word).setSince("2016-10-01").setUntil("2016-11-02")
            tweetCriteria = got.manager.TweetCriteria().setQuerySearch(word).setSince("2014-11-15").setUntil("2016-11-17").setMaxTweets(6000)
            tweets = got.manager.TweetManager.getTweets(tweetCriteria)
        except Exception:
            print('Error in word: ' + word)
            pass
        
        for tweet in tweets:
            with open('tweetsDB sentiment_analysis pos twoyears.csv', 'a', encoding='utf-8') as csvfile:
                tweetwriter = csv.writer(csvfile, lineterminator='\n', delimiter = ',')
                tweetwriter.writerow([word, tweet.username, tweet.date, tweet.text])
                
        with open('state_of_stream sentiment_analysis.csv', 'a', encoding='utf-8') as csvfile:
            tweetwriter = csv.writer(csvfile, lineterminator='\n', delimiter = ',')
            tweetwriter.writerow(['positive',word, i])
'''         
if i >= len(pos_words):         
    for word in neg_words:
        i += 1 
        print('Negative: loading '+ word)
        try:
            #tweetCriteria = got.manager.TweetCriteria().setQuerySearch(word).setSince("2016-10-01").setUntil("2016-11-02")
            tweetCriteria = got.manager.TweetCriteria().setQuerySearch(word).setSince("2014-11-15").setUntil("2016-11-17").setMaxTweets(6000)
            tweets = got.manager.TweetManager.getTweets(tweetCriteria)
        except Exception:
            print('-> Error in word: ' + word)
            pass
        
        
        for tweet in tweets:
            with open('tweetsDB sentiment_analysis neg twoyears.csv', 'a', encoding='utf-8') as csvfile:
                tweetwriter = csv.writer(csvfile, lineterminator='\n', delimiter = ',')
                tweetwriter.writerow([word, tweet.username, tweet.date, tweet.text])
                
        with open('state_of_stream sentiment_analysis.csv', 'a', encoding='utf-8') as csvfile:
            tweetwriter = csv.writer(csvfile, lineterminator='\n', delimiter = ',')
            tweetwriter.writerow(['negative',word, i])
'''