from sqlalchemy import *
from models import *

class Tag():
    def __init__(self, p_id, f_id, owner):
        self.p_id = p_id
        self.f_id = f_id
        self.owner = owner
        #self.f_id = f_id.replace("green", "")
        #self.u_id = u_id.replace("green", "")
        self.table = Table('tag', metadata, autoload=True)


    def add(self):
        post = select([self.table.c.post_id],self.table.c.post_id==self.p_id).execute()
        if post.fetchone() == None:
            self.table.insert().execute({'post_id': self.p_id, 'owner_id': self.owner})
        ##add friend id to user's out_friend_req
        query = select([self.table.c.friends_id],self.table.c.post_id==self.p_id).execute()
        tag_list = str(query.fetchone()[0])
        modified_tag_list = str(tag_list +";"+ self.f_id)
        self.table.update(self.table.c.post_id == self.p_id, values=({'friends_id':modified_tag_list})).execute()

