from handler.base import BaseHandler
import routes
from handler.exceptions import ResourceNotExistError,PermissionDeniedError,ArgsError,StateError,RelateResError


class sCircleHandler(BaseHandler):
    """
        @api {get} /v1.0/circle/all 获取圈子列表

        @apiGroup index
        @apiVersion  1.0.0
        @apiDescription 获取圈子列表

        @apiPermission user
        
        @apiSuccess    {list}    circlelist    圈子列表
    """
    async def get(self):
        user_info=await self.user_info
        condition = {'state':{'$ne':'off'},'type':'activity'}
        circlelist = await self.db.circle.get_circle_free(condition,'_id','-',1000,0)
        for i in range(0,len(circlelist)):
            circlelist[i]={
                'avatar':circlelist[i]['avatar'],
                'title':circlelist[i]['title'],
                '_id':str(circlelist[i]['_id'])
            }
        self.finish_success(result=circlelist)
        pass
class CircleHandler(BaseHandler):
    """
        @api {get} /v1.0/circle 获取圈子详情

        @apiGroup index
        @apiVersion  1.0.0
        @apiDescription 获取圈子详情

        @apiPermission user
        @apiParam    {string}    circle_id    圈子Id
        @apiSuccess    {list}        circle        圈子详情
    """
    async def get(self):
        user_info=await self.user_info
        circle_id=self.get_argument('circle_id',default=None)
        circle = await self.db.circle.get_by_id(circle_id)
        scircle={
                'avatar':circle['avatar'],
                'title':circle['title'],
                'postNum':len(circle['postList']),
                'seeNum':circle['seeNum'],
                'circleInfo':circle['circleInfo'],
                'specialPostNum':len(circle['specialPost']),
                #'topPost':[],
                'circleManager':await self.is_circleManager(circle_id,str(user_info['_id'])),
                'state':circle['state'],
                'location':circle['location'],
                'type':circle['type'],
                'activityList':[],
                'modeList':[],
                'afficheList':[],
                'moreInfo':circle['moreInfo'],
            }
        for activity_id in circle['activityList']:
            activity = await self.db.circle.get_by_id(activity_id)
            activity={
                'title':activity['title'],
                'avatar':activity['avatar'],
                '_id':activity['_id']
            }
            scircle['activityList'].append(activity)
        if len(circle['afficheList'])>0:
            affiche = await self.db.post.get_by_id(circle['afficheList'][-1])
            scircle['afficheList']=[await self.post_common(affiche,user_info)]
        else:
            scircle['afficheList']=[]
        scircle['afficheNum']=len(circle['afficheList'])
        for i in range(0,len(scircle['circleInfo']['orgaList'])):
            orign = await self.db.master.get_by_user(scircle['circleInfo']['orgaList'][i])
            scircle['circleInfo']['orgaList'][i]={
                'realName':orign['realName'],
                'avatar':orign['avatar'],
                'user_id':orign['userId'],
                'certificationInfo':orign['certificationInfo'],
            }
        for i in range(0,len(circle['modeList'])):
            mode = await self.db.mode.get_by_id(circle['modeList'][i])
            if mode['state']=='off':
                continue
            if mode['type']=='vote':
                avatarList=[]
                voteNumMap = mode['function']['voteNumMap']
                for i in range(0,len(mode['function']['optList'])):
                    mode['function']['optList'][i]['num']=voteNumMap[mode['function']['optList'][i]['feature']]
                mode['function']['optList'].sort(key=lambda x: x['num'])
                for opt in mode['function']['optList']:
                    avatarList.append(opt['content']['avatar'])
                mode ={
                    'avatar':mode['avatar'],
                    '_id':mode['_id'],
                    'title':mode['title'],
                    'content':mode['content'],
                    'joinNum':mode['function']['supportNum'],
                    'type':mode['type'],
                    'avatarList':avatarList[0:3],
                }
            elif mode['type']=='seat':
                mode = {
                    'avatar':mode['avatar'],
                    '_id':mode['_id'],
                    'title':mode['title'],
                    'content':mode['content'],
                    'joinNum':mode['joinNum'],
                    'type':mode['type'],
                    'isJoin':str(user_info['_id']) in mode['function']['userList'],
                }
            scircle['modeList'].append(mode)
        await self.db.circle.insert_seenum(circle_id)
        self.finish_success(result=scircle)
        pass
