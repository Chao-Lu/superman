# coding=utf-8
from ORM.MongoDB.base import MongoDB_orm_base,ObjectId
import pymongo
class Label(MongoDB_orm_base):
    def __init__(self, mongo_control):
        MongoDB_orm_base.__init__(self, mongo_control)
        self.colName = 'label'
        
    async def update(self,id,label):
        condition = {'_id':ObjectId(id)}
        label = {'$set':label}
        await self.db.update(condition, label, self.colName)
        
    async def updateS(self,condition,label):
        await self.db.update(condition, label, self.colName)
        
    async def get_label_free(self,condition,sortby,sort,limit,skip):
        labellist = await self.db.get_document_list(condition, sortby, sort, limit, skip, self.colName)
        for i in range(len(labellist)):
            labellist[i] = self.brief_label(labellist[i])
        return labellist
        
    async def get_by_id(self, id):
        condition = {'_id':ObjectId(id)}
        label = await self.db.get_document_one(condition, self.colName)
        return label
            
    async def update_labelMap(self,labelMap):
        condition = {'islabelMap':'yes'}
        label = {'$set':{'labelMap':labelMap}}
        await self.db.update(condition, label, self.colName)
        
    async def get_labelMap(self):
        condition = {'islabelMap':'yes'}
        label = await self.db.get_document_one(condition, self.colName)
        if label is None:
            await self.insert({'islabelMap':'yes'})
            condition = {'islabelMap':'yes'}
            label = await self.db.get_document_one(condition, self.colName)
        return label
        
                
    async def insert(self, label):
        result = await self.db.insert(label, self.colName)
        return result
        
    async def insert_user(self,id,user_id):
        condition = {'_id':ObjectId(id)}
        label = {'$addtoSet':{'userList':user_id}}
        await self.db.update(condition, label, self.colName)
        
    async def remove_user(self,id,user_id):
        condition = {'_id':ObjectId(id)}
        label = {'$pull':{'userList':user_id}}
        await self.db.update(condition, label, self.colName)  
    
    async def delete(self, label_id):
        condition = {'_id': label_id}
        await self.db.delete(condition, self.colName)

    def brief_label(self,label):
        brieflabel = self.db.brief_label(label)
        brieflabel['_id']=str(label['_id'])
        return brieflabel
