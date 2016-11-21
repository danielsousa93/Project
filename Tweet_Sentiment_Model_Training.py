import pandas as pd
import csv
import time
import re
import nltk
import pickle


#193.136.221.43

#961264893
#917502175

start_time = time.time()

'''
--------------------------------------------------------------------------------
------------------------ CREATE SET OF WORDS FROM FILES ------------------------
--------------------------------------------------------------------------------
''' 
''' 
csvfile = open('tweetsDB sentiment_analysis pos test.csv','wb')
csvfile = open('tweetsDB sentiment_analysis neg test.csv','wb')

with open('tweetsDB sentiment_analysis pos test.csv', 'a', encoding='utf-8') as csvfile:
            tweetwriter = csv.writer(csvfile, lineterminator='\n', delimiter = ',')
            tweetwriter.writerow(['word', 'tweet.username', 'tweet.date', 'Ola Soraia, tudo bem?'])
            tweetwriter.writerow(['word', 'tweet.username', 'tweet.date', 'Vamos ao McDonalds! Bora Benfica!'])
            tweetwriter.writerow(['word', 'tweet.username', 'tweet.date', 'Sou do Benfica, Soraia!'])
            tweetwriter.writerow(['word', 'tweet.username', 'tweet.date', 'Sinto-me bem!'])
            
with open('tweetsDB sentiment_analysis neg test.csv', 'a', encoding='utf-8') as csvfile:
            tweetwriter = csv.writer(csvfile, lineterminator='\n', delimiter = ',')      
            tweetwriter.writerow(['word', 'tweet.username', 'tweet.date', 'Tu estás chateado!'])
            tweetwriter.writerow(['word', 'tweet.username', 'tweet.date', 'Bati com o carro!'])
            tweetwriter.writerow(['word', 'tweet.username', 'tweet.date', 'Queimei o dedo!'])
            tweetwriter.writerow(['word', 'tweet.username', 'tweet.date', 'Sinto-me mal'])

            
with open('tweetsDB sentiment_analysis pos test.csv', 'r', encoding="utf-8") as file:
    reader = csv.reader(file, delimiter=",")
    pos_train_tweets = []
    for line in reader:
        text = re.sub('[^a-zA-Z0-9áéíóúÁÉÍÓÚâêîôÂÊÎÔãõÃÕçÇàÀ \n]', '', line[3])
        pos_train_tweets = pos_train_tweets + [(text,'positive')]
with open('tweetsDB sentiment_analysis neg test.csv', 'r', encoding="utf-8") as file:
    reader = csv.reader(file, delimiter=",")
    neg_train_tweets = []
    for line in reader:
        text = re.sub('[^a-zA-Z0-9áéíóúÁÉÍÓÚâêîôÂÊÎÔãõÃÕçÇàÀ \n]', '', line[3])
        neg_train_tweets = neg_train_tweets + [(text,'negative')]       
'''        
'''
remover o que está para cima
--------------------------------------------------------------------------------
'''        

with open('tweetsDB sentiment_analysis pos oneweek.csv', 'r', encoding="utf-8") as file:
    reader = csv.reader(file, delimiter=",")
    pos_train_tweets = []
    for line in reader:
        text = re.sub('[^a-zA-Z0-9áéíóúÁÉÍÓÚâêîôÂÊÎÔãõÃÕçÇàÀ \n]', '', line[3])
        pos_train_tweets = pos_train_tweets + [(text,'positive')]
with open('tweetsDB sentiment_analysis neg oneweek.csv', 'r', encoding="utf-8") as file:
    reader = csv.reader(file, delimiter=",")
    neg_train_tweets = []
    for line in reader:
        text = re.sub('[^a-zA-Z0-9áéíóúÁÉÍÓÚâêîôÂÊÎÔãõÃÕçÇàÀ \n]', '', line[3])
        neg_train_tweets = neg_train_tweets + [(text,'negative')]   
        
       
elapsed_time = time.time() - start_time
print('\ntime elapsed reading tweets from files: '+ str(elapsed_time))
#print(pos_train_tweets)
#print(neg_train_tweets)        
      
'''
--------------------------------------------------------------------------------
---------------------------- FILTER WORDS FROM SET -----------------------------
--------------------------------------------------------------------------------
'''
train_tweets = []
for (words, sentiment) in pos_train_tweets + neg_train_tweets:
    words_filtered = [e.lower() for e in words.split() if len(e) >= 3]
    train_tweets.append((words_filtered, sentiment))


f = open('train_tweets.pckl', 'wb')
pickle.dump(train_tweets, f)
f.close() 

elapsed_time = time.time() - start_time
print('\ntime elapsed filtering words from set: '+ str(elapsed_time))      

#train_train_tweets = tweets[0:len(tweets):2]
#test_train_tweets = tweets[1:len(tweets):2]
#print(train_train_tweets)
#print(test_train_tweets)


'''
--------------------------------------------------------------------------------
------------------------------ GET WORD FEATURES -------------------------------
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
#word_features = get_word_features(get_words_in_train_tweets(train_tweets))
#print(word_features)

elapsed_time = time.time() - start_time
print('\ntime elapsed getting word features: '+ str(elapsed_time))  

'''
--------------------------------------------------------------------------------
-------------------------------- MODEL TRAIN  ----------------------------------
--------------------------------------------------------------------------------
'''
def extract_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features

#print(extract_features(['ola', 'soraia', 'tudo', 'bem']))

print('Training the model...')
training_set = nltk.classify.apply_features(extract_features, train_tweets)
#print(training_set)

classifier = nltk.NaiveBayesClassifier.train(training_set)


elapsed_time = time.time() - start_time
print('\ntime elapsed in model training: '+ str(elapsed_time)) 

#print(classifier.show_most_informative_features(32))

'''
--------------------------------------------------------------------------------
----------------------------- STORING CLASSIFIER -------------------------------
--------------------------------------------------------------------------------
'''
#nltk.classify.accuracy(classifier, testing_set))*100

f = open('classifier.pckl', 'wb')
pickle.dump(classifier, f)
f.close()    

elapsed_time = time.time() - start_time
print('\ntime elapsed storing classifier and word_features: '+ str(elapsed_time)) 

