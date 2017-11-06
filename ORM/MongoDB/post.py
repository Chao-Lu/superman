# coding=utf-8
from ORM.MongoDB.base import MongoDB_orm_base,ObjectId
import pymongo
import random
class Post(MongoDB_orm_base):
    def __init__(self, mongo_control):
        MongoDB_orm_base.__init__(self, mongo_control)
        self.colName = 'post'
        
    async def update(self,id,post):
        condition = {'_id':ObjectId(id)}
        post = {'$set':post}
        await self.db.update(condition, post, self.colName)
        
    async def get_post_free(self,condition,sortby,sort,limit,skip):
        postlist = await self.db.get_document_list(condition, sortby, sort, limit, skip, self.colName)
        for i in range(len(postlist)):
            postlist[i] = self.brief_post(postlist[i])
        return postlist
        
    async def get_by_id(self, id):
        condition = {'_id':ObjectId(id)}
        post = await self.db.get_document_one(condition, self.colName)
        return post
            
    async def insert(self, post):
        result = await self.db.insert(post, self.colName)
        return result
        
    async def delete(self, post_id):
        condition = {'_id': ObjectId(post_id)}
        await self.db.delete(condition, self.colName)
        
    async def insert_seenum(self,id):
        condition = {'_id':ObjectId(id)}
        post = {'$inc':{'seeNum':random.randint(1,5)}}
        await self.db.update(condition, post, self.colName)
        
    async def insert_like(self,id,user_id):
        condition = {'_id':ObjectId(id)}
        post = {'$addToSet':{'likeUserList':str(user_id)}}
        await self.db.update(condition, post, self.colName)
    
    async def remove_like(self,id,user_id):
        condition = {'_id':ObjectId(id)}
        post = {'$pull':{'likeUserList':str(user_id)}}
        await self.db.update(condition, post, self.colName)
    
    async def insert_comment(self,id,comment_id):
        condition = {'_id':ObjectId(id)}
        post = {'$addToSet':{'commentList':str(comment_id)}}
        await self.db.update(condition, post, self.colName)

    async def remove_comment(self,id,comment_id):
        condition = {'_id':ObjectId(id)}
        post = {'$pull':{'commentList':str(comment_id)}}
        await self.db.update(condition, post, self.colName)

    def brief_post(self,post):
        briefpost = self.db.brief_post(post)
        briefpost['likenum']=len(post['likeUserList'])
        briefpost['commentnum']=len(post['commentList'])
        return briefpost
