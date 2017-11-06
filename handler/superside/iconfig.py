from handler.base import BaseHandler
import routes
import json
import time
from handler.exceptions import ResourceNotExistError,PermissionDeniedError,ArgsError,StateError,RelateResError
class iConfigHandler(BaseHandler):        

    """
        @api {get} /v1.0/manager/iconfig/all 获取所有设置
        @apiGroup manager
        @apiVersion  1.0.0
        @apiDescription 获取所有设置

        @apiPermission manager
        
        @apiParam    {string}    condition    
        @apiParam    {string}    sortby
        @apiParam    {string}    sort
        @apiParam    {string}    limit
        @apiParam    {string}    skip
        
        @apiSuccess    {Object}    iconfiglist    用户信息
    """
    async def post(self):
        self.prehandle()
        user_info=await self.user_info

        if not self.is_manager(user_info['masterId']):
            raise PermissionDeniedError("需要管理员用户")
        condition = json.loads(self.get_argument('condition',default='{}'))
        sortby = str(self.get_argument('sortby',default='_id'))
        sort = str(self.get_argument('sort',default='+'))
        limit = int(self.get_argument('limit',default=1000))
        skip = int(self.get_argument('skip',default=0))
        
        iconfiglist = await self.db.iconfig.get_iconfig_free(condition,sortby,sort,limit,skip)

        self.finish_success(result=iconfiglist)
        pass

    """
        @api {post} /v1.0/manager/iconfig/all 更新所有设置
        @apiGroup manager
        @apiVersion  1.0.0
        @apiDescription 更新所有设置

        @apiPermission manager
        
        @apiSuccess    {Object}    iconfiglist    用户信息
    """
    async def get(self):
        self.prehandle()
        #user_info=await self.user_info
        #if not self.is_manager(user_info['masterId']):
        #    raise PermissionDeniedError("需要管理员用户")
        userList = await self.db.user.get_user_free({},'_id','+',10000000,0)
        for user in userList:
            if user['campus']!='' and user['university']=='':
                c=user['campus']
                cl=c.split(')')
                cl=cl[0].split('(')
                u_m={
                    'campus':cl[1],
                    'university':cl[0],
                }
                await self.db.user.update(user['_id'],u_m)
        
        
        #动态管理员权限
        '''
        iconfiglist = await self.db.iconfig.get_iconfig_free({'title':'superviselist'},'_id','+',10,0)
        if len(iconfiglist)==0:
            iconfig=self.db.base.get_iconfig_default()
            iconfig={
                'title':'superviselist',
                'content':{
                    'superviselist':[
                            {'userId':'58b235a590c490226143636d','setTime':1,'rightLevel':1},
{'userId':'58b1875a90c490226160633f','setTime':1,'rightLevel':1},                            {'userId':'58cfc11290c4904644f315e4','setTime':1,'rightLevel':1},
                        #{'userId':'','setTime':'','rightLevel':''},
                        ]
                }    
            }
            await self.db.iconfig.insert(iconfig)
        #后台管理员权限
        iconfiglist = await self.db.iconfig.get_iconfig_free({'title':'managelist'},'_id','+',10,0)
        if len(iconfiglist)==0:
            iconfig=self.db.base.get_iconfig_default()
            iconfig={
                'title':'managelist',
                'content':{
                    'managelist':[#{'userId':'','setTime':'','rightLevel':''},
                        ]
                }    
            }
            await self.db.iconfig.insert(iconfig)
        await self.db.noticeholder.update_all({},{'handled':[]})
        masterlist = await self.db.master.get_master_free({'entryDate':{'$lt':time.mktime(time.strptime('2017-02-26 01:00:00','%Y-%m-%d %H:%M:%S'))}},'_id','+',100,0)
        for master in masterlist:
            await self.db.user.update(master['userId'],{'weixinopenid':''})
        await self.db.user.update_all({},{'isNew':'YES'})
        '''
        '''
        masters=[
            {'phone':'15651913995','userId':'58b18d1690c4902261606367'},
            {'phone':'15051832727','userId':'58b18d1990c490226160636b'},
            {'phone':'15651802085','userId':'58b18d1c90c490226160636f'},
            {'phone':'15651729213','userId':'58b18d2190c490226160637b'},
            {'phone':'15851838568','userId':'58b18d2290c490226160637f'},
            {'phone':'18061792535','userId':'58b1ae9490c4902261436329'},
            {'phone':'15150690014','userId':'58b1ae9490c4902261436335'},
            {'phone':'18016406812','userId':'58b1ae9590c490226143633d'},
            {'phone':'18795889123','userId':'58b1ae9490c4902261436339'},
            {'phone':'15850608757','userId':'58b18cec90c4902261606353'},
        ]
        for master in masters:
            user=await self.db.user.get_by_phone(master['phone'])
            olduser=await self.db.user.get_by_id(master['userId'])
            user['masterId']=olduser['masterId']
            user.pop('_id')
            await self.db.user.update(master['userId'],user)
            break;
        '''
class iSuperviseHandler(BaseHandler):    

    """
        @api {get} /v1.0/manager/supersize 获取动态管理员列表
        @apiGroup manager
        @apiVersion  1.0.0
        @apiDescription 获取动态管理员列表

        @apiPermission manager
        
        
        @apiSuccess    {Object}    supersizelist    动态管理员列表
    """
    async def get(self):
        self.prehandle()
        user_info=await self.user_info

        if not self.is_manager(user_info['masterId']):
            raise PermissionDeniedError("需要管理员用户")
            
        iconfig=await self.db.iconfig.get_by_title('superviselist')
        superviselist=[]
        for i in iconfig['content']['superviselist']:
            user = await self.db.user.get_by_id(i['userId'])
            supervise={
                'user':{
                    'realName':user['realName'],
                    'avatar':user['avatar'],
                    'phoneNumber':user['phoneNumber'],
                    'isMaster':self.is_master(user['masterId']),
                },
                'rightLevel':i['rightLevel'],
                'setTime':i['setTime'],
            }
            superviselist.append(supervise)
        self.finish_success(result=superviselist)
        pass
    """
        @api {post} /v1.0/manager/supersize 添加动态管理员
        @apiGroup manager
        @apiVersion  1.0.0
        @apiDescription 添加动态管理员

        @apiPermission manager
        
        @apiParam    {string}    user_id    
        @apiParam    {string}    rightLevel

        @apiSuccess    {string}    result "OK"
    """
    async def put(self):
        self.prehandle()
        user_info=await self.user_info

        if not self.is_manager(user_info['masterId']):
            raise PermissionDeniedError("需要管理员用户")
        json = self.json_body
        user_id = json['user_id']
        rightLevel = json['rightLevel']
        iconfig=await self.db.iconfig.get_by_title('superviselist')
        content=iconfig['content']
        for i in content['superviselist']:
            if i['userId'] == user_id:
                raise ResourceNotExistError("已是动态管理员")
        content['superviselist'].append({
            'userId':user_id,
            'rightLevel':rightLevel,
            'setTime':self.get_timestamp()
        })
        await self.db.iconfig.update(iconfig['_id'],{'content':content})
        self.finish_success(result='OK')
        pass


routes.handlers += [
    (r'/v1.0/manager/iconfig/all', iConfigHandler),
    (r'/v1.0/manager/supersize', iSuperviseHandler),
]
