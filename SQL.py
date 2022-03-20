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

        self.version = self.version()
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
    
    def GetHeadList(self, table:str):
        if not table in self.tables: return []
        head = self.GetHead(table)

        ndata = {}
        for req in head[0]:
            rname = req[0]
            rvalu = req[1:]
            ndata[rname] = rvalu
        return ndata
    
    def ToINS(self, table:str, data:dict):
        if not table in self.tables: return {}
        hels = self.GetHeadList(table)
        key = []
        val = []

        for i in data:
            key.append(i)
            if i in hels:

                rtype = hels[i][0]
                if rtype == 16:
                    if data[i] == 1: val.append('1')
                    else: val.append('0')
                else:
                    if data[i] == None:
                        val.append("NULL")
                    else:
                        val.append( "'{}'".format(str(data[i])) )

            else:
                if data[i] == None:
                    val.append("NULL")
                else:
                    val.append( "'{}'".format(str(data[i])) )

        key = "({})".format(', '.join(key))
        val = "({})".format(', '.join(val))

        return key, val

        
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
            try:
                if len(value) > rlong: return {}
            except:
                try:
                    if len(str(value)) > rlong: return {}
                except:pass
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
    
    def execute(self, cmd:str):
        cursor = self.db.cursor()
        try:
            cursor.execute(cmd)
            self.db.commit()
            res = True
        except:
            self.db.rollback()
            res = False
        finally:
            cursor.close()
            return res
    
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

    def GetData(self, table:str, where:dict={}, limit:int=0, ntype=list, nopin=False) -> list:
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
            temp = []
            i = list(i)

            if nopin:
                for s in i:
                    if type(s) in [str, int, list, dict]:
                        temp.append(s)
                    else:
                        temp.append(str(s))
                i = temp

            if ntype == dict: ndata.append( dict(zip(head,i)) )
            elif ntype == list: ndata.append(i)
            
        return ndata

    def NewData(self, table:str, data:dict, fore_noid:bool=False, fore_load=True):
        if not table in self.tables:return
        Base = 'INSERT INTO {}'.format(table)
        head = self.GetHead(table)[1]

        if fore_load: Data = self.Loadin(head, data, ntype=dict)[0]
        else: Data = data
        Data = self.ComparePass(table, Data)
        print(Data)
        if Data == {}: return False

        if not fore_noid:
            try:Data.pop('id')
            except:pass
        
        key, val = self.ToINS(table, Data)
        Base += " {key} VALUES {val}".format(key=key, val=val)

        print(Base)

        res = self.execute(Base)
        return res

    def Delete(self, table:str, where:dict):
        if not table in self.tables:return
        Base = 'DELETE FROM {}'.format(table)
        head = self.GetHeadList(table)

        stands = []
        for key in where:
            if not key in head:continue
            if "'" in where[key]:continue
            stands.append("{key}='{val}'".format(key=key, val=where[key]))
        stands = ' AND '.join(stands)
        if stands: Base += ' WHERE ' + stands

        res = self.execute(Base)
        return res
    
    def close(self):
        self.db.close()