from handler.base import BaseHandler
import routes
import random
import config
import handler.unit
from handler.exceptions import ResourceNotExistError,PermissionDeniedError,ArgsError,StateError,RelateResError
class PostPushHandler(BaseHandler):
    """
        @api {post} /v1.0/supervise/post/push 动态推送
        @apiGroup manager
        @apiVersion  1.0.0
        @apiDescription 动态推送

        @apiPermission manager
        
        @apiParam    {string}    post_id

        @apiSuccess    {string}    result "OK"

    """
    async def post(self):
        user_info = await self.user_info
        if  await self.is_supervise(str(user_info['_id'])):
            pass
        else:
            raise PermissionDeniedError("无权")
        jsonObj= self.json_body
        post_id=jsonObj['post_id']
        post = await self.db.post.get_by_id(post_id)
        if post['state'] != 'on':
            raise ResourceNotExistError("post 无效")
        postlist =await self.db.post.get_post_free({'content':post_id,'state':'ipush'},'_id','+',100,0)
        if len(postlist)>0:
            self.finish_success(result='OK')
            return
        post_de=self.db.base.get_post_default()
        post_de['state']='ipush'
        post_de['publisher']=post['publisher']
        post_de['content']=post_id
        post_de['pushTime']=self.get_timestamp()
        post_de['isAffiche']='no'
        await self.db.post.update(post_id,{'isPush':'YES'})
        await self.db.post.insert(post_de)
        self.finish_success(result='OK')
    async def delete(self):
        user_info = await self.user_info
        if  await self.is_supervise(str(user_info['_id'])):
            pass
        else:
            raise PermissionDeniedError("无权")
        jsonObj= self.json_body
        post_id=jsonObj['post_id']
        post = await self.db.post.get_by_id(post_id)
        if post['state'] != 'on':
            raise ResourceNotExistError("post 无效")
        postlist =await self.db.post.get_post_free({'content':post_id,'state':'ipush'},'_id','+',100,0)
        for post in postlist:
            await self.db.post.update(post['_id'],{'state':'off'})
        await self.db.post.update(post_id,{'isPush':'NO'})
        self.finish_success(result='OK')
        pass
class PostSpecialHandler(BaseHandler):
    """
        @api {post} /v1.0/supervise/post/special 动态加精
        @apiGroup manager
        @apiVersion  1.0.0
        @apiDescription 动态加精

        @apiPermission manager
        
        @apiParam    {string}    post_id

        @apiSuccess    {string}    result "OK"

    """
    async def post(self):
        user_info = await self.user_info
        if  await self.is_supervise(str(user_info['_id'])):
            pass
        else:
            raise PermissionDeniedError("无权")
        jsonObj= self.json_body
        post_id=jsonObj['post_id']
        post = await self.db.post.get_by_id(post_id)
        if post['state'] != 'on':
            raise ResourceNotExistError("post 无效")
        if post['isSpecial'] != 'no':
            raise ResourceNotExistError("post 已加精")
        

        await self.db.post.update(post_id,{'isSpecial':'yes'})
        await self.db.circle.insert_special_post(post['belongCircle'],post_id)
        self.finish_success(result='OK')
    async def delete(self):
        user_info = await self.user_info
        if  await self.is_supervise(str(user_info['_id'])):
            pass
        else:
            raise PermissionDeniedError("无权")
        jsonObj= self.json_body
        post_id=jsonObj['post_id']
        post = await self.db.post.get_by_id(post_id)
        if post['state'] != 'on':
            raise ResourceNotExistError("post 无效")
        if post['isSpecial'] != 'yes':
            raise ResourceNotExistError("post 已加精")
        

        await self.db.post.update(post_id,{'isSpecial':'no'})
        await self.db.circle.remove_special_post(post['belongCircle'],post_id)
        self.finish_success(result='OK')
        pass
class PostTopHandler(BaseHandler):
    """
        @api {post} /v1.0/supervise/post/top 动态置顶
        @apiGroup manager
        @apiVersion  1.0.0
        @apiDescription 动态置顶

        @apiPermission manager
        
        @apiParam    {string}    post_id

        @apiSuccess    {string}    result "OK"

    """
    async def post(self):
        user_info = await self.user_info
        if  await self.is_supervise(str(user_info['_id'])):
            pass
        else:
            raise PermissionDeniedError("无权")
        jsonObj= self.json_body
        post_id=jsonObj['post_id']
        post = await self.db.post.get_by_id(post_id)
        if post['state'] != 'on':
            raise ResourceNotExistError("post 无效")

        await self.db.circle.insert_top_post(post['belongCircle'],post_id)
        self.finish_success(result='OK')
    async def delete(self):
        user_info = await self.user_info
        if  await self.is_supervise(str(user_info['_id'])):
            pass
        else:
            raise PermissionDeniedError("无权")
        jsonObj= self.json_body
        post_id=jsonObj['post_id']
        post = await self.db.post.get_by_id(post_id)
        if post['state'] != 'on':
            raise ResourceNotExistError("post 无效")

        await self.db.circle.remove_top_post(post['belongCircle'],post_id)
        self.finish_success(result='OK')
        pass
