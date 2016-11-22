import pickle
import csv

pos_stock_words = []
neg_stock_words = []

with open('Loughran & McDonald 2014.cat', 'r', encoding="utf-8") as file:
#with open('tweetsDB - newfromremote onemonth.csv', 'r', encoding="utf-8") as file:
    reader = csv.reader(file)
    for line in reader:
        if line[0][:1] != '\t':
            if line[0] == 'NEGATIVE':
                neg_flag = 1
                pos_flag = 0
            elif line[0] == 'POSITIVE':
                neg_flag = 0
                pos_flag = 1
            else:
                neg_flag = 0
                pos_flag = 0
        else:
            if neg_flag == 1:
                neg_stock_words = neg_stock_words + [line[0][1:-4]]
            elif pos_flag == 1:
                pos_stock_words = pos_stock_words + [line[0][1:-4]]

f = open('pos_stock_words.pckl', 'wb')
pickle.dump(pos_stock_words, f)
f.close() 
f = open('neg_stock_words.pckl', 'wb')
pickle.dump(neg_stock_words, f)
f.close()    

print('Stock Words Set created.')

 
