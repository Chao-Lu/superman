from handler.base import BaseHandler
import routes
import json
from handler.exceptions import ResourceNotExistError,PermissionDeniedError,ArgsError,StateError,RelateResError
class sUserAllHandler(BaseHandler):        

    """
        @api {get} /v1.0/manager/user/all 获取用户列表
        @apiGroup manager
        @apiVersion  1.0.0
        @apiDescription 获取用户列表

        @apiPermission manager
        
        @apiParam    {string}    condition    
        @apiParam    {string}    sortby
        @apiParam    {string}    sort
        @apiParam    {string}    limit
        @apiParam    {string}    skip
        
        @apiSuccess    {Object}    userlist    用户信息
    """
    async def get(self):
        self.prehandle()
        user_info=await self.user_info

        if not self.is_manager(user_info['masterId']):
            raise PermissionDeniedError("需要管理员用户")
        condition = json.loads(self.get_argument('condition',default='{}'))
        sortby = str(self.get_argument('sortby',default='_id'))
        sort = str(self.get_argument('sort',default='+'))
        limit = int(self.get_argument('limit',default=1000))
        skip = int(self.get_argument('skip',default=0))
        
        userlist = await self.db.user.get_user_free(condition,sortby,sort,limit,skip)

        self.finish_success(result=userlist)
        pass

class sUserOneHandler(BaseHandler):    

    """
        @api {get} /v1.0/manager/user 获取用户信息
        @apiGroup manager
        @apiVersion  1.0.0
        @apiDescription 获取用户信息

        @apiPermission manager
        
        @apiParam    {string}    user_id    
        
        @apiSuccess    {Object}    user    用户信息
    """
    async def get(self):
        self.prehandle()
        user_info=await self.user_info

        if not self.is_manager(user_info['masterId']):
            raise PermissionDeniedError("需要管理员用户")
        user_id = self.get_argument('user_id',default=None)
        user = await self.db.user.get_by_id(user_id)
        user['cardholder']= await self.db.cardholder.get_by_user(user_id)
        
        favormaster=user['userFavorMaster']
        for i in range(0,len(favormaster)):
            favormaster[i]=self.db.master.brief_master(await self.db.master.get_by_user(favormaster[i]))
        user['userFavorMaster']=favormaster
        self.finish_success(result=user)
        pass
    """
        @api {put} /v1.0/manager/user 更改用户信息
        @apiGroup manager
        @apiVersion  1.0.0
        @apiDescription 更改用户信息

        @apiPermission manager
        
        @apiParam    {string}    user_id    
        @apiParam    {Object}    user

        @apiSuccess    {string}    result "OK"
    """
    async def put(self):
        self.prehandle()
        user_info=await self.user_info

        if not self.is_manager(user_info['masterId']):
            raise PermissionDeniedError("需要管理员用户")
        json = self.json_body
        user_id = json['user_id']
        user = json['user']
        Old_user = self.db.base.dict_match(await self.db.user.get_by_id(user_id),
            {
                #'phoneNumber':'',
                'password':'',
                'weixinopenid':'',
                'realName':'',
                'avatar':'',
                'gender':'',
                'university':'',
                'campus':'',
                'realIdentity':'',
                #'masterId':'',
                #'userOrders':[],
                #'userBalance':[],
                #'userNotification':[]
            })
        New_user = self.db.base.dict_match(user,Old_user)
        await self.db.user.update(user_id,New_user)
        user=await self.db.user.get_by_id(user_id)
        if self.is_master(user['masterId']) == True:
            await self.db.master.update(user['masterId'],{'realName':user['realName'],'avatar':user['avatar']})
        self.finish_success(result='OK')
        pass
        
    
class sUserToMasterHandler(BaseHandler):    

    """
        @api {post} /v1.0/manager/user/toMaster 用户升级为达人

        @apiGroup manager
        @apiVersion  1.0.0
        @apiDescription 用户升级为达人

        @apiPermission manager
        
        @apiParam    {Object}    user_id    用户id
        @apiParam    {Object}    master    达人信息
        
        @apiSuccess    {string}    result "OK"
    """
    async def post(self):
        self.prehandle()
        user_info=await self.user_info
        #print(user_info)
        if not self.is_manager(user_info['masterId']):
            raise PermissionDeniedError("需要管理员用户")
            
        json=self.json_body
        user_id = json['user_id']
        user_info = await self.db.user.get_by_id(user_id)
        print(user_info)
        if self.is_master(user_info['masterId']):
            raise StateError("该用户已是达人")
        
        master_src ={} #json['master']
        master_src['userId']=user_id
        master_src['avatar']=user_info['avatar']
        master_src['realName']=user_info['realName']
        master_src['state']='new'
        master_src['entryDate']=self.get_timestamp()
        master_dst = self.db.base.dict_match(master_src,self.db.base.get_master_default())
        masterId = await self.db.master.insert(master_dst)
        await self.db.user.update(user_id,{'masterId':str(masterId)})
        '''
        touser_id=user_id
        notice = self.produce_notice("达人申请通过",touser_id,str(user_info['_id']),'2',
                        {    
                            'content':'恭喜您的达人申请已通过',
                        })
        
        notice_id = await self.db.notice.insert(notice)
        await self.db.noticeholder.insert_notice(touser_id,notice_id)
        '''
        self.finish_success(result="OK")


routes.handlers += [

    (r'/v1.0/manager/user/all', sUserAllHandler),
    (r'/v1.0/manager/user', sUserOneHandler),
    (r'/v1.0/manager/user/toMaster', sUserToMasterHandler),
    
]
