from handler.base import BaseHandler
import routes
import json
from handler.exceptions import ResourceNotExistError,PermissionDeniedError,ArgsError,StateError,RelateResError

class sMasterAllHandler(BaseHandler):        

    """
        @api {get} /v1.0/manager/master/all 获取达人列表
        @apiGroup manager
        @apiVersion  1.0.0
        @apiDescription 获取达人列表

        @apiPermission manager
        
        @apiParam    {string}    condition    
        @apiParam    {string}    sortby
        @apiParam    {string}    sort
        @apiParam    {string}    limit
        @apiParam    {string}    skip
        
        @apiSuccess    {Object}    masterlist    达人信息
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
        
        masterlist = await self.db.master.get_master_free(condition,sortby,sort,limit,skip)
        for i in range(0,len(masterlist)):
            master=masterlist[i]
            orderlist = await self.db.order.get_order_free({'master':str(master['userId'])},'_id','+',10000,0)
            number=0
            value=0
            for order in orderlist:
                if order['state']=='accpaid' or order['state']=='complete':
                    number=number+1
                    value=value+order['price']
            master['orderNum']=number
            master['orderValue']=value
            master['postNum']=len(await self.db.post.get_post_free({'publisher':str(master['userId'])},'_id','-',1000000,0))
            master['eventNum']=len(await self.db.event.get_event_free({'belongedMaster':master['userId']},'type','+',10000,0))
            user = await self.db.user.get_by_id(master['userId'])
            master['favorMeNum']=len(user['favorMeList'])
            if master['category'] != self.db.base.get_master_default()['category']:
                master['category']=await self.db.category.get_by_id(master['category'])
            masterlist[i] = master
        self.finish_success(result=masterlist)
        pass

class sMasterOneHandler(BaseHandler):    

    """
        @api {get} /v1.0/manager/master 获取达人信息
        @apiGroup manager
        @apiVersion  1.0.0
        @apiDescription 获取达人信息

        @apiPermission manager
        
        @apiParam    {string}    user_id    用户ID
        
        @apiSuccess    {Object}    master    达人信息
    """
    async def get(self):
        self.prehandle()
        user_info=await self.user_info

        if not self.is_manager(user_info['masterId']):
            raise PermissionDeniedError("需要管理员用户")
        user_id = self.get_argument('user_id',default=None)
        master = await self.db.master.get_by_user(user_id)
        eventlist=await self.db.event.get_event_free({'belongedMaster':user_id},'type','+',10000,0)
        master['orderNum']=0
        for i in range(0,len(eventlist)):
            event = eventlist[i]
            orderlist = await self.db.order.get_order_free({'belonged':str(event['_id'])},'_id','+',10000,0)
            number=0
            value=0
            for order in orderlist:
                if order['state']=='accpaid' or order['state']=='complete':
                    number=number+1
                    value=value+order['price']
            event['orderNum']=number
            master['orderNum']=master['orderNum']+number
            event['orderValue']=value
            eventlist[i]=event
        master['eventlist']=eventlist
        if master['category'] != self.db.base.get_master_default()['category']:
            master['category']=await self.db.category.get_by_id(master['category'])
        user = await self.db.user.get_by_id(user_id)
        master['userType']=user['userType']
        master['favorMeNum']=len(user['favorMeList'])
        master['postNum']=-1
        self.finish_success(result=master)
        pass
    """
        @api {put} /v1.0/manager/master 更改达人信息
        @apiGroup manager
        @apiVersion  1.0.0
        @apiDescription 更改达人信息

        @apiPermission manager
        
        @apiParam    {string}    user_id    用户ID
        @apiParam    {Object}    master    更改内容
        @apiSuccess    {string}    result "OK"

    """
    async def put(self):
        self.prehandle()
        user_info=await self.user_info
        if not self.is_manager(user_info['masterId']):
            raise PermissionDeniedError("需要管理员用户")
        json = self.json_body
        user_id = json['user_id']
        Old_master = await self.db.master.get_by_user(user_id)
        master = json['master']
        master_id = Old_master['_id'] 
        
        Old_master = self.db.base.dict_match(Old_master,
            {
            'state':'',
            'realName':'',
            'avatar':'',
            'coverPhoto':'',
            'location':'',
            'category':'',
            'realTitle':'',
            'masterLabel':[],
            'personalDetails':'',
            'entryDate':'',
            'masterPhoto':[],
            'phone':'',
        })
        New_master = self.db.base.dict_match(master,Old_master)
        await self.db.master.update(master_id,New_master)
        await self.db.user.update(user_id,
                {
                    'realName':master_info['realName'],
                    'avatar':master_info['avatar'],
                    'coverPhoto':master_info['coverPhoto'],
                })
        self.finish_success(result='OK')
        pass


    async def post(self):
        self.prehandle()
        user_info=await self.user_info
        if not self.is_manager(user_info['masterId']):
            raise PermissionDeniedError("需要管理员用户")
        json = self.json_body
        master = json['master']
        
        master_brife =             {
            'state':'',
            'realName':'',
            'avatar':'',
            'coverPhoto':'',
            'location':'',
            'category':'',
            'realTitle':'',
            'masterLabel':[],
            'personalDetails':'',
            'entryDate':'',
            'masterPhoto':[],
            'phone':'',
        }
        New_master = self.db.base.dict_match(master,master_brife)
        master_id = await self.db.master.insert(New_master)

        self.finish_success(result=master_id)
        

routes.handlers += [
    (r'/v1.0/manager/master/all', sMasterAllHandler),
    (r'/v1.0/manager/master', sMasterOneHandler),
]
