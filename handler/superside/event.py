from handler.base import BaseHandler
import routes
import json
from handler.exceptions import ResourceNotExistError,PermissionDeniedError,ArgsError,StateError,RelateResError
class sEventAllHandler(BaseHandler):    

    """
        @api {get} /v1.0/manager/event/all 获取事件列表
        @apiGroup manager
        @apiVersion  1.0.0
        @apiDescription 获取事件列表

        @apiPermission manager
        
        @apiParam    {string}    condition    
        @apiParam    {string}    sortby
        @apiParam    {string}    sort
        @apiParam    {string}    limit
        @apiParam    {string}    skip
        
        @apiSuccess    {List}    eventlist    事件信息
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
        
        eventlist = await self.db.event.get_event_free(condition,sortby,sort,limit,skip)
        for i in range(0,len(eventlist)):
            event = eventlist[i]
            event['belongedMaster'] = self.db.master.brief_master(await self.db.master.get_by_user(event['belongedMaster']))
            orderlist = await self.db.order.get_order_free({'belonged':str(event['_id'])},'_id','+',10000,0)
            number=0
            value=0
            for order in orderlist:
                if order['state']=='accpaid' or order['state']=='complete':
                    number=number+1
                    value=value+order['price']
            event['orderNum']=number
            event['orderValue']=value
            if event['category'] != self.db.base.get_event_default()['category']:
                event['category']=await self.db.category.get_by_id(event['category'])

            eventlist[i] = event
        self.finish_success(result=eventlist)
        pass

class sEventOneHandler(BaseHandler):    

    """
        @api {get} /v1.0/manager/event 获取事件信息
        @apiGroup manager
        @apiVersion  1.0.0
        @apiDescription 获取事件信息

        @apiPermission manager
        
        @apiParam    {string}    event_id    事件ID
        
        @apiSuccess    {Object}    event    事件信息
    """
    async def get(self):
        self.prehandle()
        user_info=await self.user_info

        if not self.is_manager(user_info['masterId']):
            raise PermissionDeniedError("需要管理员用户")
        event_id = self.get_argument('event_id',default=None)
        event = await self.db.event.get_by_id(event_id)
        #event['uclass'] = await self.db.uclass.get_by_event(event_id)
        event['belongedMaster'] = self.db.master.brief_master(await self.db.master.get_by_user(event['belongedMaster']))
        orderlist = await self.db.order.get_order_free({'belonged':str(event['_id'])},'_id','+',10000,0)
        number=0
        value=0
        for order in orderlist:
            if order['state']=='accpaid' or order['state']=='complete':
                number=number+1
                value=value+order['price']
        event['orderNum']=number
        event['orderValue']=value
        if event['category'] != self.db.base.get_event_default()['category']:
            event['category']=await self.db.category.get_by_id(event['category'])
        self.finish_success(result=event)
        pass
    """
        @api {put} /v1.0/manager/event 更改事件信息
        @apiGroup manager
        @apiVersion  1.0.0
        @apiDescription 更改事件信息

        @apiPermission manager
        
        @apiParam    {string}    event_id    事件ID
        @apiParam    {Object}    event    更改内容
        
        
        @apiSuccess    {string}    result "OK"
    """
    async def put(self):
        self.prehandle()
        user_info=await self.user_info

        if not self.is_manager(user_info['masterId']):
            raise PermissionDeniedError("需要管理员用户")
        json = self.json_body
        event_id = json['event_id']
        event = json['event']
        
        Old_event = self.db.base.dict_match(await self.db.event.get_by_id(event_id),
            {
                'type':'',            #事件类型 'course'/'activity'/'service'
                'state':'0',        #事件状态  '0'/'1'/'2'  新创建/上架/下架
                'category':'',        #事件类别
                'slogan':'',        #事件一句话介绍
                'title':'',        #事件名称
                'serviceLead':'',    #服务介绍
                'importantinfo':'',#必要信息
                'coverPhoto':'',    #封面
                'photosDisplay':[],#顶部图片
                'extendedPhotos':[],#学员展示图片
                'price':'',            #事件价格
                'plan':'',            #训练计划
                'eventLead':'',
                'goalsText':'',
                'unitName':'',
            })
        New_event = self.db.base.dict_match(event,Old_event)
        New_event['lastChangeTime']=self.get_timestamp()
        await self.db.event.update(event_id,New_event)

        self.finish_success(result='OK')
        pass
    """
        @api {delete} /v1.0/manager/event 删除事件
        @apiGroup manager
        @apiVersion  1.0.0
        @apiDescription 删除事件

        @apiPermission manager
        
        @apiParam    {string}    event_id    事件ID
        
        @apiSuccess    {string}    result "OK"
    """
    async def delete(self):
        self.prehandle()
        user_info=await self.user_info

        if not self.is_manager(user_info['masterId']):
            raise PermissionDeniedError("需要管理员用户")
        json = self.json_body
        event_id = json['event_id']
        await self.remove_event(event_id)
        self.finish_success(result='OK')
        pass
        
    """
        @api {post} /v1.0/manager/event 上传事件
        @apiGroup manager
        @apiVersion  1.0.0
        @apiDescription 上传事件

        @apiPermission manager
        
        @apiParam    {Object}    event    事件
        
        @apiSuccess    {string}    event_id 事件ID
    """
    async def post(self):
        print("post new")
        self.prehandle()
        user_info=await self.user_info

        if not self.is_manager(user_info['masterId']):
            raise PermissionDeniedError("需要管理员用户")
        json = self.json_body
        event_src = json['event']
        event_dst = self.db.base.dict_match(event_src,self.db.base.get_event_default())
        event_dst['foundtime'] = self.get_timestamp()
        event_dst['lastChangeTime']=event_dst['foundtime']
        event_id = await self.db.event.insert(event_dst)
        
        #uclass=self.db.base.get_uclass_default()
        #uclass['eventId']=event_id
        #uclass_id=await self.db.uclass.insert(uclass)
        #TODO MANY MANY MANY !!!!

        self.finish_success(result=event_id)
        pass
routes.handlers += [
    (r'/v1.0/manager/event/all', sEventAllHandler),
    (r'/v1.0/manager/event', sEventOneHandler),
]
