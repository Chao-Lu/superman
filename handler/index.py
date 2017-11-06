from handler.base import BaseHandler
import routes
from handler.exceptions import ResourceNotExistError,PermissionDeniedError,ArgsError,StateError,RelateResError
from handler.unit.unit import ObjectId 
import bson
import random
class IndexHandler(BaseHandler):
    """
        @api {get} /v1.0/index 获取首页推荐列表

        @apiGroup index
        @apiVersion  1.0.0
        @apiDescription 获取首页推荐列表

        @apiPermission user
        
        @apiSuccess    {list}    indexlist    首页推荐列表
    """
    async def get(self):
        user_info=await self.user_info
        condition = {'state':'1','$or':[{'type':'event'},{'type':'master'}]}
        
        indexlist = await self.db.index.get_index_free(condition,'position','-',1000,0)
        for i in range(0,len(indexlist)):
            if indexlist[i]['type'] == 'event':
                indexlist[i]['content'] = self.db.event.brief_event(await self.db.event.get_by_id(indexlist[i]['contentId']))
            elif indexlist[i]['type'] == 'master':
                indexlist[i]['content'] = self.db.master.brief_master(await self.db.master.get_by_user(indexlist[i]['contentId']))
        self.finish_success(result=indexlist)
        pass
        
class NewBannerHandler(BaseHandler):
    """
        @api {get} /v1.0/new_banner 获取首页轮播图

        @apiGroup banner
        @apiVersion  1.0.0
        @apiDescription 获取首页轮播图

        @apiPermission user
        
        @apiParam   {string} typ    'appointment'

        @apiSuccess    {list}    eventlist    轮播图
    """
    async def get(self):
        user_info=await self.user_info
        typ = self.json_body['typ']
        condition = {'type':typ}
        event_list = await self.db.event.get_event_free(condition,'_id','-',1000,0)

        eventlist = []
        for event in event_list:
            event['favorNum'] = len(event['likeUserList'])
            event['appointmentNum'] = await self.db.order.get_event_orderlist_length(str(event['_id']))
            tip_list = await self.db.tip.find_by_to_event_id(str(event['_id']))
            event['tipNum'] = len(tip_list)
            master = await self.db.master.get_by_user(event['belongedMaster'])
            if master:
                event['briefMaster'] = self.db.master.brief_master(master)
                if str(user_info['_id']) in str(event['likeUserList']):
                    event['isLike'] = 'Yes'
                else:
                    event['isLike'] = 'No'
                eventlist.append(event)
        self.finish_success(result=eventlist)

class BannerHandler(BaseHandler):
    """
        @api {get} /v1.0/banner 获取首页轮播图

        @apiGroup banner
        @apiVersion  1.0.0
        @apiDescription 获取首页轮播图

        @apiPermission user
        

        @apiSuccess    {list}    bannerlist    轮播图
    """
    async def get(self):
        user_info=await self.user_info
        condition = {'state':'1','$or':[{'type':'event'},{'type':'master'}]}
        bannerlist = await self.db.banner.get_banner_free(condition,'time','-',1000,0)
        self.finish_success(result=bannerlist)
        
class cIndexHandler(BaseHandler):
    """
        @api {get} /v1.0/index/circle/all 获取圈子推荐列表

        @apiGroup index
        @apiVersion  1.0.0
        @apiDescription 获取圈子推荐列表

        @apiPermission user
        
        @apiSuccess    {list}    indexlist    首页推荐列表
    """
    async def get(self):
        user_info=await self.user_info
        user_info=await self.user_info
        condition = {'state':'on','type':'normal'}
        circlelist = await self.db.circle.get_circle_free(condition,'position','-',1000,0)
        for i in range(0,len(circlelist)):
            circlelist[i]={
                'avatar':circlelist[i]['avatar'],
                'title':circlelist[i]['title'],
                '_id':circlelist[i]['_id']
            }
        condition = {'state':'on','type':'news'}
        toplist = await self.db.circle.get_circle_free(condition,'_id','-',1000,0)
        for i in range(0,len(toplist)):
            toplist[i]={
                'avatar':toplist[i]['avatar'],
                'title':'校园新鲜事',#toplist[i]['title'],
                '_id':toplist[i]['_id']
            }
        
        
        condition = {'state':'1','type':'post'}
        indexlist = await self.db.index.get_index_free(condition,'recommendDate','-',6,0)
        inlist=[]
        for i in range(0,len(indexlist)):
            if indexlist[i]['type'] == 'post':
                post    = self.db.post.brief_post(await self.db.post.get_by_id(indexlist[i]['contentId']))
                content = await self.post_common(post,user_info)
                if content['title']=='':
                    content['title']=content['content']
                if content['state']=='off':
                    continue
                inlist.append({
                    'title':content['title'],
                    'publisherAvatar':content['publisher']['avatar'],
                    '_id':content['_id']
                })
            
        self.finish_success(result={'indexlist':inlist,'toplist':toplist,'circlelist':circlelist})
        pass        
