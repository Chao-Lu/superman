# coding=utf-8
from ORM.MongoDB.base import MongoDB_orm_base,ObjectId
import pymongo
class Tip(MongoDB_orm_base):
    def __init__(self, mongo_control):
        MongoDB_orm_base.__init__(self, mongo_control)
        self.colName = 'tip'

    async def insert(self, tip):
        result = await self.db.insert(tip, self.colName)
        return result
        
    async def get_tip_free(self,condition,sortby,sort,limit,skip):
        tiplist = await self.db.get_document_list(condition, sortby, sort, limit, skip, self.colName)
        for i in range(len(tiplist)):
            tiplist[i] = self.brief_tip(tiplist[i])
        return tiplist
        
    async def update(self,id,tip_order):
        condition = {'_id':ObjectId(id)}
        post = {'$set':tip_order}
        await self.db.update(condition, post, self.colName)

    async def get_by_orderNumber(self,order_number):
        condition = {'tipOrderNumber':str(order_number)}
        tip = await self.db.get_document_one(condition, self.colName)
        return tip

    async def get_by_id(self,tip_id):
        condition = {'_id':ObjectId(tip_id)}
        tip = await self.db.get_document_one(condition, self.colName)
        return tip

    async def find_by_to_user_id(self,to_user_id):
        condition = {'to_user_id':str(to_user_id)}
        tiplist = await self.db.get_document_list(condition, '_id', '-', 1000, 0, self.colName)
        return tiplist

    async def find_by_to_event_id(self,to_event_id):
        condition = {'to_user_id':str(to_event_id), 'state':'accpaid'}
        tiplist = await self.db.get_document_list(condition, '_id', '-', 1000, 0, self.colName)
        return tiplist
        
    def brief_tip(self, tip):
        brieftip = self.db.brief_tip(tip)
        return brieftip
