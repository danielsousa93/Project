import paramiko


ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('193.136.221.43', username='dsousa', password='tese123')

'''
stdin, stdout, stderr =  ssh.exec_command("uptime")
print(stdout.readlines())

stdin, stdout, stderr =  ssh.exec_command("sudo dmesg")
print(stdout.readlines())

stdin.write('tese123\n')
stdin.flush()
data = stdout.read
'''

ftp = ssh.open_sftp()
ftp.put('test_remote.py', '/tmp/test.py')
ftp.put('TweetsDB_gen.py', '/tmp/TweetsDB_gen.py')
ftp.put('SP500_DB.py', '/tmp/SP500_DB.py')

stdin,stdout,stderr = ssh.exec_command('python /tmp/test.py', get_pty=True)
#stdin,stdout,stderr = ssh.exec_command('python /tmp/TweetsDB_gen.py', get_pty=True)
for line in stdout:
    print(line)

#ftp.get('/tmp/tweetsDB.csv', 'tweetsDB - fromremote.csv')


ftp.close()
ssh.close()
