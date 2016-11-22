import paramiko
import tarfile

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('193.136.221.43', username='dsousa', password='tese123')



#tar = tarfile.open("got3.tar.gz", "w:gz")
#tar.add("D:\LiClipse Workspace\Project\GetOldTweets\got3", arcname="got3.tar.gz")
#tar.close()


ftp = ssh.open_sftp()

'''
COLLECT TWEETS
'''
#ftp.put('SP500_DB.py', 'SP500_DB.py')
#ftp.put('constituents-financials.csv', 'constituents-financials.csv')
#ftp.put('get_tweets_when_errors_occured.py', 'get_tweets_when_errors_occured.py')
#ftp.put('get_tweets_using_got.py', 'get_tweets_using_got.py')

'''
USER DETAILS -- mode = 0/1
'''
#ftp.put('constituents-financials.csv', 'constituents-financials.csv')
#ftp.put('SP500_DB.py', 'SP500_DB.py')
#ftp.put('DB user_details.csv', 'DB user_details.csv')
#ftp.put('get_user_details.py', 'get_user_details.py')

'''
SENTIMENT ANALYSIS
'''
ftp.put('get_sentiment_tweets.py', 'get_sentiment_tweets.py')
ftp.put('get_sentiment_tweets_when_errors_occured.py', 'get_sentiment_tweets_when_errors_occured.py')

#ftp.put('classifier.pckl', 'classifier.pckl')
#ftp.put('train_tweets.pckl', 'train_tweets.pckl')
#ftp.put('Tweet_Sentiment_Classification.py', 'Tweet_Sentiment_Classification.py')

#ftp.put('get_sentiment_tweets_stock_market.py', 'get_sentiment_tweets_stock_market.py')
#ftp.put('get_sentiment_tweets_stock_market_when_errors_occured.py', 'get_sentiment_tweets_stock_market_when_errors_occured.py')
#ftp.put('pos_stock_words.pckl', 'pos_stock_words.pckl')
#ftp.put('neg_stock_words.pckl', 'neg_stock_words.pckl')


print('Files upload done.')
ftp.close()
ssh.close()

'''COMMAND TO RUN SCRIPT IN BACKGROUND
nohup python3 -u TweetsDB_gen.py </dev/null >/dev/null 2>&1 &
'''