class CircleHandler(BaseHandler):
    """
        @api {get} /v1.0/index/circle 获取圈子

        @apiGroup banner
        @apiVersion  1.0.0
        @apiDescription 获取圈子

        @apiPermission user
        @apiParam {string} pagesize    页大小
        @apiParam {string} time    页大小
        
        @apiSuccess    {list}    postlist    动态列表
    """
    async def get(self):
        user_info=await self.user_info
        ntime=self.get_timestamp()
        time=float(self.get_argument('time',default=ntime))
        condition = {'pushTime':{'$lt':time},'isAffiche':'no','belongCircleType':{'$ne':'activity'}}
        condition['$or']=[]
        
        pagesize=int(self.get_argument('pagesize',default=10))
        user_info['userFavorMaster'].append(user_info['_id'])
        clist={'$and':[]}
        clist['$and'].append({'state':'ipush'})
        for masterId in user_info['userFavorMaster']:
            condition['$or'].append({'publisher':str(masterId),'state':'on'})
            clist['$and'].append({'publisher':{'$ne':str(masterId)}})
        condition['$or'].append(clist)
        postlist = await self.db.post.get_post_free(condition,'pushTime','-',pagesize,0)
        for i in range(0,len(postlist)):
            postlist[i]=await self.post_common(postlist[i],user_info)
        self.finish_success(result=postlist)
class SuperviseCircleHandler(BaseHandler):
    """
        @api {get} /v1.0/index/circle/supervise 获取圈子

        @apiGroup banner
        @apiVersion  1.0.0
        @apiDescription 获取圈子

        @apiPermission user
        @apiParam {string} pagesize    页大小
        @apiParam {string} time    页大小
        
        @apiSuccess    {list}    postlist    动态列表
    """
    async def get(self):
        user_info=await self.user_info
        ntime=self.get_timestamp()
        time=float(self.get_argument('time',default=ntime))
        condition = {'state':{'$ne':'off'},'pushTime':{'$lt':time},'isAffiche':'no','belongCircleType':{'$ne':'activity'}}
        pagesize=int(self.get_argument('pagesize',default=10))
        postlist = await self.db.post.get_post_free(condition,'pushTime','-',pagesize,0)
        print(condition)
    
        for i in range(0,len(postlist)):
            postlist[i]=await self.post_common(postlist[i],user_info)
        self.finish_success(result=postlist)
        
class LabelMapHandler(BaseHandler):
    """
        @api {get} /v1.0/index/labelMap 获取圈子

        @apiGroup banner
        @apiVersion  1.0.0
        @apiDescription 获取圈子

        @apiPermission user
        
        @apiSuccess    {list}    postlist    动态列表
    """
    async def get(self):
        user_info=await self.user_info
        labelMap = await self.db.label.get_labelMap()
        self.finish_success(result=labelMap)
    
class IndexAppointHandler(BaseHandler):
    """
        @api {get} /v1.0/index/appointment 获取约见主页信息

        @apiGroup banner
        @apiVersion  1.0.0
        @apiDescription 获取约见主页信息

        @apiPermission user
        @apiParam {string} pagesize    页大小
        @apiParam {string} time    页大小
        
        @apiSuccess    {list}    postlist    动态列表
    """
    async def get(self):
        user_info = await self.user_info
        user_info=await self.user_info
        condition = {'state':'1','type':'appointment'}
        bannerlist = await self.db.banner.get_banner_free(condition,'time','-',1000,0)
        condition = {'type':'appointment'}
        categorylist = await self.db.category.get_category_free(condition,'_id','-',1000,0)
        for i in range(0,len(categorylist)):
            cate = categorylist[i]
            categorylist[i]=cate
        self.finish_success(result={'bannerlist':bannerlist,'categorylist':categorylist})
        
