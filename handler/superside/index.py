from handler.base import BaseHandler
import routes
import json
from handler.exceptions import ResourceNotExistError,PermissionDeniedError,ArgsError,StateError,RelateResError
class sIndexAllHandler(BaseHandler):    

    """
        @api {get} /v1.0/manager/index/all 获取首页推荐列表
        @apiGroup manager
        @apiVersion  1.0.0
        @apiDescription 获取首页推荐列表

        @apiPermission manager
        
        @apiParam    {string}    condition    
        @apiParam    {string}    sortby
        @apiParam    {string}    sort
        @apiParam    {string}    limit
        @apiParam    {string}    skip
        
        @apiSuccess    {Object}    indexlist    首页推荐信息
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
        
        indexlist = await self.db.index.get_index_free(condition,sortby,sort,limit,skip)
        for i in range(0,len(indexlist)):
            index = indexlist[i]
            if index['type']=='master':
                index['content']=await self.db.master.get_by_user(index['contentId'])
            elif index['type']=='event':
                index['content']=await self.db.event.get_by_id(index['contentId'])
                index['content']['belongedMaster'] = await self.db.master.get_by_user(index['content']['belongedMaster'])
            indexlist[i]=index
        self.finish_success(result=indexlist)
        pass

class sIndexOneHandler(BaseHandler):    

    """
        @api {get} /v1.0/manager/index 获取首页推荐信息
        @apiGroup manager
        @apiVersion  1.0.0
        @apiDescription 获取首页推荐信息

        @apiPermission manager
        
        @apiParam    {string}    index_id    首页推荐ID
        
        @apiSuccess    {Object}    index    首页推荐信息
    """
    async def get(self):
        self.prehandle()
        user_info=await self.user_info

        if not self.is_manager(user_info['masterId']):
            raise PermissionDeniedError("需要管理员用户")
        index_id = self.get_argument('index_id',default=None)
        index = await self.db.index.get_by_id(index_id)
        self.finish_success(result=index)
        pass
    """
        @api {put} /v1.0/manager/index 更改首页推荐信息
        @apiGroup manager
        @apiVersion  1.0.0
        @apiDescription 更改首页推荐信息

        @apiPermission manager
        
        @apiParam    {string}    index_id    首页推荐ID
        @apiParam    {Object}    index    更改内容
        
        
        @apiSuccess    {string}    result "OK"
    """
    async def put(self):
        self.prehandle()
        user_info=await self.user_info

        if not self.is_manager(user_info['masterId']):
            raise PermissionDeniedError("需要管理员用户")
        json = self.json_body
        index_id = json['index_id']
        index = json['index']
        
        Old_index = self.db.base.dict_match(await self.db.index.get_by_id(index_id),
            {
                #'type':'',
                #'contentId':'',
                #'recommendDate':'',
                'state':'',
                'position':''
            })
        New_index = self.db.base.dict_match(index,Old_index)
        await self.db.index.update(index_id,New_index)

        self.finish_success(result='OK')
        pass
    """
        @api {delete} /v1.0/manager/index 删除首页推荐
        @apiGroup manager
        @apiVersion  1.0.0
        @apiDescription 删除首页推荐

        @apiPermission manager
        
        @apiParam    {string}    index_id    首页推荐ID
        
        @apiSuccess    {string}    result "OK"
    """
    async def delete(self):
        self.prehandle()
        user_info=await self.user_info

        if not self.is_manager(user_info['masterId']):
            raise PermissionDeniedError("需要管理员用户")
        json = self.json_body
        index_id = json['index_id']
        await self.remove_index(index_id)
        self.finish_success(result='OK')
        pass
        
    """
        @api {post} /v1.0/manager/index 上传首页推荐
        @apiGroup manager
        @apiVersion  1.0.0
        @apiDescription 上传首页推荐

        @apiPermission manager
        
        @apiParam    {Object}    index    首页推荐
        
        @apiSuccess    {string}    index_id 首页推荐ID
    """
    async def post(self):
        self.prehandle()
        user_info=await self.user_info

        if not self.is_manager(user_info['masterId']):
            raise PermissionDeniedError("需要管理员用户")
        json = self.json_body['index']

        if json['type'] == 'event':
            event = await self.db.event.get_by_id(json['contentId'])
            if event is None:
                raise RelateResError("事件不存在")
        elif json['type'] == 'master':
            master = await self.db.master.get_by_user(json['contentId'])
            if master is None:
                raise RelateResError("达人不存在")
        elif json['type'] == 'post':
            post = await self.db.post.get_by_id(json['contentId'])
            if post is None:
                raise RelateResError("动态不存在")
        index_src = json
        index_dst = self.db.base.dict_match(index_src,self.db.base.get_index_default())
        index_dst['recommendDate'] = self.get_timestamp()
        index_id = await self.db.index.insert(index_dst)

        self.finish_success(result=index_id)
        pass
        
class sBannerHandler(BaseHandler):
    """
        @api {get} /v1.0/manager/banner 获取轮播图列表
        @apiGroup manager
        @apiVersion  1.0.0
        @apiDescription 获取轮播图列表

        @apiPermission manager
        
        @apiParam    {string}    condition    
        @apiParam    {string}    sortby
        @apiParam    {string}    sort
        @apiParam    {string}    limit
        @apiParam    {string}    skip
        
        @apiSuccess    {Object}    bannerlist    轮播图列表
    """
    async def options(self):
        self.prehandle()
        self.finish()

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
        
        bannerlist = await self.db.banner.get_banner_free(condition,sortby,sort,limit,skip)
        for i in range(0,len(bannerlist)):
            if bannerlist[i]['type']== 'master':
                bannerlist[i]['content']=await self.db.master.get_by_user(bannerlist[i]['contentId'])
            if bannerlist[i]['type']== 'event':
                bannerlist[i]['content']=await self.db.event.get_by_id(bannerlist[i]['contentId'])
        self.finish_success(result=bannerlist)
        pass
        
    """
        @api {post} /v1.0/manager/banner 上传轮播图
        @apiGroup manager
        @apiVersion  1.0.0
        @apiDescription 上传轮播图

        @apiPermission manager
        
        @apiParam    {Object}    banner    轮播图
        
        @apiSuccess    {string}    banner_id 轮播图ID
    """
    async def post(self):
        self.prehandle()
        user_info=await self.user_info

        if not self.is_manager(user_info['masterId']):
            raise PermissionDeniedError("需要管理员用户")
        json = self.json_body
        banner_src=json['banner']
        banner_dst=self.db.base.dict_match(banner_src,self.db.base.get_banner_default())
        banner_dst['time']=self.get_timestamp()
        
        banner_id = await self.db.banner.insert(banner_dst)
        if banner_id is None:
            raise StateError("添加轮播图错误")
        self.finish_success(result=banner_id)
        pass
    """
        @api {put} /v1.0/manager/banner 更改轮播图信息
        @apiGroup manager
        @apiVersion  1.0.0
        @apiDescription 更改轮播图信息

        @apiPermission manager
        
        @apiParam    {string}    banner_id    轮播图ID
        @apiParam    {Object}    banner    更改内容
        
        
        @apiSuccess    {string}    result "OK"
    """
    async def put(self):
        self.prehandle()
        user_info=await self.user_info

        if not self.is_manager(user_info['masterId']):
            raise PermissionDeniedError("需要管理员用户")
        json = self.json_body
        banner_id = json['banner_id']
        banner = json['banner']
        
        Old_banner = self.db.base.dict_match(await self.db.banner.get_by_id(banner_id),
            {
                'state':'',            #轮播图状态  '0'/'1'/'2'   下架/上架/失效
                #'type':'',            #轮播图指向类型
                #'contentId':'',        #轮播图指向ID
                'content':'',        #轮播图说明
                #'image':'',            #轮播图图片
                #'time':''            #轮播图生成时间
                'position':'',
            })
        New_banner = self.db.base.dict_match(banner,Old_banner)
        await self.db.banner.update(banner_id,New_banner)

        self.finish_success(result='OK')
        
class LabelHandler(BaseHandler):
    async def get(self):
        user_info=await self.user_info
        labelMap = await self.db.label.get_labelMap()
        self.finish_success(result=labelMap)
routes.handlers += [
    (r'/v1.0/manager/index/all', sIndexAllHandler),
    (r'/v1.0/manager/index', sIndexOneHandler),
    (r'/v1.0/manager/banner', sBannerHandler),
    (r'/v1.0/manager/labelMap', LabelHandler),
]
