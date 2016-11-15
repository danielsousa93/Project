import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('193.136.221.43', username='dsousa', password='tese123')

ftp = ssh.open_sftp()

#ftp.get('tweetsDB.csv', 'tweetsDB - fromremote.csv')
#ftp.get('tweetsDB new_with_got.csv', 'tweetsDB - newfromremote.csv')
#ftp.get('state_of_stream.csv', 'state_of_stream.csv')
ftp.get('DB user_details.csv', 'DB user_details.csv')
#ftp.get('nohup.out', 'nohup.out')

print('.csv files downloaded.')

ftp.close()
ssh.close()


'''COMMAND TO RUN SCRIPT IN BACKGROUND
nohup python3 -u TweetsDB_gen.py </dev/null >/dev/null 2>&1 &
'''
