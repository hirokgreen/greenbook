from sqlalchemy import *
from models import *
import json


class Chat_Add():

    def __init__(self, txt, con, con2, jsn):
        self.con = con
        self.con2 = con2
        self.jsn = jsn
        self.txt = txt

    def add(self):
        #t1 = Table(str(self.con), metadata, autoload=True)
        table1 = Table(str(self.con), metadata, autoload=False)
        if table1.exists():
            f = self.txt.replace("\n", "")
            ins = text('INSERT INTO ' + str(self.con) +
                       '(myself,friend) VALUES("' + f + '","n/a")')
            db.engine.execute(ins)
            sql = text('select * from ' + str(self.con) + '')
            result = db.engine.execute(sql)
            for item in result:
                self.jsn.append({"frnd": item.friend, "self": item.myself})
                # print item.friend,item.myself
        else:
            f = self.txt.replace("\n", "")
            ins = text('INSERT INTO ' + str(self.con2) +
                       '(friend,myself) VALUES("' + f + '","n/a")')
            db.engine.execute(ins)
            sql = text('select * from ' + str(self.con2) + '')
            result = db.engine.execute(sql)
            for item in result:
                self.jsn.append({"frnd": item.myself, "self": item.friend})
        return self.jsn


class Chat_view():

    def __init__(self, t, con, jsn):
        self.con = con
        self.jsn = jsn
        self.t = t

    def view(self):
        if self.t == 't1':
            sql = text('select * from ' + str(self.con) + '')
            result = db.engine.execute(sql)
            for item in result:
                self.jsn.append({"frnd": item.friend, "self": item.myself})

        else:
            sql = text('select * from ' + str(self.con) + '')
            result = db.engine.execute(sql)
            for item in result:
                self.jsn.append({"frnd": item.myself, "self": item.friend})
        return self.jsn

#jsn = [{ "frnd":"lolo" , "self":"bgb" }]
#c = Chat_Add('g6','g7',jsn)
# print c.add()
