import pandas as pd
import csv
import time
import re
import nltk
import pickle
from SP500_DB import cashtag_list
import sqlite3

#193.136.221.43


start_time = time.time()
'''
--------------------------------------------------------------------------------
---------------------------- RESTORING CLASSIFIER ------------------------------
--------------------------------------------------------------------------------
'''
f = open('classifier.pckl', 'rb')
classifier = pickle.load(f)
f.close()

f = open('train_tweets.pckl', 'rb')
train_tweets = pickle.load(f)
f.close()

elapsed_time = time.time() - start_time
print('\ntime elapsed restoring classifier and tweets: '+ str(elapsed_time)) 

'''
--------------------------------------------------------------------------------
------ FUNCTIONS AND VARIABLES NEEDED FROM Tweet_Sentiment_Classification ------
--------------------------------------------------------------------------------
'''
def get_words_in_tweets(tweets):
    all_words = []
    for (words, sentiment) in tweets:
        all_words.extend(words)
    return all_words

def get_word_features(wordlist):
    wordlist = nltk.FreqDist(wordlist)
    #print(wordlist.freq)
    word_features = wordlist.keys()
    return word_features


word_features = get_word_features(get_words_in_tweets(train_tweets))


def extract_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features


elapsed_time = time.time() - start_time
print('\ntime elapsed getting word features (Tweet_Sentiment_Classification import part): '+ str(elapsed_time))  

'''
--------------------------------------------------------------------------------
------------------------------ CLASSIFICATION  ---------------------------------
--------------------------------------------------------------------------------
'''

'''
tweet = 'benfica'
print('Tweet: ' + tweet)
print('Sentiment: ' + classifier.classify(extract_features(tweet.split())))
print(classifier.show_most_informative_features(32))
'''
i=0
sentiment_array = []
with open('tweetsDB - newfromremote oneweek.csv', 'r', encoding="utf-8") as file:
#with open('tweetsDB - newfromremote onemonth.csv', 'r', encoding="utf-8") as file:
    reader = csv.reader(file, delimiter=",")
    for line in reader:
        i += 1
        tweet = line[5]
        try:
            sentiment = classifier.classify(extract_features(tweet.split()))
            if sentiment == 'positive':
                sentiment_value = 1
            else:
                sentiment_value = -1
            
            sentiment_array = sentiment_array + [(line[0], line[1], line[2], sentiment, sentiment_value)]
            
            print(i, line[0], line[1], sentiment, sentiment_value, line[5])
        except Exception:
            print('ERROR classifying cashtag: ' + line[0] + ' / user: ' + line[1])
            sentiment_array = sentiment_array + [(line[0], line[1], 'error')]
            pass

elapsed_time = time.time() - start_time
print('\ntime elapsed classifying each tweet from remote: '+ str(elapsed_time))  


'''
--------------------------------------------------------------------------------
--------------------------- STORING CLASSIFICATIONS ----------------------------
--------------------------------------------------------------------------------
'''
f = open('classifications.pckl', 'wb')
pickle.dump(sentiment_array, f)
f.close()    

elapsed_time = time.time() - start_time
print('\ntime elapsed storing classifications: '+ str(elapsed_time)) 





 

