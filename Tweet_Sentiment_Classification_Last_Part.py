import time
import pickle
from SP500_DB import cashtag_list
from numpy import sort
from pprint import pprint
import csv
import sys

#193.136.221.43


start_time = time.time()
'''
--------------------------------------------------------------------------------
------------------------- RESTORING SENTIMENT_ARRAY ----------------------------
--------------------------------------------------------------------------------
'''
f = open('classifications.pckl', 'rb')
sentiment_array = pickle.load(f)
f.close()

elapsed_time = time.time() - start_time
print('\ntime elapsed restoring sentiment_array: '+ str(elapsed_time)) 



sentiment_score_set = []
old_cashtag = sentiment_array[0][0]
sentiment_score = 0
for (cashtag, user_name, date, sentiment, sentiment_coef, positive_coef, negative_coef, text) in sentiment_array:
    if cashtag == old_cashtag:
        sentiment_score += sentiment_coef  
    else:
        print(old_cashtag, sentiment_score)
        sentiment_score_set.append((old_cashtag,sentiment_score))
        old_cashtag = cashtag
        sentiment_score = 0
        sentiment_score += sentiment_coef
print(cashtag, sentiment_score)
sentiment_score_set.append((old_cashtag,sentiment_score))

sorted_sentiment_score_set = sentiment_score_set
sorted_sentiment_score_set.sort(key=lambda tup: tup[1], reverse = True)


'''
--------------------------------------------------------------------------------
--------------------------- STORING CLASSIFICATIONS ----------------------------
--------------------------------------------------------------------------------
'''

f = open('sentiment_score_set.pckl', 'wb')
pickle.dump(sentiment_score_set, f)
f.close()    

elapsed_time = time.time() - start_time
print('\ntime elapsed storing classifications: '+ str(elapsed_time)) 

