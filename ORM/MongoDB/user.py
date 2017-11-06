# coding=utf-8
from ORM.MongoDB.base import MongoDB_orm_base,ObjectId
import    operator
import pymongo
import config
class User(MongoDB_orm_base):
    def __init__(self, mongo_control):
        MongoDB_orm_base.__init__(self, mongo_control)
        self.colName = 'user'
        
    async def delete(self,user_id):
        condition = {'user_id': user_id}
        await self.db.delete(condition, self.colName)
        
    async def get_user_free(self,condition,sortby,sort,limit,skip):
        userlist = await self.db.get_document_list(condition, sortby, sort, limit, skip, self.colName)
        for i in range(len(userlist)):
            userlist[i] = self.brief_user(userlist[i])
        return userlist
        
    async def get_by_id(self, id):
        condition = {'_id':ObjectId(id)}
        user = await self.db.get_document_one(condition, self.colName)
        return user
    
    async def get_by_openid(self, id):
        condition = {'weixinopenid':id}
        user = await self.db.get_document_one(condition, self.colName)
        return user

    async def get_manager_user(self):
        condition = {'masterId':config.MANAGER_ID}
        user = await self.db.get_document_one(condition, self.colName)
        return user
            
    async def get_by_phone(self, phone):
        condition = {'phoneNumber':phone}
        user = await self.db.get_document_one(condition, self.colName)
        return user
        
    async def insert(self, user):
        result = await self.db.insert(user, self.colName)
        return result
    
    async def insert_notice_flag(self,user_id):
        condition = {'_id':ObjectId(user_id)}
        user = {'$set':{'noticeFlag':'1'}}
        await self.db.update(condition, user, self.colName)
        
    async def remove_notice_flag(self,user_id):
        condition = {'_id':ObjectId(user_id)}
        user = {'$set':{'noticeFlag':'0'}}
        await self.db.update(condition, user, self.colName)
        
    async def update(self,user_id,user):
        condition = {'_id':ObjectId(user_id)}
        user = {'$set':user}
        await self.db.update(condition, user, self.colName)
        
    async def update_all(self,con,user):
        condition = con
        user = {'$set':user}
        await self.db.update(condition, user, self.colName)
        
    async def insert_favor_master(self,user_id,master_id):
        condition = {'_id':ObjectId(user_id)}
        user = {'$addToSet':{'userFavorMaster':master_id}}
        await self.db.update(condition, user, self.colName)

    async def remove_favor_master(self,user_id,master_id):
        condition = {'_id':ObjectId(user_id)}
        user = {'$pull':{'userFavorMaster':master_id}}
        await self.db.update(condition, user, self.colName)

    async def insert_favor_event(self,user_id,event_id):
        condition = {'_id':ObjectId(user_id)}
        user = {'$addToSet':{'userFavorEvent':str(event_id)}}
        await self.db.update(condition, user, self.colName)

    async def remove_favor_event(self,user_id,event_id):
        condition = {'_id':ObjectId(user_id)}
        user = {'$pull':{'userFavorEvent':str(event_id)}}
        await self.db.update(condition, user, self.colName)
    
    async def insert_favor_team(self,user_id,team_id):
        condition = {'_id':ObjectId(user_id)}
        user = {'$addToSet':{'userFavorTeam':team_id}}
        await self.db.update(condition, user, self.colName)

    async def remove_favor_team(self,user_id,team_id):
        condition = {'_id':ObjectId(user_id)}
        user = {'$pull':{'userFavorTeam':team_id}}
        await self.db.update(condition, user, self.colName)
    
    async def insert_favorMe(self,user_id,id):
        condition = {'_id':ObjectId(user_id)}
        user = {'$addToSet':{'favorMeList':id}}
        await self.db.update(condition, user, self.colName)

    async def remove_favorMe(self,user_id,id):
        condition = {'_id':ObjectId(user_id)}
        user = {'$pull':{'favorMeList':id}}
        await self.db.update(condition, user, self.colName)
        
    def brief_user(self,user):
        briefuser = self.db.brief_user(user)
        briefuser['favorMeNum']=len(user['favorMeList'])
        return briefuser

    async def update_phone(self,user_id,phoneNumber):
        condition = {'_id':ObjectId(user_id)}
        user = {'$set':{'phoneNumber':phoneNumber}}
        await self.db.update(condition, user, self.colName)

    #设置用户初始的虚拟币
    async def insert_vcoin_number(self,user_id,vcoin_number):
        condition = {'_id':ObjectId(user_id)}
        user = {'$set':{'vcoin':int(vcoin_number)}}
        await self.db.update(condition, user, self.colName)
        
    #获取虚拟币数量
    async def get_vcoin_number(self,user_id):
        condition = {'_id':ObjectId(user_id)}
        user = await self.db.get_document_one(condition)
        if 'vcoin' in user:
            return user['vcoin']
        else:
            return -1
            
    #增加虚拟币
    async def add_vcoin_number(self,user_id,vcoin_number):
        condition = {'_id':ObjectId(user_id)}
        user = {'$inc':{'vcoin':int(vcoin_number)}}
        await self.db.update(condition, user, self.colName)
        
    #减少虚拟币
    async def reduce_vcoin_number(self,user_id,vcoin_number):
        condition = {'_id':ObjectId(user_id)}
        user = {'$inc':{'vcoin':(-int(vcoin_number))}}
        await self.db.update(condition, user, self.colName)
        
    #获取累计签到天数
    async def get_signup_days(self,user_id):
        condition = {'_id':ObjectId(user_id)}
        user = await self.db.get_document_one(condition)
        if 'signup_days' in user:
            return user['signup_days']
        else:
            return []
            
    #清空签到记录
    async def delete_signup(self,user_id):
        condition = {'_id':ObjectId(user_id)}
        user = {'$set':{'signup_days':[]}}
        await self.db.update(condition, user, self.colName)
        
    #签到记录
    async def record_signup(self,user_id,time_stamp):
        condition = {'_id':ObjectId(user_id)}
        user = {'$push':{'signup_days':time_stamp}}
        await self.db.update(condition, user, self.colName)
        
    async def set_award(self,user_id):
        condition = {'_id':ObjectId(user_id)}
        user = {'$set':{'isAward':'Yes'}}
        await self.db.update(condition, user, self.colName)
        
    async def reset_award(self,user_id):
        condition = {'_id':ObjectId(user_id)}
        user = {'$set':{'isAward':'No'}}
        await self.db.update(condition, user, self.colName)
        
    async def insert_order(self,user_id,order_id):
        condition = {'_id':ObjectId(user_id)}
        user = {'$addToSet':{'userOrders':order_id}}
        await self.db.update(condition, user, self.colName)
