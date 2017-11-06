from handler.base import BaseHandler
import routes
import json
from handler.exceptions import ResourceNotExistError,PermissionDeniedError,ArgsError,StateError,RelateResError
class sCircleAllHandler(BaseHandler):    

    """
        @api {get} /v1.0/manager/circle/all 获取圈子列表
        @apiGroup manager
        @apiVersion  1.0.0
        @apiDescription 获取圈子列表

        @apiPermission manager
        
        @apiParam    {string}    condition    
        @apiParam    {string}    sortby
        @apiParam    {string}    sort
        @apiParam    {string}    limit
        @apiParam    {string}    skip
        
        @apiSuccess    {Object}    circlelist    圈子信息
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
        
        circlelist = await self.db.circle.get_circle_free(condition,sortby,sort,limit,skip)
        circlelist = await self.db.circle.get_circle_free(condition,'_id','-',1000,0)
        '''for i in range(0,len(circlelist)):
            circlelist[i]={
                'avatar':circlelist[i]['avatar'],
                'title':circlelist[i]['title'],
            }'''
        self.finish_success(result=circlelist)
        pass

class sCircleOneHandler(BaseHandler):    

    """
        @api {get} /v1.0/manager/circle 获取圈子信息
        @apiGroup manager
        @apiVersion  1.0.0
        @apiDescription 获取圈子信息

        @apiPermission manager
        
        @apiParam    {string}    event_id    圈子ID
        
        @apiSuccess    {Object}    event    圈子信息
    """
    async def get(self):
        self.prehandle()
        user_info=await self.user_info

        if not self.is_manager(user_info['masterId']):
            raise PermissionDeniedError("需要管理员用户")
        circle_id=self.get_argument('circle_id',default=None)
        print(circle_id)
        circle = await self.db.circle.get_by_id(circle_id)
        circle={
            'avatar':circle['avatar'],
            'title':circle['title'],
            'postNum':len(circle['postList']),
            'seeNum':circle['seeNum'],
            'circleInfo':circle['circleInfo'],
            'specialPostNum':len(circle['specialPost']),
            #'topPost':[],
            'circleManager':str(user_info['_id']) in circle['circleManager'],
            'state':circle['state'],
            'location':'',
        }
        self.finish_success(result=circle)
        pass
    """
        @api {put} /v1.0/manager/circle 更改圈子信息
        @apiGroup manager
        @apiVersion  1.0.0
        @apiDescription 更改圈子信息

        @apiPermission manager
        
        @apiParam    {string}    circle_id    圈子ID
        @apiParam    {Object}    circle    更改内容
        
        
        @apiSuccess    {string}    result "OK"
    """
    async def put(self):
        self.prehandle()
        user_info=await self.user_info

        if not self.is_manager(user_info['masterId']):
            raise PermissionDeniedError("需要管理员用户")
        json = self.json_body
        circle_id = json['circle_id']
        circle = json['circle']
        
        Old_circle = self.db.base.dict_match(await self.db.circle.get_by_id(circle_id),
            {
                'avatar':'',
                'title':'',
                'seeNum':0,
                'circleInfo':'',
                'specialPost':[],
                'topPost':[],
                'circleManager':[],
                'state':'off',
                'modeList':[],
                'activityList':[],
                'location':'',
            })
        New_circle = self.db.base.dict_match(circle,Old_circle)

        await self.db.circle.update(circle_id,New_circle)

        self.finish_success(result='OK')
        pass
    """
        @api {delete} /v1.0/manager/circle 删除圈子
        @apiGroup manager
        @apiVersion  1.0.0
        @apiDescription 删除圈子

        @apiPermission manager
        
        @apiParam    {string}    circle_id    圈子ID
        
        @apiSuccess    {string}    result "OK"
    """
    async def delete(self):
        self.prehandle()
        user_info=await self.user_info
        '''
        if not self.is_manager(user_info['masterId']):
            raise PermissionDeniedError("需要管理员用户")
        json = self.json_body
        event_id = json['event_id']
        await self.remove_event(event_id)
        self.finish_success(result='OK')
        pass
        '''
        
    """
        @api {post} /v1.0/manager/circle 上传圈子
        @apiGroup manager
        @apiVersion  1.0.0
        @apiDescription 上传圈子

        @apiPermission manager
        
        @apiParam    {string}    circle    圈子
        
        @apiSuccess    {string}    circle_id 圈子ID
    """
    async def post(self):
        print("post new")
        self.prehandle()
        user_info=await self.user_info

        if not self.is_manager(user_info['masterId']):
            raise PermissionDeniedError("需要管理员用户")
        json = self.json_body
        circle_src ={
                'circleManager':json['circle']['circleManager'],
                'entryDate':self.get_timestamp(),
                'avatar':json['circle']['avatar'],
                'title':json['circle']['title'],
                'circleInfo':json['circle']['circleInfo'],
                'state':json['circle']['state'],
                'location':json['circle']['location'],
                'type':json['circle']['type'],
                'position':json['circle']['position'],
                'moreInfo':json['circle']['moreInfo'],
            }
        circle_dst = self.db.base.dict_match(circle_src,self.db.base.get_circle_default())

        circle_id = await self.db.circle.insert(circle_dst)
        
        #uclass=self.db.base.get_uclass_default()
        #uclass['eventId']=event_id
        #uclass_id=await self.db.uclass.insert(uclass)
        #TODO MANY MANY MANY !!!!

        self.finish_success(result=circle_id)
        pass
routes.handlers += [
    (r'/v1.0/manager/circle/all', sCircleAllHandler),
    (r'/v1.0/manager/circle', sCircleOneHandler),
]
