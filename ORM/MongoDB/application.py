# coding=utf-8
from ORM.MongoDB.base import MongoDB_orm_base,ObjectId
import pymongo
class Application(MongoDB_orm_base):
    def __init__(self, mongo_control):
        MongoDB_orm_base.__init__(self, mongo_control)
        self.colName = 'application' 

    def check_state(self, application):
        success = True
        result = None
        allowedType = ['masterApplication']
        allowedState = ['new', 'approved', 'denied']
        if 'type' in application and not application['type'] in allowedType:
            success = False
            result = "type Error. current type is " +  str(application['type']) + " The allowed type is " + str(allowedType)
            return (success, result)
        if 'state' in application and not application['state'] in allowedState:
            success = False
            result = "state Error. current state is " +  str(application['state']) + " The allowed state is " + str(allowedState)
            return (success, result)
        return (success, result)


        
    async def get_application_free(self, condition, sortby, sort, limit, skip):
        applicationlist = await self.db.get_document_list(condition, sortby, sort, limit, skip, self.colName)
        return applicationlist
        
    async def get_by_id(self, id):
        condition = {'_id':ObjectId(id)}
        application = await self.db.get_document_one(condition, self.colName)
        return application
            
    async def insert(self, application):
        (success, result) =  self.check_state(application)
        if success == False:
            return (success, result)
        result = await self.db.insert(application, self.colName)
        return (True, result)
        
    async def delete(self, application_id):
        condition = {'_id': application_id}
        await self.db.delete(condition, self.colName)
        
    async def update(self,id,application):
        (success, result) =  self.check_state(application)
        if success == False:
            return (success, result)
        condition = {'_id':ObjectId(id)}
        application = {'$set':application}
        await self.db.update({'_id':ObjectId(id)}, application, self.colName)
        return (True,'')

    def brief_application(self,application):
        briefapplication = self.db.brief_application(application)
        return briefapplication
