# coding=utf-8
from ORM.MongoDB.base import MongoDB_orm_base,ObjectId
import pymongo
class Category(MongoDB_orm_base):
    def __init__(self, mongo_control):
        MongoDB_orm_base.__init__(self, mongo_control)
        self.colName = 'category' 

        
    async def update(self,id,category):
        condition = {'_id':ObjectId(id)}
        behave = {'$set':category}
        await self.db.update(condition, behave, self.colName)
        
    async def get_category_free(self,condition,sortby,sort,limit,skip):
        categorylist = await self.db.get_document_list(condition, sortby, sort, limit, skip, self.colName)
        return categorylist
        
    async def get_by_id(self, id):
        condition = {'_id':ObjectId(id)}
        category = await self.db.get_document_one(condition, self.colName)
        return category
            
    async def insert(self, category):
        result = await self.db.insert(category, self.colName)
        return result
        
    async def delete(self, category_id):
        condition = {'_id': category_id}
        await self.db.delete(condition, self.colName)

    def brief_category(self,category):
        brief_category = self.db.brief_category(category)
        return brief_category
