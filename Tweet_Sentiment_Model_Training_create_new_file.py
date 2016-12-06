#!/usr/local/bin/python3.5

import csv
import time

#193.136.221.43


start_time = time.time()

csvfile = open('tweetsDB sentiment_analysis pos twoyears 50k.csv','wb')
csvfile = open('tweetsDB sentiment_analysis neg twoyears 50k.csv','wb')

'''
--------------------------------------------------------------------------------
------------------------ CREATE SET OF WORDS FROM FILES ------------------------
--------------------------------------------------------------------------------
'''       
j = 1
with open('tweetsDB sentiment_analysis pos twoyears.csv', 'r', encoding="utf-8") as file:
    reader = csv.reader(file, delimiter=",")
    i = 1
    for line in reader:
        i += 1
        if i == 4:
            i = 1
            j += 1
            print(i*j)
            with open('tweetsDB sentiment_analysis pos twoyears 50k.csv', 'a', encoding='utf-8') as csvfile:
                tweetwriter = csv.writer(csvfile, lineterminator='\n', delimiter = ',')
                tweetwriter.writerow(line)
j=1
with open('tweetsDB sentiment_analysis neg twoyears.csv', 'r', encoding="utf-8") as file:
    reader = csv.reader(file, delimiter=",")
    i = 1
    for line in reader:
        i += 1
        if i == 4:
            i = 1
            j += 1
            print(i*j)
            with open('tweetsDB sentiment_analysis neg twoyears 50k.csv', 'a', encoding='utf-8') as csvfile:
                tweetwriter = csv.writer(csvfile, lineterminator='\n', delimiter = ',')
                tweetwriter.writerow(line)

 

elapsed_time = time.time() - start_time
print('\ntime elapsed reducing size of files of sentiment training: '+ str(elapsed_time)) 



