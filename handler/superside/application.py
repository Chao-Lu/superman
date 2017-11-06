from handler.base import BaseHandler
import routes
import json
from handler.exceptions import ResourceNotExistError,PermissionDeniedError,ArgsError,StateError,RelateResError
class sApplicationAllHandler(BaseHandler):    

    """
        @api {get} /v1.0/manager/application/all 获取申请列表
        @apiGroup manager
        @apiVersion  1.0.0
        @apiDescription 获取申请列表

        @apiPermission manager
        
        @apiParam    {string}    condition    
        @apiParam    {string}    sortby
        @apiParam    {string}    sort
        @apiParam    {string}    limit
        @apiParam    {string}    skip
        
        @apiSuccess    {Object}    applicationlist    申请信息
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
        
        applicationlist = await self.db.application.get_application_free(condition,sortby,sort,limit,skip)
        
        self.finish_success(result=applicationlist)
        pass

class sApplicationOneHandler(BaseHandler):

    """
        @api {get} /v1.0/manager/application 获取申请信息
        @apiGroup manager
        @apiVersion  1.0.0
        @apiDescription 获取申请信息

        @apiPermission manager
        
        @apiParam    {string}    application_id    
        
        @apiSuccess    {Object}    application    申请信息
    """
    async def get(self):
        self.prehandle()
        user_info=await self.user_info

        if not self.is_manager(user_info['masterId']):
            raise PermissionDeniedError("需要管理员用户")
        application_id = self.get_argument('application_id',default=None)
        application = await self.db.application.get_by_id(application_id)
        self.finish_success(result=application)
        pass
    """
        @api {put} /v1.0/manager/application 更改申请信息
        @apiGroup manager
        @apiVersion  1.0.0
        @apiDescription 更改申请信息

        @apiPermission manager
        
        @apiParam    {string}    application_id    
        @apiParam    {Object}    application
        
        @apiSuccess    {string}    result "OK"

    """
    async def put(self):
        self.prehandle()
        user_info=await self.user_info

        if not self.is_manager(user_info['masterId']):
            raise PermissionDeniedError("需要管理员用户")
        json = self.json_body
        application_id = json['application_id']
        application = json['application']
        
        Old_application = self.db.base.dict_match(await self.db.application.get_by_id(application_id),
            {
                #'title':'',
                #'userId':'',
                #'type':'',
                #'content':'',
                #'time':'',
                'state':'',
                'handler':'',
                'illustrate':''
            })
        New_application = self.db.base.dict_match(application,Old_application)
        (success, result) = await self.db.application.update(application_id,New_application)
        if success:
            self.finish_success(result='OK')
        else :
            self.finish_err(400, result)
        

class sMasterApplicationHandler(BaseHandler):
    async def put(self):
        self.prehandle()
        user_info=await self.user_info

        if not self.is_manager(user_info['masterId']):
            raise PermissionDeniedError("需要管理员用户")
        jsonstr = self.json_body
        application_id = jsonstr['application_id']
        application = jsonstr['application']
        
        application_content = await self.db.application.get_by_id(application_id)
        user_id = application_content["userId"]
        Old_application = self.db.base.dict_match(application_content,
            {
                'state':'',
                'handler':'',
                'illustrate':''
            })
        New_application = self.db.base.dict_match(application,Old_application)
        (success, result) = await self.db.application.update(application_id,New_application)
        if not success:
            raise StateError(result)
            return
        # 将用户变成达人
        user_info = await self.db.user.get_by_id(user_id)
        if self.is_master(user_info['masterId']):
            raise StateError("该用户已是达人")
        if application['state'] == 'approved':
            appli_cont = json.loads(application_content['content'])
            master_src = {}
            master_src['userId']=str(user_id)
            master_src['state'] ='new'
            master_src['avatar']=user_info['avatar']
            master_src['realName']=appli_cont['name']
            master_src['realTitle']=appli_cont['title']
            master_src['personalDetails']=appli_cont['introduction']
            master_src['phone']=appli_cont['phone']
            master_src['masterPhoto']=appli_cont['images']
            master_src['entryDate']=self.get_timestamp()
            master_dst = self.db.base.dict_match(master_src,self.db.base.get_master_default())
            masterId = await self.db.master.insert(master_dst)
            await self.db.user.update(user_id,{'masterId':str(masterId)})
        self.finish_success(result='ok')


routes.handlers += [
    (r'/v1.0/manager/application/all', sApplicationAllHandler),
    (r'/v1.0/manager/application', sApplicationOneHandler),
    (r'/v1.0/manager/masterapplication', sMasterApplicationHandler),
]
