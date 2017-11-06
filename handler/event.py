from handler.base import BaseHandler
import routes
from handler.exceptions import ResourceNotExistError,PermissionDeniedError,ArgsError,StateError,RelateResError

class EventsIndexHandler(BaseHandler):
    """
        @api {get} /v1.0/event/index 获取所有事件列表
        @apiGroup event
        @apiVersion  1.0.0
        @apiDescription 获取事件列表

        @apiPermission user
        
        @apiParam    {string}    type    

        
        @apiSuccess    {Object}    eventlist    事件列表
    """
    async def get(self):
        user_info=await self.user_info
        typ = self.get_argument('type',default=None)
        sortby = '_id'
        sort = '+'
        limit = 1000
        skip = 0
        condition={}
        categorylist = await self.db.category.get_category_free(condition,sortby,sort,limit,skip)
        if typ == 'course':
            condition['type']='course'
        elif typ == 'activity':
            condition['type']='activity'
        elif typ == 'service':
            condition['type']='service'
        elif typ == 'appointment':
            condition['type']='appointment'
        else:
            raise ArgsError("type?")
        condition['$or']=[{'state':'on'},{'state':'onno'}]
        eventlist=[]
        for i in range(0,len(categorylist)):
            condition['category']=str(categorylist[i]['_id'])
            elist=await self.db.event.get_event_free(condition,sortby,sort,limit,skip)
            if len(elist) == 0:
                continue
            eventlist.append({'category':categorylist[i],'events':elist})

        self.finish_success(result=eventlist)
        pass






class EventHandler(BaseHandler):
    """
        @api {get} /v1.0/event 获取事件详情(用户)

        @apiGroup event
        @apiVersion  1.0.0
        @apiDescription 获取事件详情(用户)

        @apiPermission user
        
        @apiParam    {string}    event_id    事件ID
        
        @apiSuccess    {object}    event    事件详情
    """
    async def get(self):
        user_info=await self.user_info


        event_id=self.get_argument('event_id',default=None)
        
        event = await self.db.event.get_by_id(event_id)
        if event is None:
            raise ResourceNotExistError("事件不存在")
        if event['category'] !='':
            event['category'] = await self.db.category.get_by_id(event['category'])
        
        event['belongedMaster'] = self.db.master.brief_master(await self.db.master.get_by_user(event['belongedMaster']))
        event['briefMaster'] = event['belongedMaster']
        event['favorNum'] = len(event['likeUserList'])
        event['isFavor'] = str(user_info['_id']) in str(event['likeUserList'])
        event['appointmentNum'] = await self.db.order.get_event_orderlist_length(str(event['_id']))
        event['commentNum'] = await self.db.comment.get_comment_num({'postId':event_id,'state':'on'})
        commentList = await self.db.comment.get_comment_free({'postId':event_id,'state':'on'},'_id','-',event['commentNum'],0)
        star = [0.0,0.0,0.0]
        if event['commentNum'] != 0:
            for com in commentList:
                star = [ star[i] + com['star'][i] for i in range(0,3)]
            event['commentStar'] = [star[i]/event['commentNum'] for i in range(0,3)]
        else:
            event['commentStar'] = star
        tipList = await self.db.tip.get_tip_free({'to_event_id':event_id,'state':'accpaid'},'_id','-',20,0)
        tipImageList = []
        for tip in tipList:
            uinfo = await self.db.user.get_by_id(tip['from_user'])
            tipImageList.append(uinfo['avatar'])
        event['tipImageList'] = tipImageList
        tip_list = await self.db.tip.find_by_to_event_id(str(event['_id']))
        event['tipNum'] = len(tip_list)
        if 'likeUserList' in event:
            if str(user_info['_id']) in event['likeUserList']:
                event['isLike'] = 'Yes'
            else:
                event['isLike'] = 'No'
        else:
            pass
        self.finish_success(result=event)
        pass
    """
        @api {delete} /v1.0/event 删除约见事件
        @apiGroup manager
        @apiVersion  1.0.0
        @apiDescription 删除约见事件

        @apiPermission manager
        
        @apiParam    {string}    event_id    事件ID
        
        @apiSuccess    {string}    result "OK"
        @apiSuccess {string}    result "没有权限"
    """
    async def delete(self):
        self.prehandle()
        user_info=await self.user_info
        json = self.json_body
        event_id = json['event_id']
        event = await self.db.event.get_by_id(ObjectId(event_id))
        if ObjectId(user_info['_id']) == ObjectId(event['belongedMaster']):
            await self.remove_event(event_id)
            self.finish_success(result='OK')
        else:
            self.finish_success(result='没有权限')
    """
        @api {post} /v1.0/event 上传约见事件
        @apiGroup manager
        @apiVersion  1.0.0
        @apiDescription 上传约见事件

        @apiPermission manager
        
        @apiParam    {Object}    event    事件
        @apiParam    (event)        {string}    type            事件类型  'appoinment'
        @apiParam    (event)        {string}    state            事件状态  '0'/'1'/'2'  新创建/上架/下架
        @apiParam    (event)        {string}    category         事件类别
        @apiParam     (event)        {string}    coverPhoto        封面
        @apiParam     (event)        {string}    title            标题
        @apiParam    (event)        {string}    serviceLead        约见详情介绍
        @apiParam    (event)        {list}        photosDisplay    展示图片
        @apiParam     (event)        {string}    importantinfo    需知
        @apiParam     (event)        {int}        price            单价
        
        @apiSuccess    {string}    event_id 事件ID
    """
    async def post(self):
        user_info=await self.user_info

        if not self.is_master(user_info['masterId']):
            raise PermissionDeniedError("需要注册成为达人")
        else:
            json = self.json_body#belongedMaster
            event_src = json['event']
            event_dst = self.db.base.dict_match(event_src,self.db.base.get_event_default())
            event_dst['foundtime'] = self.get_timestamp()
            event_dst['lastChangeTime']=event_dst['foundtime']
            event_dst['belongedMaster']=str(user_info['_id'])
            event_id = await self.db.event.insert(event_dst)

            self.finish_success(result=event_id)
    """
        @api {put} /v1.0/event 修改约见事件
        @apiGroup manager
        @apiVersion  1.0.0
        @apiDescription 修改约见事件

        @apiPermission manager
        @apiParam    {string}    event_id    事件ID
        @apiParam    {Object}    event        事件
        @apiParam    (event)        {string}    state            事件状态  '0'/'1'/'2'  新创建/上架/下架
        @apiParam     (event)        {string}    coverPhoto        封面
        @apiParam     (event)        {string}    title            标题
        @apiParam    (event)        {string}    serviceLead        约见详情介绍
        @apiParam    (event)        {list}        photosDisplay        展示图片
        @apiParam     (event)        {string}    importantinfo        需知
        
        @apiSuccess    {string}    event_id 事件ID
    """
    async def put(self):
        user_info=await self.user_info

        if not self.is_master(user_info['masterId']):
            raise PermissionDeniedError("需要注册成为达人")
        else:
            json = self.json_body#belongedMaster
            event_src = json['event']
            event_id = json['event_id']
            event_default={
                'state':'',
                'coverPhoto':'',
                'title':'',
                'serviceLead':'',
                'photosDisplay':'',
                'importantinfo':''
            }
            event = await self.db.event.get_by_id(event_id)
            event_default= self.db.base.dict_match(event,event_default)
            event_dst = self.db.base.dict_match(event_src,event_default)
            await self.db.event.update(event_id,event_dst)

            self.finish_success(result=event_id)

