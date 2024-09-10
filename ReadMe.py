import time
from datetime import datetime
for i in range(101):
    time.sleep(0.05) 
    print ("\r Loading... {} ".format(i), end="")
print('Done')

print(datetime.now())
while True:
    
    time.sleep(0.5)
    print("\r DateTime : {}".format(datetime.now()),end="")
    
progress=lambda current, total,length=50: print(f'\r Progress : {"█"* int(current*length/total):{length}s} {int(100 *current / total) } %',end='',flush=True)
total_ite=100
for i in range (total_ite +1):
    progress(i, total_ite)
    time.sleep(0.01)



#Get User    
import getpass

username = getpass.getuser()
print("System user name:", username)
