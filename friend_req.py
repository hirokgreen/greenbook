from sqlalchemy import *
from models import *

class Friend():
    def __init__(self,u_id,fid):
        self.to_be_add_to_user = fid
        self.to_be_add_to_frnd = u_id
        self.fid = fid.replace("green", "")
        self.u_id = u_id.replace("green", "")
        self.table = Table('users', metadata, autoload=True)


    def add(self):
        ##add friend id to user's out_friend_req
        query = select([self.table.c.out_friend_req],self.table.c.id==int(self.u_id)).execute()
        previous_req = str(query.fetchone()[0])
        modified_req = str(previous_req +";"+ self.to_be_add_to_user)
        self.table.update(self.table.c.id == int(self.u_id) , values=({'out_friend_req':modified_req}) ).execute()

        ## add user id to friends in_friend_req
        query = select([self.table.c.in_friend_req],self.table.c.id==int(self.fid)).execute()
        previous_req = str(query.fetchone()[0])
        modified_req = str(previous_req +";"+ self.to_be_add_to_frnd)
        self.table.update(self.table.c.id == int(self.fid) , values=({'in_friend_req':modified_req}) ).execute()

    def check_friend(self):
        #chech if member is friend of current_user or others status
        query = select([self.table.c.friend,self.table.c.out_friend_req,self.table.c.in_friend_req],self.table.c.id==int(self.u_id)).execute()
        for row in query:
            user_f_list = str(row[0])
            user_sent_f_list = str(row[1])
            user_incoming_f_list = str(row[2])

        flist = user_f_list.split(";")
        foutlist = user_sent_f_list.split(";")
        finlist = user_incoming_f_list.split(";")
        if str(self.to_be_add_to_user) in flist:
            return "friend"
        if (self.to_be_add_to_user) not in flist:
            if str(self.to_be_add_to_user) in foutlist:
                return "request_sent"
            if str(self.to_be_add_to_user) in finlist:
                return "accept"
        return "not_friend"

    def accept_request(self):
        query = select([self.table.c.friend,self.table.c.in_friend_req],self.table.c.id==int(self.u_id)).execute()
        f_query = select([self.table.c.friend,self.table.c.out_friend_req],self.table.c.id==int(self.fid)).execute()
        for row in query:
            user_f = str(row[0])
            user_incoming = str(row[1])
        for row2 in f_query:
            mem_f = str(row2[0])
            mem_out_f = str(row2[1])
        user_f_list = append_id(self.to_be_add_to_user, user_f)
        mem_f_list = append_id(self.to_be_add_to_frnd, mem_f)
        user_in_list = remove_id(self.to_be_add_to_user, user_incoming)
        mem_out_list = remove_id(self.to_be_add_to_frnd, mem_out_f)
        self.table.update(self.table.c.id == int(self.u_id) , values=({'friend':user_f_list,'in_friend_req':user_in_list})).execute()
        self.table.update(self.table.c.id == int(self.fid) , values=({'friend':mem_f_list,'out_friend_req':mem_out_list})).execute()

    def unfriend(self):
        query = select([self.table.c.friend],self.table.c.id==int(self.u_id)).execute()
        f_query = select([self.table.c.friend],self.table.c.id==int(self.fid)).execute()
        user_f = str(query.fetchone()[0])
        friend_f = str(f_query.fetchone()[0])
        flist = remove_id(self.to_be_add_to_user, user_f)
        f_flist = remove_id(self.to_be_add_to_frnd, friend_f)
        self.table.update(self.table.c.id == int(self.u_id) , values=({'friend':flist})).execute()
        self.table.update(self.table.c.id == int(self.fid) , values=({'friend':f_flist})).execute()

    def cancel_request(self):
        query = select([self.table.c.out_friend_req],self.table.c.id==int(self.u_id)).execute()
        f_query = select([self.table.c.in_friend_req],self.table.c.id==int(self.fid)).execute()
        user_out = str(query.fetchone()[0])
        friend_in = str(f_query.fetchone()[0])
        flist = remove_id(self.to_be_add_to_user, user_out)
        f_flist = remove_id(self.to_be_add_to_frnd, friend_in)
        self.table.update(self.table.c.id == int(self.u_id) , values=({'out_friend_req':flist})).execute()
        self.table.update(self.table.c.id == int(self.fid) , values=({'in_friend_req':f_flist})).execute()

    def reject_request(self):
        query = select([self.table.c.in_friend_req],self.table.c.id==int(self.u_id)).execute()
        f_query = select([self.table.c.out_friend_req],self.table.c.id==int(self.fid)).execute()
        user_in = str(query.fetchone()[0])
        friend_out = str(f_query.fetchone()[0])
        flist = remove_id(self.to_be_add_to_user, user_in)
        f_flist = remove_id(self.to_be_add_to_frnd, friend_out)
        self.table.update(self.table.c.id == int(self.u_id) , values=({'in_friend_req':flist})).execute()
        self.table.update(self.table.c.id == int(self.fid) , values=({'out_friend_req':f_flist})).execute()





def append_id(id,s):
    userlist = s.split(";")
    userlist.append(str(id))
    modified = ";".join(userlist)

    return modified

def remove_id(id,s):
    userlist = s.split(";")
    userlist.remove(str(id))
    modified = ";".join(userlist)

    return modified