'''
class EventFavorHandler(BaseHandler):
    """
        @api {get} /v1.0/event/favor 获取喜欢的事件

        @apiGroup event
        @apiVersion  1.0.0
        @apiDescription 获取喜欢的事件

        @apiPermission user
        
        @apiSuccess    {list}    eventlist
    """
    async def get(self):
        user_info=await self.user_info
        #eventholder = await self.db.eventholder.get_by_id(str(user_info['_id']))
        eventlist=[]
        for i in user_info['userFavorEvent']:
            event = self.db.event.brief_event(await self.db.event.get_by_id(i))
            event['briefMaster'] = self.db.master.brief_master(await self.db.master.get_by_user(event['belongedMaster']))
            if str(user_info['_id']) in event['likeUserList']:
                event['isLike'] = 'Yes'
            else:
                event['isLike'] = 'No'
            eventlist.append(event)
        
        self.finish_success(result=eventlist)
    """
        @api {post} /v1.0/event/favor 添加/取消喜欢的事件

        @apiGroup event
        @apiVersion  1.0.0
        @apiDescription 添加喜欢的事件

        @apiPermission user
        
        @apiParam    {string}    event_id    事件ID
        
        @apiSuccess    {string}    result 'OK'
    """
    async def post(self):
        user_info=await self.user_info
        event_id=self.get_argument('event_id',default=None)
        event = await self.db.event.get_by_id(event_id)
        if event is None:
            raise ResourceNotExistError("事件不存在")            
        else:
            if str(user_info['_id']) in event['likeUserList']:
                await self.db.eventholder.remove_like_event(user_info['_id'],event_id)
                await self.db.event.remove_like(event['_id'],user_info['_id'])
                await self.db.user.remove_favor_event(user_info['_id'],event_id)
                self.finish_success(result='unlike')
            else:
                await self.db.eventholder.insert_like_event(user_info['_id'],event_id)    
                await self.db.event.insert_like(event['_id'],user_info['_id'])
                await self.db.user.insert_favor_event(user_info['_id'],event_id)
                self.finish_success(result="like")
    """
        @api {delete} /v1.0/event/favor 去除喜欢的事件

        @apiGroup event
        @apiVersion  1.0.0
        @apiDescription 去除喜欢的事件

        @apiPermission user
        
        @apiParam    {string}    event_id    事件ID
        
        @apiSuccess    {string}    result 'OK'
    """
    async def delete(self):
        user_info=await self.user_info
        event_id=self.get_argument('event_id',default=None)
        event = await self.db.event.get_by_id(event_id)
        if event is None:
            raise ResourceNotExistError("事件不存在")            
        await self.db.eventholder.remove_like_event(user_info['_id'],event_id)    
        await self.db.event.remove_like(event['_id'],user_info['_id'])        
        self.finish_success(result="OK")
        
'''


routes.handlers += [
    (r'/v1.0/event', EventHandler),
    #(r'/v1.0/event/favor', EventFavorHandler),
    (r'/v1.0/event/index',EventsIndexHandler),
]
