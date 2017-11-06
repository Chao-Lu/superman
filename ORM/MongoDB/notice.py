# coding=utf-8
from ORM.MongoDB.base import MongoDB_orm_base,ObjectId
import pymongo
class Notice(MongoDB_orm_base):
    def __init__(self, mongo_control):
        MongoDB_orm_base.__init__(self, mongo_control)
        self.colName = 'notice'
    
    async def handle(self,id):
        condition = {'_id':ObjectId(id)}
        notice = {'$set':{'state':'1'}}
        await self.db.update(condition, notice, self.colName)
        
    async def update(self,id,notice):
        condition = {'_id':ObjectId(id)}
        notice = {'$set':notice}
        await self.db.update(condition, notice, self.colName)
        
    async def insert_source(self,id,source):
        condition = {'_id':ObjectId(id)}
        notice = {'$addToSet':{'source':source}}
        await self.db.update(condition, notice, self.colName)
        
    async def get_count(self,condition):
        count = await self.db.get_document_count(condition, self.colName)
        return count

    async def delete(self, notice_id):
        condition = {'_id': notice_id}
        await self.db.delete(condition, self.colName)
            
    async def get_notice_free(self,condition,sortby,sort,limit,skip):
        noticelist = await self.db.get_document_list(condition, sortby, sort, limit, skip, self.colName)
        for i in range(len(noticelist)):
            noticelist[i] = self.brief_notice(noticelist[i])
        return noticelist
        
    async def get_by_id(self, id):
        condition = {'_id':ObjectId(id)}
        notice = await self.db.get_document_one(condition, self.colName)
        return notice
        
    async def get_by_user(self, id):
        condition = {'user_id':str(id)}
        notice = await self.db.get_document_one(condition, self.colName)
        return notice    
                
    async def insert(self, notice):
        result = await self.db.insert(notice, self.colName)
        return result
        
    def brief_notice(self,notice):
        briefnotice = self.db.brief_notice(notice)
        return briefnotice
