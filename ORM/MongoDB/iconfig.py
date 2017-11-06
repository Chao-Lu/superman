# coding=utf-8
from ORM.MongoDB.base import MongoDB_orm_base,ObjectId
import pymongo
class Iconfig(MongoDB_orm_base):
    def __init__(self, mongo_control):
        MongoDB_orm_base.__init__(self, mongo_control)
        self.colName = 'iconfig'
        
    async def get_iconfig_free(self,condition,sortby,sort,limit,skip):
        iconfiglist = await self.db.get_document_list(condition, sortby, sort, limit, skip, self.colName)
        return iconfiglist
        
    async def update(self,id,iconfig):
        condition = {'_id':ObjectId(id)}
        iconfig = {'$set':iconfig}
        await self.db.update(condition, iconfig, self.colName)
        
    async def get_by_id(self, id):
        condition = {'_id':ObjectId(id)}
        iconfig = await self.db.get_document_one(condition, self.colName)
        return iconfig
        
    async def get_by_title(self, title):
        condition = {'title':title}
        iconfig = await self.db.get_document_one(condition, self.colName)
        return iconfig    
        
    async def insert(self, iconfig):
        result = await self.db.insert(iconfig, self.colName)
        return result
        
    async def delete(self, iconfig_id):
        condition = {'_id': iconfig_id}
        await self.db.delete(condition, self.colName)
