from Data import DB
import hashlib


def MD5(text:str):
    return hashlib.md5(text.encode('utf-8')).hexdigest()


class UserDB:
    def __init__(self, location:str):
        self.db = DB(location)
        self.head = self.db.head
        self.addust = ['name', 'uid', 'email', 'password']
        self.standt = ['uid']
        self.location = location
    
    def SearchBy(self, key, item:str) -> dict:
        if not item in self.head:return
        rows = self.db.SearchCert(key, item)
        if not rows:return {}
        row = rows[0]
        data = self.db.GetRows([row])[0]
        data['row'] = row
        return data
    
    def Add(self, data:dict):
        newid = self.db.GetRows([self.db.ws.max_row])[0]['uid']
        newid = int(newid) + 1
        data['uid'] = newid

        data, mis = self.db.Loadin(data, ntype=dict, defin='None')
        mis = list(set(self.addust).intersection(set(mis)))
        if mis:return 'MIS', mis

        data = self.db.Loadin(data, ntype=list, defin='None')
        self.db.Append(data)
        return newid
    
    def Del(self, uid:int):
        uid = self.db.SearchCert(uid, 'uid')
        if not uid:return
        self.db.DeleteRows(uid)

    def Change(self, uid:int, data:dict):
        row = self.SearchBy(uid, 'uid').get('row')
        data = self.db.LoadinExt(data, row, stop=self.standt)
        print(data)
        self.db.WriteRow(row, data)