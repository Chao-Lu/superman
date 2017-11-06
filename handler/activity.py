from handler.base import BaseHandler
import routes
from handler.exceptions import ResourceNotExistError,PermissionDeniedError,ArgsError,StateError,RelateResError


class sActivityHandler(BaseHandler):
    """
        @api {get} /v1.0/activity/all 获取圈子列表

        @apiGroup index
        @apiVersion  1.0.0
        @apiDescription 获取圈子列表

        @apiPermission user
        
        @apiSuccess    {list}    activitylist    圈子列表
    """
    async def get(self):
        user_info=await self.user_info
        condition = {'state':{'$ne':'off'},'type':'activity'}
        activitylist = await self.db.circle.get_circle_free(condition,'_id','-',1000,0)
        for i in range(0,len(activitylist)):
            activitylist[i]={
                'avatar':activitylist[i]['avatar'],
                'title':activitylist[i]['title'],
                '_id':str(activitylist[i]['_id'])
            }
        self.finish_success(result=activitylist)
        pass
class ActivityHandler(BaseHandler):
    """
        @api {get} /v1.0/activity 获取圈子详情

        @apiGroup index
        @apiVersion  1.0.0
        @apiDescription 获取圈子详情

        @apiPermission user
        @apiParam    {string}    activity_id    圈子Id
        @apiSuccess    {list}        activity        圈子详情
    """
    async def get(self):
        user_info=await self.user_info
        activity_id=self.get_argument('activity_id',default=None)
        activity = await self.db.circle.get_by_id(activity_id)
        sactivity={
                'avatar':activity['avatar'],
                'title':activity['title'],
                'postNum':len(activity['postList']),
                'seeNum':activity['seeNum'],
                'circleInfo':activity['circleInfo'],
                'specialPostNum':len(activity['specialPost']),
                #'topPost':[],
                'circleManager':await self.is_circleManager(circle_id,str(user_info['_id'])),
                'state':activity['state'],
                'location':activity['location'],
                'type':activity['type'],
            }
        if activity['type']!='activity':
            raise ResourceNotExistError()
        await self.db.circle.insert_seenum(activity_id)
        self.finish_success(result=sactivity)
        pass
class ActivityPostHandler(BaseHandler):
    """
        @api {get} /v1.0/activity/post 获取圈子动态

        @apiGroup banner
        @apiVersion  1.0.0
        @apiDescription 获取圈子动态

        @apiPermission user
        @apiParam {string} pagesize    页大小
        @apiParam {string} time    页大小
        @apiParam {string} activity_id    页大小
        @apiSuccess    {list}    postlist    动态列表
    """
    async def get(self):
        user_info=await self.user_info
        ntime=self.get_timestamp()
        time=float(self.get_argument('time',default=ntime))
        activity_id=self.get_argument('activity_id',default='')
        pagesize=int(self.get_argument('pagesize',default=10))
        condition = {'pushTime':{'$lt':time},'belongCircle':activity_id,'state':'on'}
        

        postlist = await self.db.post.get_post_free(condition,'pushTime','-',pagesize,0)
        for i in range(0,len(postlist)):
            postlist[i]=await self.post_common(postlist[i],user_info)
        self.finish_success(result=postlist)
class ActivitySpecialPostHandler(BaseHandler):
    """
        @api {get} /v1.0/activity/post/special 获取圈子精品动态

        @apiGroup banner
        @apiVersion  1.0.0
        @apiDescription 获取圈子精品动态

        @apiPermission user
        @apiParam {string} pagesize    页大小
        @apiParam {string} time    页大小
        @apiParam {string} activity_id    页大小
        @apiSuccess    {list}    postlist    动态列表
    """
    async def get(self):
        user_info=await self.user_info
        ntime=self.get_timestamp()
        time=float(self.get_argument('time',default=ntime))
        activity_id=self.get_argument('activity_id',default='')
        pagesize=int(self.get_argument('pagesize',default=10))
        condition = {'pushTime':{'$lt':time},'belongCircle':activity_id,'state':'on','isSpecial':'yes'}
        postlist = await self.db.post.get_post_free(condition,'pushTime','-',pagesize,0)
        for i in range(0,len(postlist)):
            postlist[i]=await self.post_common(postlist[i],user_info)
        self.finish_success(result=postlist)
routes.handlers += [
    (r'/v1.0/activity/all', sActivityHandler),
    (r'/v1.0/activity', ActivityHandler),
    (r'/v1.0/activity/post', ActivityPostHandler),
    (r'/v1.0/activity/post/special', ActivitySpecialPostHandler),
]
