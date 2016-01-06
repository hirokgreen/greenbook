
#post = PostTable('post_01')
#table = post.posttable()
#table.create()

#insert into table
#table.insert().execute(title='commit',  description='sqlalchemy here')


# insert with json method
#table.insert().execute({'title': 'first post', 'description': 'i\'m here'},
         # {'title': '2nd post', 'description': 'hello again'})

#table = Table('users', metadata, autoload=True)
#rs = select([table.c.id,table.c.uname,table.c.password],table.c.uname=='greenhirok').execute()
#rs = table.select().order_by(table.c.id.desc()).execute()
# retrive table data
#rs = table.select().execute()
#row = rs.fetchone()
#print 'Id:', row[0]
#print 'title:', row['title']
#print 'description:', row[table.c.description]
#for row in rs:
 #   print str(row[0])
    #print row.uname, '::', row.password,'.'



#stmt = update(users).where(users.c.id==5).\
 #       values(name='user #5')


