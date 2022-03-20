import pymysql
import datetime


class DB:
    def __init__(self, host:str, user:str, password:str, database:str, port:int=3306):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.db = pymysql.connect(host=host, user=user, password=password, database=database, port=port)

        self.tables = self.LoadTables()
    
    def LoadTables(self):
        data = self.fetchall('SHOW TABLES;')
        tlis = []
        for i in data:
            tlis.append(i[0])
        return tlis
    
    def Loadin(self, head:list, data:dict, ntype=dict, defin=''):
        mis = []
        new = []
        for i in head:
            if i in data:
                new.append(data[i])
            else:
                mis.append(i)
                new.append(defin)
        if ntype == dict:
            new = dict(zip(head,new))
            return new, mis
        elif ntype == list:
            return new, None
    
    def Nesary(self, table:str):
        if not table in self.tables: return []
        head = self.GetHead(table)

        need = []
        for req in head[0]:
            rname = req[0]
            rneed = req[6]
            if rneed: need.append(rname)
        return need
        
    def ComparePass(self, table:str, data:dict, define=''):
        if not table in self.tables: return {}
        head = self.GetHead(table)

        ndata = {}
        for req in head[0]:
            rname = req[0]
            rneed = req[6]
            rtype = req[1]
            rlong = req[3]

            if not rname in data:
                if rneed: return {}
                ndata[rname] = define
                continue

            value = data[rname]
            if len(value) > rlong: return {}
            ndata[rname] = value
        
        return ndata
    
    def fetchone(self, cmd:str):
        cursor = self.db.cursor()
        cursor.execute(cmd)
        data = cursor.fetchone()
        cursor.close()
        return data
    
    def fetchall(self, cmd:str):
        cursor = self.db.cursor()
        cursor.execute(cmd)
        data = cursor.fetchall()
        cursor.close()
        return data
    
    def version(self):
        try:data = self.fetchone("SELECT VERSION();")[0]
        except:data = ''
        return data
    
    def head(self, name):
        cursor = self.db.cursor()
        sql = "select * from {};".format(name)
        try:result = cursor.execute(sql)
        except:
            cursor.close()
            return None, None

        desp = cursor.description
        head = [item[0] for item in desp]
        cursor.close()
        return desp, head

    def GetHead(self, table:str) :
        if not table in self.tables:return
        head = self.head(table)
        return head

    def GetData(self, table:str, where:dict={}, limit:int=0, ntype=list) -> list:
        if not table in self.tables:return
        Base = 'SELECT * FROM {}'.format(table)
        head = self.GetHead(table)[1]

        stands = []
        for key in where:
            if not key in head:continue
            if "'" in where[key]:continue
            stands.append("{key}='{val}'".format(key=key, val=where[key]))
        stands = ' AND '.join(stands)
        if stands: Base += ' WHERE ' + stands

        if limit: Base += ' LIMIT {}'.format(str(limit))

        data = self.fetchall(Base)
        ndata = []
        for i in data:
            if ntype == dict: ndata.append( dict(zip(head,list(i))) )
            elif ntype == list: ndata.append( list(i) )
            
        return ndata
    
    def close(self):
        self.db.close()



class LTDB(DB):
    def NewData(self, table:str, data:dict):
        if not table in self.tables:return
        Base = 'INSERT INTO {}'.format(table)
        head = self.GetHead(table)[1]
        Data = self.Loadin(head, data, ntype=dict)[0]