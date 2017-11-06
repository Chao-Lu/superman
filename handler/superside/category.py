from handler.base import BaseHandler
import routes
import json
from handler.exceptions import ResourceNotExistError,PermissionDeniedError,ArgsError,StateError,RelateResError
class sCategoryAllHandler(BaseHandler):    

    """
        @api {get} /v1.0/manager/category/all 获取类别列表
        @apiGroup manager
        @apiVersion  1.0.0
        @apiDescription 获取类别列表

        @apiPermission manager
        
        @apiParam    {string}    condition    
        @apiParam    {string}    sortby
        @apiParam    {string}    sort
        @apiParam    {string}    limit
        @apiParam    {string}    skip
        
        @apiSuccess    {list}    categorylist    类别信息
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
        
        categorylist = await self.db.category.get_category_free(condition,sortby,sort,limit,skip)

        self.finish_success(result=categorylist)
        pass

class sCategoryOneHandler(BaseHandler):    

    """
        @api {post} /v1.0/manager/category 上传类别
        @apiGroup manager
        @apiVersion  1.0.0
        @apiDescription 上传类别

        @apiPermission manager
        
        @apiParam    {Object}    category    类别内容
        
        
        @apiSuccess    {string}    category_id 类别Id
    """
    async def post(self):
        self.prehandle()
        user_info=await self.user_info

        if not self.is_manager(user_info['masterId']):
            raise PermissionDeniedError("需要管理员用户")
        json = self.json_body
        category_src = json['category']
        category_dst = self.db.base.dict_match(category_src,self.db.base.get_category_default())
        #print(category_dst)
        category_dst['foundtime']=self.get_timestamp()
        category_id = await self.db.category.insert(category_dst)

        self.finish_success(result=category_id)
        pass
    """
        @api {put} /v1.0/manager/category 更改类别信息
        @apiGroup manager
        @apiVersion  1.0.0
        @apiDescription 更改类别信息

        @apiPermission manager
        
        @apiParam    {string}    category_id    类别ID
        @apiParam    {Object}    category    更改内容
        
        
        @apiSuccess    {string}    result "OK"
    """
    async def put(self):
        self.prehandle()
        user_info=await self.user_info

        if not self.is_manager(user_info['masterId']):
            raise PermissionDeniedError("需要管理员用户")
        json = self.json_body
        category_id = json['category_id']
        category = json['category']
        
        Old_category = self.db.base.dict_match(await self.db.category.get_by_id(category_id),
            {
                'title':'',
                'father':'',
                #'foundtime':'',
            })
        New_category = self.db.base.dict_match(category,Old_category)
        await self.db.category.update(category_id,New_category)

        self.finish_success(result='OK')
        pass
    """
        @api {delete} /v1.0/manager/category 删除类别
        @apiGroup manager
        @apiVersion  1.0.0
        @apiDescription 删除类别

        @apiPermission manager
        
        @apiParam    {string}    category_id    类别ID
        
        @apiSuccess    {string}    result "OK"
    """
    async def delete(self):
        self.prehandle()
        user_info=await self.user_info

        if not self.is_manager(user_info['masterId']):
            raise PermissionDeniedError("需要管理员用户")
        json = self.json_body
        category_id = json['category_id']
        await self.remove_category(category_id)
        self.finish_success(result='OK')
        pass

        
routes.handlers += [
    (r'/v1.0/manager/category/all', sCategoryAllHandler),
    (r'/v1.0/manager/category', sCategoryOneHandler),
]
