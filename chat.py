from sqlalchemy import *
from models import *
import json
class Chat_Add():
    def __init__(self,con,con2,jsn):
        self.con = con
        self.con2 = con
        self.jsn = jsn
    def add(self):
        #t1 = Table(str(self.con), metadata, autoload=True)
        table1 = Table(str(self.con), metadata, autoload=False)
        if table1.exists():
            #t1.insert().execute({'myself':'lol','friend':'na'})
            #rs = t1.select().execute()
            sql = text('select * from '+str(self.con)+'')
            result = db.engine.execute(sql)
            for item in result:
                self.jsn.append({"frnd":item.friend,"self":item.myself})
                #print item.friend,item.myself
        else:
            t2 = Table(str(self.con2), metadata, autoload=True)
            #t2.insert().execute({'myself':'na','friend':str(c)})
            rs = t2.select().execute()
            for item in rs:
                self.jsn.append({"frnd":item.myself,"self":item.friend})
        return self.jsn



#jsn = [{ "frnd":"lolo" , "self":"bgb" }]
#c = Chat_Add('g6','g7',jsn)
#print c.add()