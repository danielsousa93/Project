import paramiko
import tarfile

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('193.136.221.43', username='dsousa', password='tese123')



#tar = tarfile.open("got3.tar.gz", "w:gz")
#tar.add("D:\LiClipse Workspace\Project\GetOldTweets\got3", arcname="got3.tar.gz")
#tar.close()


ftp = ssh.open_sftp()
#ftp.put('TweetsDB_gen.py', 'TweetsDB_gen.py')
ftp.put('SP500_DB.py', 'SP500_DB.py')
ftp.put('constituents-financials.csv', 'constituents-financials.csv')
ftp.put('using_got.py', 'using_got.py')
ftp.put('get_user_details.py', 'get_user_details.py')
ftp.put('DB user_details.csv', 'DB user_details.csv')

print('Files upload done.')

ftp.close()
ssh.close()

'''COMMAND TO RUN SCRIPT IN BACKGROUND
nohup python3 -u TweetsDB_gen.py </dev/null >/dev/null 2>&1 &
'''