import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('193.136.221.43', username='dsousa', password='tese123')

ftp = ssh.open_sftp()

'''
COLLECT TWEETS
'''
#ftp.get('tweetsDB new_with_got.csv', 'tweetsDB - newfromremote.csv')
#ftp.get('state_of_stream.csv', 'state_of_stream.csv')


'''
USER DETAILS
'''
#ftp.get('DB user_details.csv', 'DB user_details.csv')
#ftp.get('DB user_details onemonth.csv', 'DB user_details onemonth.csv')

'''
SENTIMENT ANALYSIS
'''
ftp.get('tweetsDB sentiment_analysis pos twoyears.csv', 'tweetsDB sentiment_analysis pos twoyears.csv')
#ftp.get('tweetsDB sentiment_analysis neg twoyears.csv', 'tweetsDB sentiment_analysis neg twoyears.csv')
ftp.get('state_of_stream sentiment_analysis.csv', 'state_of_stream sentiment_analysis.csv')

#ftp.get('classifications.pckl', 'classifications.pckl')

#ftp.get('tweetsDB sentiment_analysis pos_stock_market twoyears.csv', 'tweetsDB sentiment_analysis pos_stock_market twoyears.csv')
#ftp.get('tweetsDB sentiment_analysis neg_stock_market twoyears.csv', 'tweetsDB sentiment_analysis neg_stock_market twoyears.csv')
#ftp.get('state_of_stream sentiment_analysis stock_market.csv', 'state_of_stream sentiment_analysis stock_market.csv')



print('.csv files downloaded.')
ftp.close()
ssh.close()


'''COMMAND TO RUN SCRIPT IN BACKGROUND
nohup python3 -u TweetsDB_gen.py </dev/null >/dev/null 2>&1 &
'''
