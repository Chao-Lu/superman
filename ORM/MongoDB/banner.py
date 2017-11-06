# coding=utf-8
from ORM.MongoDB.base import MongoDB_orm_base,ObjectId
import pymongo
class Banner(MongoDB_orm_base):
    def __init__(self, mongo_control):
        MongoDB_orm_base.__init__(self, mongo_control)
        self.colName = 'banner' 
        
    async def update(self,id,banner):
        condition = {'_id':ObjectId(id)}
        banner = {'$set':banner}
        await self.db.update(condition, banner, self.colName)

    async def updateAll(self,condition,banner):
        await self.db.update(condition, banner, self.colName)

    async def get_banner_free(self,condition,sortby,sort,limit,skip):
        bannerlist = await self.db.get_document_list(condition, sortby, sort, limit, skip, self.colName)
        return bannerlist
        
    async def get_by_id(self, id):
        condition = {'_id':ObjectId(id)}
        banner = await self.db.get_document_one(condition, self.colName)
        return banner
            
    async def insert(self, banner):
        result = await self.db.insert(banner, self.colName)
        return result
        
    async def delete(self, banner_id):
        condition = {'_id': banner_id}
        await self.db.delete(condition, self.colName)
            
    def brief_banner(self,banner):
        briefbanner = self.db.brief_banner(banner)
        return briefbanner
