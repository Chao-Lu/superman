# coding=utf-8
from ORM.MongoDB.base import MongoDB_orm_base,ObjectId
import pymongo
class Mode(MongoDB_orm_base):
    def __init__(self, mongo_client):
        MongoDB_orm_base.__init__(self, mongo_client)
        
    async def update(self,id,mode):
        await self.db.mode.update({'_id':ObjectId(id)},mode)
        
    async def updateS(self,condition,mode):
        await self.db.mode.update(condition,mode)
        
    async def get_mode_free(self,condition,sortby,sort,limit,skip):
        sortlist={
            '+':pymongo.ASCENDING ,
            '-':pymongo.DESCENDING
        }
        cursor = self.db.mode.find(condition)
        cursor.sort(sortby,sortlist[sort]).limit(limit).skip(skip)
        modelist=[]
        async for mode in cursor:
            modelist.append(self.brief_mode(mode))
        return modelist
        
    async def get_by_id(self, id):
        mode = await self.db.mode.find_one({'_id':ObjectId(id)})
        return mode
            
    async def insert(self, mode):
        result=await self.db.mode.insert(mode)
        return result
        
    async def delete(self, mode_id):
        await self.db.mode.delete_many({'_id': mode_id})
    
    async def insert_join(self,id,user_id):
        await self.db.mode.update({'id':ObjectId(id)},{'$addToSet':{'joinList':user_id}})
            
    def brief_mode(self,mode):
        briefmode=self.dict_match(mode,
            {                
                '_id':'',
                'beginTime':'',
                'endTime':'',
                'content':'',
                'belongActivity':'',
                'joinList':[],
                'state':'on',
                'type':'',
                'title':'',
                'avatar':'',
                'entryDate':'',
                'function':'',
            }
        )
        return briefmode
