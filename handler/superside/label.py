from handler.base import BaseHandler
import routes
import json
from handler.exceptions import ResourceNotExistError,PermissionDeniedError,ArgsError,StateError,RelateResError
class sLabelAllHandler(BaseHandler):    

    """
        @api {get} /v1.0/manager/label/all 获取首页推荐列表
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
        
        labellist = await self.db.label.get_label_free(condition,sortby,sort,limit,skip)
        self.finish_success(result=labellist)
        pass

class sLabelOneHandler(BaseHandler):    

    """
        @api {get} /v1.0/manager/label 获取首页推荐信息
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
        label_id = self.get_argument('label_id',default=None)
        label = await self.db.label.get_by_id(label_id)
        self.finish_success(result=label)
        pass
    """
        @api {put} /v1.0/manager/label 更改首页推荐信息
        @apiGroup manager
        @apiVersion  1.0.0
        @apiDescription 更改首页推荐信息

        @apiPermission manager
        
        @apiParam    {string}    label_id    首页推荐ID
        @apiParam    {Object}    label    更改内容
        
        
        @apiSuccess    {string}    result "OK"
    """
    async def put(self):
        self.prehandle()
        user_info=await self.user_info

        if not self.is_manager(user_info['masterId']):
            raise PermissionDeniedError("需要管理员用户")
        json = self.json_body
        label_id = json['label_id']
        label = json['label']
        
        Old_label = self.db.base.dict_match(await self.db.label.get_by_id(label_id),
            {
                'title':'',
            })
        New_label = self.db.base.dict_match(label,Old_label)
        await self.db.label.update(label_id,New_label)

        self.finish_success(result='OK')
        pass
    """
        @api {delete} /v1.0/manager/label 删除首页推荐
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
        label_id = json['label_id']
    #    await self.db.label.remove(label_id)
        self.finish_success(result='OK')
        pass
        
    """
        @api {post} /v1.0/manager/label 上传首页推荐
        @apiGroup manager
        @apiVersion  1.0.0
        @apiDescription 上传首页推荐

        @apiPermission manager
        
        @apiParam    {Object}    label    首页推荐
        
        @apiSuccess    {string}    label_id 首页推荐ID
    """
    async def post(self):
        self.prehandle()
        user_info=await self.user_info

        if not self.is_manager(user_info['masterId']):
            raise PermissionDeniedError("需要管理员用户")
        json = self.json_body['label']
        label_src = json
        label_dst = self.db.base.dict_match(label_src,self.db.base.get_label_default())
        label_dst['entryDate'] = self.get_timestamp()
        label_id = await self.db.label.insert(label_dst)

        self.finish_success(result=label_id)
        pass
    
class LabelMapHandler(BaseHandler):
    async def get(self):
        self.prehandle()
        user_info=await self.user_info

        if not self.is_manager(user_info['masterId']):
            raise PermissionDeniedError("需要管理员用户")
        labelMap = await self.db.label.get_labelMap()
        self.finish_success(result=labelMap)
    async def post(self):
        self.prehandle()
        user_info=await self.user_info

        if not self.is_manager(user_info['masterId']):
            raise PermissionDeniedError("需要管理员用户")
        labelm=self.json_body['labelMap']
        labelMap=[]
        for line in labelm:
            label=await self.db.label.get_by_id(line['firstLabel'])
            line['firstLabel']={
                'title':label['title'],
                'label_id':str(label['_id']),
            }
            for i in range(0,len(line['secondList'])):
                label=await self.db.label.get_by_id(line['secondList'][i])
                line['secondList'][i]={
                    'title':label['title'],
                    'label_id':str(label['_id']),
                }
            labelMap.append(line)
        #labelMap=[
        #        {    'firstLabel':{'title':'','label_id':''},
        #            'avatar':'',
        #            'secondList':[{'title':'','label_id':'',},{'title':'','label_id':'',}]},
        #    ]
        await self.db.label.get_labelMap()
        await self.db.label.update_labelMap(labelMap)
        self.finish_success(result='OK')
routes.handlers += [
    (r'/v1.0/manager/label/all', sLabelAllHandler),
    (r'/v1.0/manager/label', sLabelOneHandler),
    (r'/v1.0/manager/labelMap', LabelMapHandler),

]
