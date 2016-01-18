from app import *

like = Table('like', metadata, autoload=True)
s = select([like.c.id]).where(like.c.post_id=='green6_6').where(like.c.user_id=='green9').execute()
for row in s:
    print row[0]




#delete from like where like.id in (select like.id from like where like.user_id='green9' and like.post_id='green6_5')