# coding=utf-8
from ORM.MongoDB.base import MongoDB_orm_base,ObjectId
import    operator
import pymongo
class Master(MongoDB_orm_base):
    def __init__(self, mongo_control):
        MongoDB_orm_base.__init__(self, mongo_control)
        self.colName = 'master'
        
    async def delete(self,master_id):
        condition = {'_id': master_id}
        await self.db.delete(condition, self.colName)
        
    async def get_master_free(self,condition,sortby,sort,limit,skip):
        masterlist = await self.db.get_document_list(condition, sortby, sort, limit, skip, self.colName)
        for i in range(len(masterlist)):
            masterlist[i] = self.brief_master(masterlist[i])
        return masterlist
        
    async def get_by_id(self, id):
        condition = {'_id':ObjectId(id)}
        master = await self.db.get_document_one(condition, self.colName)
        return master
    
    async def get_by_user(self, id):
        condition = {'userId':str(id)}
        master = await self.db.get_document_one(condition, self.colName)
        return master
    
    async def insert(self, master):
        result = await self.db.insert(master, self.colName)
        return result
        
    async def update(self, id, master):
        condition = {'_id':ObjectId(id)}
        master = {'$set':master}
        await self.db.update(condition, master, self.colName)

    #增加 money
    async def add_money_by_user_id(self, money_type, user_id, money):
        condition = {'userId':str(user_id)}
        master = {'$inc':{str(money_type):int(money)}}
        await self.db.update(condition, master, self.colName)
        

    #减少 money
    async def reduce_money_by_user_id(self,money_type,user_id,money):
        condition = {'userId':str(user_id)}
        master = {'$inc':{str(money_type):(-int(money))}}
        await self.db.update(condition, master, self.colName)
                
    def brief_master(self,master):
        briefmaster = self.db.brief_master(master)
        return briefmaster

        




