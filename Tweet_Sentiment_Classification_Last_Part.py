import time
import pickle
from SP500_DB import cashtag_list
from numpy import sort
import csv

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
print(sentiment_score_set)

'''
with open('tweetsDB - newfromremote oneweek.csv', 'r', encoding="utf-8") as file:
    reader = csv.reader(file, delimiter=",")
    for line in reader:
        if line[0] == '$PEG':
            print(line[1], line[5])
'''

