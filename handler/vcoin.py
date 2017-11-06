# coding = utf-8
from handler.base import BaseHandler
import routes
from handler.exceptions import ResourceNotExistError,PermissionDeniedError,ArgsError,StateError,RelateResError
from handler.unit.unit import ObjectId 
import time

def isOneDay(time_a,time_b):
    timea = time.localtime(time_a)
    timeb = time.localtime(time_b)
    if(timea.tm_year==timeb.tm_year and \
        timea.tm_mon==timeb.tm_mon and \
        timea.tm_mday==timeb.tm_mday):
        return True
    else:
        return False

#timeb is the next day of timea
#int
def isNextDay(timea,timeb):
    oneday_seconds = 60*60*24
    timea_next_day = time.localtime(timea + oneday_seconds)
    timeb_tmp = time.localtime(timeb)
    if(timea_next_day.tm_year==timeb_tmp.tm_year and \
        timea_next_day.tm_mon==timeb_tmp.tm_mon and \
        timea_next_day.tm_mday==timeb_tmp.tm_mday):
        return True
    else:
        return False


class SignUpHandler(BaseHandler):
    """
        @api {get} /v1.0/vcoin/signup 获取签到天数
        @apiGroup vcoin
        @apiVersion  1.0.0
        @apiDescription 获取签到天数
        @apiPermission user
        
        @apiSuccess {Object} signUpObj
        @apiSuccess {int}    days           0/1/2/3/4/5/6/7  
        @apiSuccess {string} isTodaySignUp  'Yes'/'No'
        @apiSuccess {string} isAward        'Yes'/'No'
    """
    async def get(self):
        days = 0;
        user_info=await self.user_info
        user_id = user_info['_id']
        time_stamp_list = await self.db.user.get_signup_days(ObjectId(user_id))
        days = len(time_stamp_list)
        isTodaySignUp = ''
        if days == 0:
            user_info['isAward'] = 'No'
            await self.db.user.reset_award(user_info['_id'])
            isTodaySignUp = 'No'
        elif (days<7 and days>0):
            user_info['isAward'] = 'No'
            await self.db.user.reset_award(user_info['_id'])
            present_time = time.time()
            last_time = max(time_stamp_list)
            if(isOneDay(last_time,present_time)):
                isTodaySignUp = 'Yes'
            elif(isNextDay(last_time,present_time)):
                isTodaySignUp = 'No'
            #存在一天没签到
            else:
                await self.db.user.delete_signup(user_id)
                isTodaySignUp = 'No'
                days = 0
        elif days==7:
            present_time = time.time()
            last_time = max(time_stamp_list)
            if(isOneDay(last_time,present_time)):
                isTodaySignUp = 'Yes'
            elif(isNextDay(last_time,present_time)):
                user_info['isAward'] = 'No'
                await self.db.user.reset_award(user_info['_id'])
                await self.db.user.delete_signup(user_id)
                isTodaySignUp = 'No'
                days = 0
            else:
                user_info['isAward'] = 'No'
                await self.db.user.reset_award(user_info['_id'])
                await self.db.user.delete_signup(user_id)
                isTodaySignUp = 'No'
                days = 0
        else:
            user_info['isAward'] = 'No'
            await self.db.user.reset_award(user_info['_id'])
            await self.db.user.delete_signup(user_id)
            isTodaySignUp = 'No'
            days = 0

        signUpObj = {
            'isTodaySignUp':isTodaySignUp,
            'days':days,
            'isAward':user_info['isAward'],
        }
        self.finish_success(result=signUpObj)

    """
        @api {post} /v1.0/vcoin/signup 签到
        @apiGroup vcoin
        @apiVersion  1.0.0
        @apiDescription 签到
        @apiPermission user

        @apiParam   {int}   vcoin_number    签到获得虚拟币数量    
        
        @apiSuccess {String}    result    'OK'
        @apiErr     {String}    result    '今日已签到'/'其他'
    """
    async def post(self):
        user_info = await self.user_info
        vcoin_number = self.json_body['vcoin_number']
        time_stamp_list = await self.db.user.get_signup_days(ObjectId(user_info['_id']))
        days = len(time_stamp_list)
        print(days)
        present_time = time.time()
        if days==0:
            await self.db.user.record_signup(user_info['_id'],present_time)
            await self.db.user.add_vcoin_number(user_info['_id'],int(vcoin_number))
            self.finish_success(result='OK')
        elif (days<7 and days>0):
            last_time = max(time_stamp_list)
            if(isOneDay(last_time,present_time)):
                self.finish_err(result='今日已签到')
            elif(isNextDay(last_time,present_time)):
                await self.db.user.record_signup(user_info['_id'],present_time)
                await self.db.user.add_vcoin_number(user_info['_id'],int(vcoin_number))
                self.finish_success(result='OK')
            else:
                await self.db.user.delete_signup(user_info['_id'])
                await self.db.user.record_signup(user_info['_id'],present_time)
                await self.db.user.add_vcoin_number(user_info['_id'],int(vcoin_number))
                self.finish_success(result='OK')
        elif days == 7:
            last_time = max(time_stamp_list)
            if(isOneDay(last_time,present_time)):
                self.finish_err(result='今日已签到')
            else:
                await self.db.user.delete_signup(user_info['_id'])
                self.finish_err(result = '其他')
        else:
            await self.db.user.delete_signup(user_info['_id'])
            self.finish_err(result = '其他')


