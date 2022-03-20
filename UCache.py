import json
import os

class UC:
    def __init__(self):
        path = os.path.join(os.getcwd(), '../usercache.json')
        path = os.path.abspath(path)
        self.path = path
        self.data = None
        self.Reload()
    
    def Reload(self):
        with open(self.path, 'r', encoding='utf-8') as f:
            self.data = json.loads(f.read())
    
    def SearchBy(self, key:str, val:str):
        for i in self.data:
            if not key in i:continue
            if i[key] == val: return i
        return