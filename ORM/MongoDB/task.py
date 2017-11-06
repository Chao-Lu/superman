# coding=utf-8
from ORM.MongoDB.base import MongoDB_orm_base,ObjectId
import pymongo
class Task(MongoDB_orm_base):
    def __init__(self, mongo_control):
        MongoDB_orm_base.__init__(self, mongo_control)
        self.colName = 'task'
        
    async def insert(self,task):
        result = await self.db.insert(task, self.colName)
        return result

    async def get_task_by_master_id(self,master_id):
        condition = {'master_id':str(master_id)}
        task = await self.db.get_document_one(condition, self.colName)
        return task

    async def update(self,master_id,task):
        condition = {'master_id':str(master_id)}
        task = {'$set':task}
        await self.db.update(condition, post, self.colName)

    def brief_task(self,task):
        brieftask = self.db.brief_task(task)
        return brieftask
