# coding=utf-8
from ORM.MongoDB.base import MongoDB_orm_base,ObjectId
import pymongo
class Index(MongoDB_orm_base):
    def __init__(self, mongo_control):
        MongoDB_orm_base.__init__(self, mongo_control)
        self.colName = 'index'
        
    async def update(self,id,index):
        condition = {'_id':ObjectId(id)}
        index = {'$set':index}
        await self.db.update(condition, index, self.colName)
        
    async def updateAll(self,condition,index):
        await self.db.update(condition, index, self.colName)
            
    async def get_index_free(self,condition,sortby,sort,limit,skip):
        indexlist = await self.db.get_document_list(condition, sortby, sort, limit, skip, self.colName)
        for i in range(len(indexlist)):
            indexlist[i] = self.brief_index(indexlist[i])
        return indexlist
        
    async def get_by_id(self, id):
        condition = {'_id':ObjectId(id)}
        index = await self.db.get_document_one(condition, self.colName)
        return index
            
    async def insert(self, index):
        result = await self.db.insert(index, self.colName)
        return result
        
    async def delete(self, index_id):
        condition = {'_id': index_id}
        await self.db.delete(condition, self.colName)
            
    def brief_index(self,index):
        briefindex = self.db.brief_index(index)
        return briefindex
