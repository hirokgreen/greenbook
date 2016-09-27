from sqlalchemy import *
from models import *
#post = PostTable('post_01')
#table = post.posttable()
#table.create()

#insert into table
#table.insert().execute(title='commit',  description='sqlalchemy here')


# insert with json method
#table.insert().execute({'title': 'first post', 'description': 'i\'m here'},
         # {'title': '2nd post', 'description': 'hello again'})

table = Table('users', metadata, autoload=True)
rs = select([table.c.friend],table.c.id==int('6')).execute()
#rs = table.select().order_by(table.c.id.desc()).execute()
# retrive table data
#rs = table.select().execute()
row = rs.fetchone()[0]
print row
#print 'title:', row['title']
#print 'description:', row[table.c.description]
    #print row.uname, '::', row.password,'.'
#if rs.fetchone()[0] != None:
#    print str(rs.fetchone()[0])
#table.update(table.c.id == '56' , values=({'out_friend_req':'lol'}) ).execute()
#print "done"


#stmt = update(users).where(users.c.id==5).\
 #       values(name='user #5')

#t1 = Table('green6_green7', metadata, autoload=True)
#table1 = Table('green6_green7', metadata, autoload=False)
#table2 = Table('green7_green6', metadata, autoload=False)

#if table1.exists():
    #t1.insert().execute({'myself':'lol','friend':'na'})
    #print 'lol'
   # sql = text('select * from '+str('green6_green7')+'')
   #result = db.engine.execute(sql)
    #rs = t1.select().execute()
    #for item in rs:
        #print item.friend,item.myself
#else:
    #t2 = Table('green7_green6', metadata, autoload=True)
    #print 'bal'