class CirclePostHandler(BaseHandler):
    """
        @api {get} /v1.0/circle/post 获取圈子动态

        @apiGroup banner
        @apiVersion  1.0.0
        @apiDescription 获取圈子动态

        @apiPermission user
        @apiParam {string} pagesize    页大小
        @apiParam {string} time        页大小
        @apiParam {string} location    页大小
        @apiParam {string} circle_id    页大小
        @apiSuccess    {list}    postlist    动态列表
    """
    async def get(self):
        user_info=await self.user_info
        ntime=self.get_timestamp()
        time=float(self.get_argument('time',default=ntime))
        circle_id=self.get_argument('circle_id',default='')
        pagesize=int(self.get_argument('pagesize',default=10))
        location=self.get_argument('location',default='')
        condition = {'pushTime':{'$lt':time},'belongCircle':circle_id,'state':'on','isAffiche':'no'}
        if location != '':
            condition['location']=location

        postlist = await self.db.post.get_post_free(condition,'pushTime','-',pagesize,0)
        for i in range(0,len(postlist)):
            postlist[i]=await self.post_common(postlist[i],user_info)
        self.finish_success(result=postlist)
class CircleSpecialPostHandler(BaseHandler):
    """
        @api {get} /v1.0/circle/post/special 获取圈子精品动态

        @apiGroup banner
        @apiVersion  1.0.0
        @apiDescription 获取圈子精品动态

        @apiPermission user
        @apiParam {string} pagesize    页大小
        @apiParam {string} time        页大小
        @apiParam {string} location    页大小
        @apiParam {string} circle_id    页大小
        @apiSuccess    {list}    postlist    动态列表
    """
    async def get(self):
        user_info=await self.user_info
        ntime=self.get_timestamp()
        time=float(self.get_argument('time',default=ntime))
        circle_id=self.get_argument('circle_id',default='')
        pagesize=int(self.get_argument('pagesize',default=10))
        
        location=self.get_argument('location',default='')
        condition = {'pushTime':{'$lt':time},'belongCircle':circle_id,'state':'on','isSpecial':'yes'}
        if location != '':
            condition['location']=location
        postlist = await self.db.post.get_post_free(condition,'pushTime','-',pagesize,0)
        for i in range(0,len(postlist)):
            postlist[i]=await self.post_common(postlist[i],user_info)
        self.finish_success(result=postlist)
class CircleAffichePostHandler(BaseHandler):
    """
        @api {get} /v1.0/circle/post/affiche 获取圈子精品动态

        @apiGroup banner
        @apiVersion  1.0.0
        @apiDescription 获取圈子精品动态

        @apiPermission user
        @apiParam {string} pagesize    页大小
        @apiParam {string} time        页大小
        @apiParam {string} circle_id    页大小
        @apiSuccess    {list}    postlist    动态列表
    """
    async def get(self):
        user_info=await self.user_info
        ntime=self.get_timestamp()
        time=float(self.get_argument('time',default=ntime))
        circle_id=self.get_argument('circle_id',default='')
        pagesize=int(self.get_argument('pagesize',default=10))
        condition = {'pushTime':{'$lt':time},'belongCircle':circle_id,'state':'on','isAffiche':'yes'}
        postlist = await self.db.post.get_post_free(condition,'pushTime','-',pagesize,0)
        for i in range(0,len(postlist)):
            postlist[i]=await self.post_common(postlist[i],user_info)
        self.finish_success(result=postlist)
routes.handlers += [
    (r'/v1.0/circle/all', sCircleHandler),
    (r'/v1.0/circle', CircleHandler),
    (r'/v1.0/circle/post', CirclePostHandler),
    (r'/v1.0/circle/post/special', CircleSpecialPostHandler),
    (r'/v1.0/circle/post/affiche',CircleAffichePostHandler),
]
