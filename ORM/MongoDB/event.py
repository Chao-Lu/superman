# coding=utf-8
from ORM.MongoDB.base import MongoDB_orm_base,ObjectId
import pymongo
class Event(MongoDB_orm_base):
    def __init__(self, mongo_control):
        MongoDB_orm_base.__init__(self, mongo_control)
        self.colName = 'event'
        
    async def update(self,id,event):
        condition = {'_id':ObjectId(id)}
        event = {'$set':event}
        await self.db.update(condition, event, self.colName)
        
    async def get_event_count(self,condition):
        count = await self.db.get_document_count(condition, self.colName)
        return count
            
    async def get_event_free(self,condition,sortby,sort,limit,skip):
        eventlist = await self.db.get_document_list(condition, sortby, sort, limit, skip, self.colName)
        for i in range(len(eventlist)):
            eventlist[i] = self.brief_event(eventlist[i])
        return eventlist
        
    async def get_by_id(self, id):
        condition = {'_id':ObjectId(id)}
        event = await self.db.get_document_one(condition, self.colName)
        return event
            
    async def insert(self, event):
        result = await self.db.insert(event, self.colName)
        return result
        
    async def delete(self, event_id):
        condition = {'_id': event_id}
        await self.db.delete(condition, self.colName)

    async def insert_like(self,event_id,user_id):
        condition = {'_id':ObjectId(event_id)}
        event = {'$addToSet':{'likeUserList':str(user_id)}}
        await self.db.update(condition, event, self.colName)
    
    async def remove_like(self,event_id,user_id):
        condition = {'_id':ObjectId(event_id)}
        event = {'$pull':{'likeUserList':str(user_id)}}
        await self.db.update(condition, event, self.colName)
    
    async def insert_comment(self,event_id,comment_id):
        condition = {'_id':ObjectId(event_id)}
        event = {'$addToSet':{'commentList':str(comment_id)}}
        await self.db.update(condition, event, self.colName)

    async def remove_comment(self,event_id,comment_id):
        condition = {'_id':ObjectId(event_id)}
        event = {'$pull':{'commentList':str(comment_id)}}
        await self.db.update(condition, event, self.colName)
        
    def brief_event(self,event):
        briefevent = self.db.brief_event(event)
        return briefevent

