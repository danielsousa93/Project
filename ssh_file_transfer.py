import paramiko
import tarfile

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('193.136.221.43', username='dsousa', password='tese123')

#193.136.221.43


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
#ftp.put('get_sentiment_tweets.py', 'get_sentiment_tweets.py')
#ftp.put('get_sentiment_tweets_when_errors_occured.py', 'get_sentiment_tweets_when_errors_occured.py')

#ftp.put('tweetsDB sentiment_analysis pos twoyears.csv', 'tweetsDB sentiment_analysis pos twoyears.csv')
#ftp.put('tweetsDB sentiment_analysis neg twoyears.csv', 'tweetsDB sentiment_analysis neg twoyears.csv')
ftp.put('Tweet_Sentiment_Model_Training.py', 'Tweet_Sentiment_Model_Training.py')


#ftp.put('classifier.pckl', 'classifier.pckl')
#ftp.put('train_tweets.pckl', 'train_tweets.pckl')
#ftp.put('Tweet_Sentiment_Classification.py', 'Tweet_Sentiment_Classification.py')

'''
STOCK MARKET ANALYSIS
'''
#ftp.put('get_data_from_yahoo.py', 'get_data_from_yahoo.py')
ftp.put('yahoo_data_parser.py', 'yahoo_data_parser.py')



print('Files upload done.')
ftp.close()
ssh.close()

'''COMMAND TO RUN SCRIPT IN BACKGROUND
nohup python3 -u TweetsDB_gen.py </dev/null >/dev/null 2>&1 &
'''