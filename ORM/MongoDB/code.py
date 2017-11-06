# coding=utf-8
from ORM.MongoDB.base import MongoDB_orm_base,ObjectId
import pymongo

class Code(MongoDB_orm_base):
    def __init__(self, mongo_control):
        MongoDB_orm_base.__init__(self, mongo_control)
        self.colName = 'code'

    async def get_by_mobile(self, mobile):
        condition = {'mobile':mobile,'state':'on'}
        code = await self.db.get_document_one(condition, self.colName)
        return code

    async def update(self,mobile,code):
        condition = {'mobile':mobile}
        code = {'$set':code}
        await self.db.update(condition, code, self.colName)
        
    async def insert(self,mobile,code_str,time):
        code = {'mobile':mobile,'code_str':code_str,'time':time,'state':'on'}
        result = await self.db.insert(code, self.colName)
        return result
        
    async def delete(self,mobile):
        condition = {'mobile':mobile}
        await self.db.delete(condition, self.colName)