class IndexAppointListHandler(BaseHandler):
    """
        @api {get} /v1.0/index/appointment/list 获取所有的约见

        @apiGroup banner
        @apiVersion  1.0.0
        @apiDescription 获取所有的约见

        @apiPermission user
        @apiParam     {string} category    类别
        @apiSuccess    {list}    postlist    动态列表
    """
    async def get(self):
        user_info=await self.user_info
        ntime=self.get_timestamp()
        category=self.get_argument('category',default='~')
        if category == '~':
            time=float(self.get_argument('time',default=ntime))
            condition = {'state':'1','lastChangeTime':{'$lt':time},'type':'appointment'}
            pagesize=int(self.get_argument('pagesize',default=10))
            appointlist = await self.db.event.get_event_free(condition,'lastChangeTime','-',pagesize,0)
    
            for i in range(0,len(appointlist)):
                appointlist[i]['belongedMaster']= await self.db.master.get_by_user(appointlist[i]['belongedMaster'])
                appointlist[i]['isFavor'] = str(user_info['_id']) in str(appointlist[i]['likeUserList'])
                appointlist[i]['favorNum'] = len(appointlist[i]['likeUserList'])
                appointlist[i]['appointmentNum'] = await self.db.order.get_event_orderlist_length(str(appointlist[i]['_id']))
                tip_list = await self.db.tip.find_by_to_event_id(str(appointlist[i]['_id']))
                appointlist[i]['tipNum'] = len(tip_list)
            self.finish_success(result=appointlist)
        else:
            time=float(self.get_argument('time',default=ntime))
            condition = {'state':'1','lastChangeTime':{'$lt':time},'type':'appointment','category':category}
            pagesize=int(self.get_argument('pagesize',default=10))
            appointlist = await self.db.event.get_event_free(condition,'lastChangeTime','-',pagesize,0)
    
            for i in range(0,len(appointlist)):
                appointlist[i]['belongedMaster']= await self.db.master.get_by_user(appointlist[i]['belongedMaster'])
                appointlist[i]['isFavor'] = str(user_info['_id']) in str(appointlist[i]['likeUserList'])
            self.finish_success(result=appointlist)
class RecommendAppointHandler(BaseHandler):
    """
        @api {get} /v1.0/index/appointment/recommend 获取个人主页的随机推荐约见

        @apiGroup banner
        @apiVersion  1.0.0
        @apiDescription 获取个人主页的随机推荐约见

        @apiPermission user
        @apiParam     {string} category    类别
        @apiSuccess    {list}    postlist    动态列表
    """
    async def get(self):
        user_info=await self.user_info
        ntime=self.get_timestamp()
        condition = {'state':'1','type':'appointment'}
        appointNum= await self.db.event.get_event_count(condition)
        skip = random.randint(0,max(appointNum-5,0))
        
        
        
        
        appointlist = await self.db.event.get_event_free(condition,'lastChangeTime','-',5,skip)
        for i in range(0,len(appointlist)):
            event = appointlist[i]
            event['favorNum'] = len(event['likeUserList'])
            event['appointmentNum'] = await self.db.order.get_event_orderlist_length(str(event['_id']))
            tip_list = await self.db.tip.find_by_to_event_id(str(event['_id']))
            event['tipNum'] = len(tip_list)
            master = await self.db.master.get_by_user(event['belongedMaster'])
            if master:
                event['belongedMaster'] = self.db.master.brief_master(master)
            event['isFavor'] = str(user_info['_id']) in str(event['likeUserList'])
            appointlist[i]=event
    
        self.finish_success(result=appointlist)

