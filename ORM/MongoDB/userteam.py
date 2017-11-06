# coding=utf-8
from ORM.MongoDB.base import MongoDB_orm_base,ObjectId
import pymongo
class userTeam(MongoDB_orm_base):
    def __init__(self, mongo_control):
        MongoDB_orm_base.__init__(self, mongo_control)
        self.colName = 'userteam'
        
    async def update(self,id,userteam):
        condition = {'_id':ObjectId(id)}
        userteam = {'$set':userteam}
        await self.db.update(condition, userteam, self.colName)
        
    async def get_userteam_free(self,condition,sortby,sort,limit,skip):
        userteamlist = await self.db.get_document_list(condition, sortby, sort, limit, skip, self.colName)
        for i in range(len(userteamlist)):
            userteamlist[i] = self.brief_userteam(userteamlist[i])
        return userteamlist
        
    async def get_by_id(self, id):
        condition = {'_id':ObjectId(id)}
        userteam = await self.db.get_document_one(condition, self.colName)
        return userteam
            
    async def insert(self, userteam):
        result = await self.db.insert(userteam, self.colName)
        return result
        
    async def delete(self, userteam_id):
        condition = {'_id': userteam_id}
        await self.db.delete(condition, self.colName)
        
    async def insert_member(self,userteam_id,user_id):
        condition = {'_id':ObjectId(userteam_id)}
        userteam = {'$addToSet':{'teamMember':user_id}}
        await self.db.update(condition, userteam, self.colName)
    
    async def remove_member(self,userteam_id,user_id):
        condition = {'_id':ObjectId(userteam_id)}
        userteam = {'$pull':{'teamMember':user_id}}
        await self.db.update(condition, userteam, self.colName)
        
    def brief_userteam(self,userteam):
        briefuserteam = self.db.brief_userteam(userteam)
        return briefuserteam
