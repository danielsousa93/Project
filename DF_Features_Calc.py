import pandas as pd
import time

start_time = time.time()


df_tweets = pd.read_pickle('df_tweets - Backup.h5')
df_user = pd.read_pickle('df_user - Backup.h5')





elapsed_time = time.time() - start_time
print('\ntime elapsed: '+ str(elapsed_time))