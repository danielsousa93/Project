import pandas as pd
import time
import nltk
import pickle
from SP500_DB import cashtag_list
import sys 


#193.136.221.43

bound = 0.2

start_time = time.time()
initial = start_time
initial_cashtag = start_time
old_cashtag_list = cashtag_list


exit_flag = 0
concatenate_flag = 1
cashtag_list = cashtag_list[5:14]
#print(cashtag_list[:5])
#print(cashtag_list[5:14])
#sys.exit()

'''
--------------------------------------------------------------------------------
---------------------------- RESTORING CLASSIFIER ------------------------------
--------------------------------------------------------------------------------
'''
if exit_flag == 0:
    f = open('classifier.pckl', 'rb')
    classifier = pickle.load(f)
    f.close()
    
    f = open('train_tweets.pckl', 'rb')
    train_tweets = pickle.load(f)
    f.close()


f = open('df_tweets_by_company.pckl', 'rb')
df_tweets_by_company = pickle.load(f)
f.close()

elapsed_time = time.time() - start_time
print('\ntime elapsed restoring classifier and tweets: '+ str(elapsed_time)) 



'''
////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////
'''
if exit_flag == 1:
    #print(old_cashtag_list[0])
    for cashtag in old_cashtag_list:
        print(cashtag, len(df_tweets_by_company[cashtag]))
        
    sys.exit()

if concatenate_flag == 1:
    f = open('df_tweets_by_company_with_sentiment_analysis.pckl', 'rb')
    df_tweets_by_company = pickle.load(f)
    f.close()
'''
////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////
'''





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
tweet = 'happy bad'
print('Tweet: ' + tweet)
print('Sentiment: ' + classifier.classify(extract_features(tweet.split())))
#print(classifier.show_most_informative_features(32))

dist = classifier.prob_classify(extract_features(tweet.split()))
for label in dist.samples():
    print("%s: %f" % (label, dist.prob(label)))
    sum = dist.prob('positive') - dist.prob('negative')
print(sum)
'''

#print(df_tweets_by_company['$ZTS'])
#sys.exit()


j = 1
old_cashtag = cashtag_list[0]
for cashtag in cashtag_list:
    if j != 1:
        print(time.time() - initial_cashtag, old_cashtag)
        initial_cashtag = time.time()
        old_cashtag = cashtag
        
    print(j, ' ---> ' + cashtag + ' <---')
    j += 1    
    i = 0

    sentiment_array = []
    sentiment_coef_array = []
    positive_coef_array = []
    negative_coef_array = []
    
    length = len(df_tweets_by_company[cashtag])
    
    for tweet in df_tweets_by_company[cashtag]['tweet_text']:
        i += 1
        try:
            sentiment = classifier.classify(extract_features(tweet.split()))
            dist = classifier.prob_classify(extract_features(tweet.split()))
            for label in dist.samples():
                positive_coef = round(dist.prob('positive'), 3)
                negative_coef = round(dist.prob('negative'), 3)
                sentiment_coef = round(round(positive_coef, 3) - round(negative_coef, 3),3)
                    
                
            if -bound <= sentiment_coef <= bound:
                sentiment = 'neutral'
            
            sentiment_array = sentiment_array + [sentiment]
            sentiment_coef_array = sentiment_coef_array + [sentiment_coef]
            positive_coef_array = positive_coef_array + [positive_coef]
            negative_coef_array = negative_coef_array + [negative_coef]
                        
            

        except Exception:
            print('ERROR classifying cashtag: ' + cashtag + ' / text: ' + tweet)
            sentiment_array = sentiment_array + [0]
            sentiment_coef_array = sentiment_coef_array + [0]
            positive_coef_array = positive_coef_array + [0]
            negative_coef_array = negative_coef_array + [0]
            pass
        
        elapsed = time.time() - initial
        initial = time.time()
        print(length-i, elapsed)
        
        
    df_tweets_by_company[cashtag]['sentiment'] = sentiment_array
    df_tweets_by_company[cashtag]['sentiment_coef'] = sentiment_coef_array
    df_tweets_by_company[cashtag]['positive_coef'] = positive_coef_array
    df_tweets_by_company[cashtag]['negative_coef'] = negative_coef_array
    

elapsed_time = time.time() - start_time
print('\ntime elapsed classifying each tweet from remote: '+ str(elapsed_time)) 

'''
--------------------------------------------------------------------------------
--------------------------- STORING CLASSIFICATIONS ----------------------------
--------------------------------------------------------------------------------
'''
f = open('df_tweets_by_company_with_sentiment_analysis.pckl', 'wb')
pickle.dump(df_tweets_by_company, f)
f.close() 

#print(df_tweets_by_company['$MMM'])

elapsed_time = time.time() - start_time
print('\ntime elapsed creating df_tweets_by_company_with_sentiment_analysis: '+ str(elapsed_time))




 