class IndexAppointHandler(BaseHandler):
    """
        @api {get} /v1.0/index/appointment/index 推荐主页的推荐约见

        @apiGroup banner
        @apiVersion  1.0.0
        @apiDescription 推荐主页的推荐约见

        @apiPermission user
        
        @apiSuccess    {list}    postlist    动态列表
    """
    async def get(self):
        user_info=await self.user_info
        ntime=self.get_timestamp()
        category=self.get_argument('category',default='~')
        if category == '~':
            condition = {'state':'1','type':'appointment'}
            indexList= await self.db.index.get_index_free(condition,'_id','-',1000,0)
            appointlist=[]
            for index in indexList:
                appointlist.append( await self.db.event.get_by_id(index['contentId']))
            for i in range(0,len(appointlist)):
                event = appointlist[i]
                event['favorNum'] = len(event['likeUserList'])
                event['appointmentNum'] = await self.db.order.get_event_orderlist_length(str(event['_id']))
                tip_list = await self.db.tip.find_by_to_event_id(str(event['_id']))
                event['tipNum'] = len(tip_list)
                master = await self.db.master.get_by_user(event['belongedMaster'])
                if master:
                    event['belongedMaster'] = self.db.master.brief_master(master)

                event['isFavor'] = str(user_info['_id']) in str(event['likeUserList'])
                appointlist[i]=event
    
            self.finish_success(result=appointlist)
        else:
            condition = {'state':'1','type':'appointment','category':category}
            indexList= await self.db.index.get_index_free(condition,'_id','-',1000,0)
            appointlist=[]
            for index in indexList:
                appointlist.append( await self.db.event.get_by_id(index['contentId']))
            for i in range(0,len(appointlist)):
                event = appointlist[i]
                event['favorNum'] = len(event['likeUserList'])
                event['appointmentNum'] = await self.db.order.get_event_orderlist_length(str(event['_id']))
                tip_list = await self.db.tip.find_by_to_event_id(str(event['_id']))
                event['tipNum'] = len(tip_list)
                master = await self.db.master.get_by_user(event['belongedMaster'])
                if master:
                    event['belongedMaster'] = self.db.master.brief_master(master)
                event['isFavor'] = str(user_info['_id']) in str(event['likeUserList'])
                appointlist[i]=event
    
            self.finish_success(result=appointlist)
class IndexHotCommentHandler(BaseHandler):
    """
        @api {get} /v1.0/index/comment/hot hotcomment

        @apiGroup banner
        @apiVersion  1.0.0
        @apiDescription hotcomment

        @apiPermission user
        @apiParam {string} pagesize    页大小
        @apiParam {string} time    页大小
        
        @apiSuccess    {list}    commentlist    动态列表
    """
    async def get(self):
        user_info=await self.user_info
        ntime=self.get_timestamp()
        pagesize=int(self.get_argument('pagesize',default=10))
        time=float(self.get_argument('time',default=ntime))
        condition = {'state':'on','commentTime':{'$lt':time},'commentType':'appointment'}
        commentlist = await self.db.comment.get_comment_free(condition,'commentTime','-',pagesize,0)
        for i in range(0,len(commentlist)):
            comment =     commentlist[i]
            comment['commenter'] = self.db.user.brief_user(await self.db.user.get_by_id(comment['commenter']))
            comment['event'] = await self.db.event.get_by_id(comment['postId'])
            comment['event']['belongedMaster'] = self.db.master.brief_master(await self.db.master.get_by_user(comment['event']['belongedMaster']))
            commentlist[i] = comment
        self.finish_success(result=commentlist)
routes.handlers += [
    (r'/v1.0/index', IndexHandler),
    (r'/v1.0/banner', BannerHandler),
    (r'/v1.0/new_banner',NewBannerHandler),
    (r'/v1.0/index/circle/supervise', SuperviseCircleHandler),
    (r'/v1.0/index/circle', CircleHandler),    
    (r'/v1.0/index/circle/all',cIndexHandler),
    (r'/v1.0/index/labelMap',LabelMapHandler),
    (r'/v1.0/index/appointment',IndexAppointHandler),
    (r'/v1.0/index/appointment/list',IndexAppointListHandler),
    (r'/v1.0/index/appointment/recommend',RecommendAppointHandler),
    (r'/v1.0/index/appointment/index',IndexAppointHandler),
    (r'/v1.0/index/comment/hot',IndexHotCommentHandler),
    
]
