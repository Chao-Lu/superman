# coding=utf-8
from ORM.MongoDB.base import MongoDB_orm_base,ObjectId
import pymongo
class Comment(MongoDB_orm_base):
    def __init__(self, mongo_control):
        MongoDB_orm_base.__init__(self, mongo_control)
        self.colName = 'comment'
    
    async def get_comment_num(self,condition):
        count = await self.db.get_document_count(condition, self.colName)
        return count
    
    async def get_comment_free(self,condition,sortby,sort,limit,skip):
        commentlist = await self.db.get_document_list(condition, sortby, sort, limit, skip, self.colName)
        for i in range(len(commentlist)):
            commentlist[i] = self.brief_comment(commentlist[i])
        return commentlist
        
    async def get_by_id(self, id):
        condition = {'_id':ObjectId(id)}
        comment = await self.db.get_document_one(condition, self.colName)
        return comment

    async def get_by_event_id(self,event_id):
        condition = {'postId':str(event_id)}
        commentlist = await self.db.get_document_list(condition, '_id', '-', 1000, 0, self.colName)
        return commentlist
            
    async def insert(self,comment):
        result = await self.db.insert(comment, self.colName)
        return result
        
    async def delete(self, comment_id):
        condition = {'_id': comment_id}
        await self.db.delete(condition, self.colName)
    
    async def insert_reply(self,comment_id,reply):
        condition = {'_id':ObjectId(comment_id)}
        comment = {'$addToSet':{'replyList':reply}}
        await self.db.update(condition, comment, self.colName)

    async def remove_reply(self,comment_id,reply):
        condition = {'_id':ObjectId(comment_id)}
        comment = {'$pull':{'replyList':reply}}
        await self.db.update(condition, comment, self.colName)
    
    async def insert_like(self,comment_id,user_id):
        condition = {'_id':ObjectId(comment_id)}
        comment = {'$addToSet':{'likeUserList':str(user_id)}}
        await self.db.update(condition, comment, self.colName)

    async def remove_like(self,comment_id,user_id):
        condition = {'_id':ObjectId(comment_id)}
        comment = {'$pull':{'likeUserList':str(user_id)}}
        await self.db.update(condition, comment, self.colName)
    
    async def update(self,id,comment):
        condition = {'_id':ObjectId(id)}
        comment = {'$set':comment}
        await self.db.update(condition, comment, self.colName)        
        
    def brief_comment(self,comment):
        briefcomment = self.db.brief_comment(comment)
        return briefcomment