class VcoinHandler(BaseHandler):
    """
        @api {get} /v1.0/vcoin/getnumber 获取虚拟币个数
        @apiGroup vcoin
        @apiVersion  1.0.0
        @apiDescription 　获取虚拟币个数

        @apiPermission user
        
        @apiSuccess {int}    vcoin_number   虚拟币个数
    """
    async def get(self):
        user_info = await self.user_info
        vcoin_number = await self.db.user.get_vcoin_number(user_info['_id'])
        self.finish_success(result=vcoin_number)

    """
        @api {post} /v1.0/vcoin/postnumber 领取虚拟币个数
        @apiGroup vcoin
        @apiVersion  1.0.0
        @apiDescription 领取虚拟币,领取额外奖励
        
        @apiParam   {int}   vcoin_number    获得虚拟币数量    
        @apiParam   {string}award          表示是否为获取额外奖励 'Yes'/'No'
        
        @apiPermission user
    """
    async def post(self):
        user_info = await self.user_info
        vcoin_number = self.json_body['vcoin_number']
        await self.db.user.add_vcoin_number(user_info['_id'],int(vcoin_number))
        if self.json_body['award'] == 'Yes':
            await self.db.user.set_award(user_info['_id'])
        else:
            pass

class VcoinTaskHandler(BaseHandler):
    """
        @api {get} /v1.0/vcoin/task 查看可以领取虚拟币的任务
        @apiGroup vcoin
        @apiVersion  1.0.0
        @apiDescription 领取虚拟币,领取额外奖励
        
        @apiPermission user

        @apiSuccess {Object}    task   
        @apiSuccess (task)   　　　{string}    self_info           'undo'/'done'/'finish'
        @apiSuccess (task)      {string}    achievement         'undo'/'done'/'finish'
        @apiSuccess (task)      {string}    brief_introduction  'undo'/'done'/'finish'
        @apiSuccess (task)      {string}    display_photo       'undo'/'done'/'finish'
    """

    async def get(self):
        task = {
            'master_id':'',
            'self_info':'undo',
            'achievement':'undo',
            'brief_introduction':'undo',
            'display_photo':'undo',
        }
        user_info = await self.user_info
        master = await self.db.master.get_by_user(user_info['_id'])
        if master:
            task['master_id'] = str(master['_id'])
            if master['realTitle']!='':
                task['self_info'] = 'done'
            if master['masterLabel']!=[]:
                task['achievement'] = 'done'
            if master['masterPhoto'] !=[] or master['relatePhoto']!=[]:
                task['display_photo'] = 'done'
            if master['personalDetails'] != '':
                task['brief_introduction'] = 'done'

            
            old_task = await self.db.task.get_task_by_master_id(master['_id'])
            if old_task:
                task['self_info'] = old_task['self_info']
                task['achievement'] = old_task['achievement']
                task['brief_introduction'] = old_task['brief_introduction']
                task['display_photo'] = old_task['display_photo']
            else:
                await self.db.task.insert(task)
        else:
            pass
        self.finish_success(result = task)

    """
        @api {post} /v1.0/vcoin/task 领取虚拟币
        @apiGroup vcoin
        @apiVersion  1.0.0
        @apiDescription 领取虚拟币
        
        @apiPermission user
 
        @apiParam   {string}   task_type    'self_info'/'achievement'/'brief_introduction'/'display_photo'
        @apiParam   {string}   vcoin_number 增加虚拟币个数

        @apiSuccess {string}    result      '领取金币成功'/'无法领取金币'
    """
    async def post(BaseHandler):
        user_info = await self.user_info
        master = self.db.master.get_by_user(user_info['_id'])
        if master:
            task = await self.db.task.get_task_by_master_id(master['_id'])
            if task:
                jsonObj = self.json_body
                if task[jsonObj['task_type']] == 'done':
                    await self.db.user.add_vcoin_number(user_info['_id'],jsonObj['vcoin_number'])
                    await self.db.task.update(master['_id'],{jsonObj['task_type']:'finish'})
                    self.finish_success(result='领取金币成功')
                else:
                    self.finish_success(result='无法领取金币')
            else:
                self.finish_success(result='无法领取金币')
        else:
            self.finish_err(result='无法领取金币')

routes.handlers += [
    (r'/v1.0/vcoin/signup',SignUpHandler),
    (r'/v1.0/vcoin/getnumber',VcoinHandler),
    (r'/v1.0/vcoin/postnumber',VcoinHandler),
    (r'/v1.0/vcoin/task',VcoinTaskHandler),
]


