from sqlalchemy import *
from models import *
from datetime import datetime

table = Table('users', metadata, autoload=True)
#table.update(table.c.id == 10 ,values=({'time_last_active':datetime.now()}) ).execute()
c = datetime(2016, 2, 22, 22, 11, 19, 789000)
b = datetime(2016, 2, 22, 22, 11, 38, 842000)

e = c+timedelta(seconds=23424)
print e

if c>=b-timedelta(seconds=20):
    print 'online'

diff = b-c

print diff.total_seconds()
dict={}
rs  = table.select(table.c.time_last_active <= datetime.now() - timedelta(seconds=5)).execute()
for i in rs:
    print i