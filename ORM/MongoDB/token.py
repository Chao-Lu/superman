# coding=utf-8
from ORM.MongoDB.base import MongoDB_orm_base
import uuid
import pymongo
from handler.unit.unit import ObjectId
class Token(MongoDB_orm_base):
    def __init__(self, mongo_control):
        MongoDB_orm_base.__init__(self, mongo_control)
        self.colName = 'token'
    
    async def get_by_id(self, id):
        condition = {'_id':ObjectId(id)}
        utoken = await self.db.get_document_one(condition, self.colName)
        return utoken
        
    async def get_by_token(self, token):
        condition = {'accessToken':token}
        utoken = await self.db.get_document_one(condition, self.colName)
        return utoken
        
    async def insert(self, token):
        result = await self.db.insert(token, self.colName)
        return result
    
    async def delete_by_user(self,user_id):
        condition = {'user':user_id}
        await self.db.delete(condition, self.colName)
        
    async def get_by_user(self, id):
        condition = {'userId':ObjectId(id)}
        utoken = await self.db.get_document_one(condition, self.colName)
        return utoken
        
    def produce_token(self):
        token=str(uuid.uuid4())
        return token
        
    async def check_token(self,token):
        utoken = await self.get_by_token(token)
        if utoken is None:
            return None
        else:
            return utoken['user']
    

