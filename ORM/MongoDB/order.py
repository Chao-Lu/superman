# coding=utf-8
from ORM.MongoDB.base import MongoDB_orm_base,ObjectId
import pymongo
class Order(MongoDB_orm_base):
    def __init__(self, mongo_control):
        MongoDB_orm_base.__init__(self, mongo_control)
        self.colName = 'order'
        

        
    async def update(self,id,order):
        condition = {'_id':ObjectId(id)}
        order = {'$set':order}
        await self.db.update(condition, order, self.colName)
        
    async def get_order_free(self,condition,sortby,sort,limit=10000,skip=0):
        orderlist = await self.db.get_document_list(condition, sortby, sort, limit, skip, self.colName)
        for i in range(len(orderlist)):
            orderlist[i] = self.brief_order(orderlist[i])
        return orderlist
        
    async def get_by_id(self, id):
        condition = {'_id':ObjectId(id)}
        order = await self.db.get_document_one(condition, self.colName)        
        return order
    
    async def get_by_orderNumber(self, orderNumber):
        condition = {'orderNumber':orderNumber}
        order = await self.db.get_document_one(condition, self.colName)
        return order
    
    async def get_event_orderlist_length(self,event_id):
        condition = {'belonged':str(event_id)}
        count = await self.db.get_document_count(condition, self.colName)
        return count

    async def get_user_orderlist(self,user_id):
        condition = {'belonged':str(user_id)}
        orderlist = await self.db.get_document_list(condition, '_id', '-', 1000, 0, self.colName)
        return orderlist

    async def insert(self, order):
        result = await self.db.insert(order, self.colName)
        return result
        
    async def delete(self, order_id):
        condition = {'_id': order_id}
        await self.db.delete(condition, self.colName)

    async def insert_comment_id(self,order_id,comment_id):
        condition = {'_id':ObjectId(order_id)}
        order = {'$set':{'comment_id':str(comment_id)}}
        await self.db.update(condition, order, self.colName)

    def brief_order(self,order):
        brieforder = self.db.brief_order(order)
        return brieforder
