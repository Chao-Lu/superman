# coding=utf-8
from ORM.MongoDB.base import MongoDB_orm_base,ObjectId
import pymongo
import random
class Circle(MongoDB_orm_base):
    def __init__(self, mongo_control):
        MongoDB_orm_base.__init__(self, mongo_control)
        self.colName = 'circle' 
        
    async def update(self,id,circle):
        condition = {'_id':ObjectId(id)}
        circle = {'$set':circle}
        await self.db.update(condition, circle, self.colName)
        
    async def get_circle_free(self,condition,sortby,sort,limit=10000,skip=0):
        circlelist = await self.db.get_document_list(condition, sortby, sort, limit, skip, self.colName)
        return circlelist
        
    async def get_by_id(self, id):
        condition = {'_id':ObjectId(id)}
        circle = await self.db.get_document_one(condition, self.colName)
        return circle
    
    async def get_by_circleNumber(self, circleNumber):
        condition = {'circleNumber':circleNumber}
        circle = await self.db.get_document_one(condition, self.colName)
        return circle
                
    async def insert(self, circle):
        result = await self.db.insert(circle, self.colName)
        return result
        
    async def delete(self, circle_id):
        condition = {'_id': circle_id}
        await self.db.delete(condition, self.colName)

    async def insert_seenum(self,circle_id):
        condition = {'_id':ObjectId(circle_id)}
        circle = {'$inc':{'seeNum':random.randint(1,5)}}
        await self.db.update(condition, circle, self.colName)
        
    async def insert_post(self,circle_id,post_id):
        condition = {'_id':ObjectId(circle_id)}
        circle = {'$addToSet':{'postList':post_id}}
        await self.db.update(condition, circle, self.colName)


    async def remove_post(self,circle_id,post_id):
        condition = {'_id':ObjectId(circle_id)}
        circle = {'$pull':{'postList':post_id}}
        await self.db.update(condition, circle, self.colName)

        
    async def insert_special_post(self,circle_id,post_id):
        condition = {'_id':ObjectId(circle_id)}
        circle = {'$addToSet':{'specialPost':post_id}}
        await self.db.update(condition, circle, self.colName)

    async def remove_special_post(self,circle_id,post_id):
        condition = {'_id':ObjectId(circle_id)}
        circle = {'$pull':{'specialPost':post_id}}
        await self.db.update(condition, circle, self.colName)
        
    async def insert_top_post(self,circle_id,post_id):
        condition = {'_id':ObjectId(circle_id)}
        circle = {'$addToSet':{'topPost':post_id}}
        await self.db.update(condition, circle, self.colName)

    async def remove_top_post(self,circle_id,post_id):
        condition = {'_id':ObjectId(circle_id)}
        circle = {'$pull':{'topPost':post_id}}
        await self.db.update(condition, circle, self.colName)
        
    async def insert_manager(self,circle_id,user_id):
        condition = {'_id':ObjectId(circle_id)}
        circle = {'$addToSet':{'circleManager':user_id}}
        await self.db.update(condition, circle, self.colName)

    async def remove_manager(self,circle_id,user_id):
        condition = {'_id':ObjectId(circle_id)}
        circle = {'$pull':{'circleManager':user_id}}
        await self.db.update(condition, circle, self.colName)
        
    async def insert_mode(self,circle_id,mode_id):
        condition = {'_id':ObjectId(circle_id)}
        circle = {'$addToSet':{'modeList':mode_id}}
        await self.db.update(condition, circle, self.colName)

    async def remove_mode(self,circle_id,mode_id):
        condition = {'_id':ObjectId(circle_id)}
        circle = {'$pull':{'modeList':mode_id}}
        await self.db.update(condition, circle, self.colName)
        
    async def insert_affiche(self,circle_id,post_id):
        condition = {'_id':ObjectId(circle_id)}
        circle = {'$addToSet':{'afficheList':post_id}}
        await self.db.update(condition, circle, self.colName)

    async def remove_affiche(self,circle_id,post_id):
        condition = {'_id':ObjectId(circle_id)}
        circle = {'$pull':{'afficheList':post_id}}
        await self.db.update(condition, circle, self.colName)
        
    def brief_circle(self,circle):
        brief_circle = self.db.brief_circle(circle)
        briefcircle['postNum']=len(briefcircle['postList'])
        briefcircle.pop('postList')
        return briefcircle