class PostIndexHandler(BaseHandler):
    """
        @api {post} /v1.0/supervise/post/index 动态置顶
        @apiGroup manager
        @apiVersion  1.0.0
        @apiDescription 动态置顶

        @apiPermission manager
        
        @apiParam    {string}    post_id

        @apiSuccess    {string}    result "OK"

    """
    async def post(self):
        user_info = await self.user_info
        if  await self.is_supervise(str(user_info['_id'])):
            pass
        else:
            raise PermissionDeniedError("无权")
        jsonObj= self.json_body
        
        post_id = jsonObj['post_id']
        post = await self.db.post.get_by_id(post_id)
        if post is None:
            raise RelateResError("动态不存在")
        index_src = {
            'type':'post',
            'contentId':post_id,
            'recommendDate':'',
            'state':'1',
            'position':1,
        }
        index_dst = self.db.base.dict_match(index_src,self.db.base.get_index_default())
        index_dst['recommendDate'] = self.get_timestamp()
        index_id = await self.db.index.insert(index_dst)
        self.finish_success(result=index_id)
class AppointBannerHandler(BaseHandler):
    async def post(self):
        user_info = await self.user_info
        if  await self.is_supervise(str(user_info['_id'])):
            pass
        else:
            raise PermissionDeniedError("无权")
        jsonObj= self.json_body
        appointment_id= jsonObj['appointment_id']
        appointment =await self.db.event.get_by_id(appointment_id)
        if appointment is None:
            raise RelateResError("动态不存在")
        bannerlist = await self.db.banner.get_banner_free({'contentId':appointment_id,'state':'1'},'_id','-',1000,0)
        if len(bannerlist) !=0:
            raise RelateResError("banner存在")
        banner_src={
            'state':'1',
            'type':'appointment',
            'contentId':appointment_id,
            'content':appointment['title'],
            'image':appointment['coverPhoto'],
            'time':self.get_timestamp(),
            'position':1,
        }
        banner_dst = self.db.base.dict_match(banner_src,self.db.base.get_banner_default())
        banner_id=await self.db.banner.insert(banner_dst)
        self.finish_success(result=banner_id)
    async def delete(self):
        user_info = await self.user_info
        if  await self.is_supervise(str(user_info['_id'])):
            pass
        else:
            raise PermissionDeniedError("无权")
        jsonObj= self.json_body
        appointment_id= jsonObj['appointment_id']
        bannerlist = await self.db.banner.get_banner_free({'contentId':appointment_id,'state':'1'},'_id','-',1000,0)
        if len(bannerlist) !=0:
            await self.db.banner.updateAll({'contentId':appointment_id,'state':'1'},{'$set':{'state':'2'}})
        self.finish_success(result='OK')
        
class AppointIndexHandler(BaseHandler):
    async def post(self):
        user_info = await self.user_info
        if  await self.is_supervise(str(user_info['_id'])):
            pass
        else:
            raise PermissionDeniedError("无权")
        jsonObj= self.json_body
        appointment_id= jsonObj['appointment_id']
        appointment =await self.db.event.get_by_id(appointment_id)
        if appointment is None:
            raise RelateResError("动态不存在")
        indexlist = await self.db.index.get_index_free({'contentId':appointment_id,'state':'1'},'_id','-',1000,0)
        if len(indexlist) !=0:
            raise RelateResError("banner存在")
        index_src={
            'type':'appointment',
            'contentId':appointment_id,
            'recommendDate':self.get_timestamp(),
            'state':'1',
            'position':1,
            'category':appointment['category'],
        }
        #index_dst = self.db.base.dict_match(index_src,self.db.base.get_index_default())
        index_id=await self.db.index.insert(index_src)
        self.finish_success(result=index_id)
    async def delete(self):
        user_info = await self.user_info
        if  await self.is_supervise(str(user_info['_id'])):
            pass
        else:
            raise PermissionDeniedError("无权")
        jsonObj= self.json_body
        appointment_id= jsonObj['appointment_id']
        indexlist = await self.db.index.get_index_free({'contentId':appointment_id,'state':'1'},'_id','-',1000,0)
        if len(indexlist) !=0:
            await self.db.index.updateAll({'contentId':appointment_id,'state':'1'},{'$set':{'state':'2'}})
        self.finish_success(result='OK')    
routes.handlers += [
    (r'/v1.0/supervise/post/push',PostPushHandler),
    (r'/v1.0/supervise/post/special',PostSpecialHandler),
    (r'/v1.0/supervise/post/top',PostTopHandler),
    (r'/v1.0/supervise/post/index',PostIndexHandler),
    (r'/v1.0/supervise/appointment/index',AppointIndexHandler),
    (r'/v1.0/supervise/appointment/banner',AppointBannerHandler),
]
