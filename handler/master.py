from handler.base import BaseHandler
import routes
from handler.exceptions import ResourceNotExistError,PermissionDeniedError,ArgsError,StateError,RelateResError

class MastersIndexHandler(BaseHandler):
    """
        @api {get} /v1.0/master/index 获取所有达人列表(按分类划分)
        @apiGroup master
        @apiVersion  1.0.0
        @apiDescription 获取所有达人列表

        @apiPermission user
        
        @apiParam    {string}    type    

        
        @apiSuccess    {Object}    masterlist    达人列表
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
        condition['state']='on'
        masterlist=[]
        for i in range(0,len(categorylist)):            
            condition['category']=str(categorylist[i]['_id'])
            mlist=await self.db.master.get_master_free(condition,sortby,sort,limit,skip)
            if len(mlist) == 0:
                continue
            masterlist.append({'category':categorylist[i],'masters':mlist})
            
        self.finish_success(result=masterlist)
        pass 


class MastersHandler(BaseHandler):
    """
        @api {get} /v1.0/master/all 获取达人列表
        @apiGroup master
        @apiVersion  1.0.0
        @apiDescription 获取达人列表

        @apiPermission user
        
        @apiParam    {string}    condition    
        @apiParam    {string}    sortby
        @apiParam    {string}    sort
        @apiParam    {string}    limit
        @apiParam    {string}    skip
        
        @apiSuccess    {Object}    masterlist    达人信息
    """
    async def get(self):
        user_info=await self.user_info


        condition = json.loads(self.get_argument('condition',default='{}'))
        sortby = str(self.get_argument('sortby',default='_id'))
        sort = str(self.get_argument('sort',default='+'))
        limit = int(self.get_argument('limit',default=10))
        skip = int(self.get_argument('skip',default=0))
        

        masterlist = await self.db.master.get_master_free(condition,sortby,sort,limit,skip)
        


        self.finish_success(result=masterlist)
        pass


class MasterHandler(BaseHandler):    
    """
        @api {get} /v1.0/master 获取达人详情(商业部)
        @apiGroup master
        @apiVersion  1.0.0
        @apiDescription 获取达人详情

        @apiPermission user
        
        @apiParam    {string}    user_id    达人ID
        
        @apiSuccess    {Object}    master    达人信息
    """
    async def get(self):
        user_info=await self.user_info
        user_id = self.get_argument('user_id',default= None)
        isMe=0
        if user_id is None:
            user_id=str(user_info['_id'])
            isMe=1
        master = await self.db.master.get_by_user(user_id)
        master_default ={
            'userId':'', 
            'state':'',
            'realName':'',
            'avatar':'',
            'coverPhoto':'',
            'location':'',
            'category':'',
            'realTitle':'',
            'masterLabel':[],#标签
            'personalDetails':'',#个人简介
            'entryDate':'',
            'masterPhoto':[],#展示图片
            'phone':'',
            'masterSign':'',#签名
            'masterContact':{},#联系方式　'wxNumber','QQNumber','phoneNumber'　
        }
        if master is None:
            master_info={}
            userInfo = await self.db.user.get_by_id(user_id)
            master_info['realName'] = userInfo['realName']
            master_info['avatar'] = userInfo['avatar']
            master_info['location'] = userInfo['university']
            master_info['entryDate'] = ''
            master_info=self.db.base.dict_match(master_info,self.db.base.get_master_default())
            master_info['eventlist']=[]
            master_info['courselist']=[]
            
            master_info['isFavor'] = str(userInfo['_id']) in user_info['userFavorMaster']
            self.finish_success(result=master_info)
            pass
            #raise ResourceNotExistError("达人不存在")
        else:
            master_info = self.db.base.dict_match(master,master_default)

            #达人查询自己的信息
            if str(user_id) == str(master['userId']):
                master_info['vcoin'] = user_info['vcoin']
                master_info['total_money'] = int(master['order_money']) + int(master['tip_money'])
                if master_info['location'] == '':
                    master_info['location'] = user_info['university']
            if isMe == 0:
                event_list=await self.db.event.get_event_free({'belongedMaster':user_id,'type':'appointment','state':'1'},'type','+',10000,0)
            else:
                event_list=await self.db.event.get_event_free({'belongedMaster':user_id,'type':'appointment' },'type','+',10000,0)
            eventlist=[]
            for event in event_list:
                event['favorNum'] = len(event['likeUserList'])
                event['appointmentNum'] = await self.db.order.get_event_orderlist_length(str(event['_id']))
                tip_list = await self.db.tip.find_by_to_event_id(str(event['_id']))
                event['tipNum'] = len(tip_list)

                comment_len = len(event['commentList'])
                if comment_len == 0:
                    event['firstCommentContent'] = ''
                else:
                    firstComment = await self.db.comment.get_by_id(event['commentList'][comment_len-1])
                    event['firstCommentContent'] = firstComment['content']

                eventlist.append(event)
            master_info['eventlist']=eventlist
            if isMe == 0:
                event_list=await self.db.event.get_event_free({'belongedMaster':user_id,'type':{'$ne':'appointment'},'state':'on'},'type','+',10000,0)
            else:
                event_list=await self.db.event.get_event_free({'belongedMaster':user_id,'type':{'$ne':'appointment'} },'type','+',10000,0)
            eventlist=[]
            for event in event_list:
                event['favorNum'] = len(event['likeUserList'])
                event['appointmentNum'] = await self.db.order.get_event_orderlist_length(str(event['_id']))
                tip_list = await self.db.tip.find_by_to_event_id(str(event['_id']))
                event['tipNum'] = len(tip_list)

                comment_len = len(event['commentList'])
                if comment_len == 0:
                    event['firstCommentContent'] = ''
                else:
                    firstComment = await self.db.comment.get_by_id(event['commentList'][comment_len-1])
                    event['firstCommentContent'] = firstComment['content']

                eventlist.append(event)
            master_info['courselist']=eventlist
            
            
            master_info['isFavor'] = str(user_info['_id']) in user_info['userFavorMaster']
            self.finish_success(result=master_info)
            pass
class MasterCommentHandler(BaseHandler):
    """
        @api {get} /v1.0/appointment/comment 达人拒绝约见

        @apiGroup appointment
        @apiVersion  1.0.0
        @apiDescription 达人拒绝约见

        @apiPermission master
        @apiParam {string}  pagesize    页大小
        @apiParam {string}  time    页大小
        @apiParam   {string}    master_id    订单id     
        
        @apiSuccess {string}    result 'ok' 
    """

    async def get(self):
        user_info=await self.user_info
        ntime=self.get_timestamp()
        pagesize=int(self.get_argument('pagesize',default=10))
        time=float(self.get_argument('time',default=ntime))
        master_id = self.get_argument('master_id',default=None)
        condition = {'state':'1','type':'appointment','belongedMaster':master_id}
        appointmentList = await self.db.event.get_event_free(condition,'_id','-',100,0)
        condition = {'state':'on','commentTime':{'$lt':time},'commentType':'appointment','$or':[]}
        for a in appointmentList:
            condition['$or'].append({'postId':str(a['_id'])})
        if len(condition['$or']) == 0:
            self.finish_success(result=[])
            return 
        commentlist = await self.db.comment.get_comment_free(condition,'commentTime','-',pagesize,0)
        for i in range(0,len(commentlist)):
            comment =     commentlist[i]
            comment['commenter'] = self.db.user.brief_user(await self.db.user.get_by_id(comment['commenter']))
            comment['event'] = await self.db.event.get_by_id(comment['postId'])
            comment['event']['belongedMaster'] = self.db.master.brief_master(await self.db.master.get_by_user(comment['event']['belongedMaster']))
            commentlist[i] = comment
        self.finish_success(result=commentlist)
        pass

class MasterAppointmentHandler(BaseHandler):
    """
        @api {get} /v1.0/master/appointment 获取达人详情(商业部)
        @apiGroup master
        @apiVersion  1.0.0
        @apiDescription 获取达人详情

        @apiPermission user
        @apiParam {string} pagesize    页大小
        @apiParam {string} time    页大小
        
        @apiParam    {string}    user_id    达人ID
        
        @apiSuccess    {Object}    master    达人信息
    """
    async def get(self):
        user_info=await self.user_info
        ntime=self.get_timestamp()
        pagesize=int(self.get_argument('pagesize',default=10))
        time=float(self.get_argument('time',default=ntime))
        user_id = self.get_argument('user_id',default= None)
        isMe=0
        if user_id is None:
            user_id=str(user_info['_id'])
            isMe=1
            
        if isMe == 0:
            event_list=await self.db.event.get_event_free({'belongedMaster':user_id,'lastChangeTime':{'$lt':time},'state':'1'},'lastChangeTime','-',pagesize,0)
        else:
            event_list=await self.db.event.get_event_free({'belongedMaster':user_id ,'lastChangeTime':{'$lt':time}},'lastChangeTime','-',pagesize,0)
        eventlist=[]
        for event in event_list:
            event['favorNum'] = len(event['likeUserList'])
            event['appointmentNum'] = await self.db.order.get_event_orderlist_length(str(event['_id']))
            tip_list = await self.db.tip.find_by_to_event_id(str(event['_id']))
            event['tipNum'] = len(tip_list)

            comment_len = len(event['commentList'])
            if comment_len == 0:
                event['firstCommentContent'] = ''
            else:
                firstComment = await self.db.comment.get_by_id(event['commentList'][comment_len-1])
                event['firstCommentContent'] = firstComment['content']

            eventlist.append(event)
        self.finish_success(result=eventlist)
class MasterUpdateHandler(BaseHandler):
    """
        @api {put} /v1.0/master/masterinfo 更新达人信息
        @apiGroup master
        @apiVersion  1.0.0
        @apiDescription 获取达人卡片信息
        @apiPermission user

        @apiParam    {string}    master    达人信息
        
        @apiSuccess    {list}    cardlist    卡片信息列表
    """
    async def put(self):
        user_info=await self.user_info
            
        jsonObj=self.json_body
        user_id=user_info['_id']
        user_info = await self.db.user.get_by_id(user_id)
        if not self.is_master(user_info['masterId']):
            master_src ={} #json['master']
            master_src['userId']=str(user_id)
            master_src['avatar']=user_info['avatar']
            master_src['realName']=user_info['realName']
            master_src['state']='new'
            master_src['entryDate']=self.get_timestamp()
            master_src['masterContact']={'wxNumber':'','QQNumber':'','phoneNumber':user_info['phoneNumber']}
            master_dst = self.db.base.dict_match(master_src,self.db.base.get_master_default())
            masterId = await self.db.master.insert(master_dst)
            await self.db.user.update(user_id,{'masterId':str(masterId)})
        
        
        master_info= await self.db.master.get_by_user(user_id)
        master_id=master_info['_id']
        #可更新内容列表
        Update_module={
            #'userId':'', 
            #'state':'',
            'realName':'',
            'avatar':'',
            'coverPhoto':'',
            'location':'',
            #'category':'',
            'realTitle':'',
            'masterLabel':[],
            'personalDetails':'',
            #'entryDate':'',
            'masterPhoto':[],
            'phone':'',
            'masterContact':{},
            'masterSign':'',
            # 下面的数据暂时不用
            #'contact':'',
            #'certificationInfo':'',
            #'masterLargEvent':[],
            #'masterOrders':[],
            #'masterFiance':[],
            #'masterNotification':[],
            #'masterMessage':[],
            #'collectionQuantity':'',
            #'relatePhoto':[]
        }
        master_default = self.db.base.dict_match(master_info,Update_module)
        master_info=self.db.base.dict_match(
            jsonObj['master'],
            master_default
        )
        await self.db.master.update(master_id,master_info)
        await self.db.user.update(user_id,
                {'realName':master_info['realName'],'avatar':master_info['avatar']})

        self.finish_success(result="OK")
        
        pass


class MasterPersonHandler(BaseHandler):
    """
        @api {get} /v1.0/master/display 达人个人主页信息
        @apiGroup master
        @apiVersion  1.0.0
        @apiDescription 达人个人主页信息
        @apiPermission user

        @apiParam    {string}    user_id

        
        @apiSuccess    {list}    master    达人个人主页信息
    """
    async def get(self):
        user_info=await self.user_info
        user_id = self.get_argument('user_id',default= None)
        master = await self.db.master.get_by_user(user_id)
        if master is None:
            raise ResourceNotExistError("达人不存在")

        imageList=[]
        for image in master['masterPhoto']:
            imageList.append(image)
            if len(imageList)==3:
                break

        eventList = await self.db.event.get_event_free({'belongedMaster':user_id,'state':{'$ne':'off'}},'lastChangeTime','-',2,0)
        for i in range(0,len(eventList)):
            event = eventList[i]
            eventList[i]={
                '_id':event['_id'],
                'title':event['title'],
                'photosDisplay':[event['photosDisplay'][0]],
                'category':event['category'],
                'slogan':event['slogan'],
                'type':event['type'],
            }
        
        master={
            '_id':master['_id'],
            'avatar':master['avatar'],
            'coverPhoto':master['coverPhoto'],
            'realName':master['realName'],
            'realTitle':master['realTitle'],
            'favorMaster':user_id in user_info['userFavorMaster'],
            'imageList':imageList,
            'eventList':eventList,
        }
        
        self.finish_success(result=master)

class MasterPostHandler(BaseHandler):
    """
        @api {get} /v1.0/master/deisplay/post 获取圈子

        @apiGroup banner
        @apiVersion  1.0.0
        @apiDescription 获取圈子

        @apiPermission user
        @apiParam {string} pagesize    页大小
        @apiParam {string} time    页大小
        @apiParam    {string}    user_id
        
        @apiSuccess    {list}    postlist    动态列表
    """
    async def get(self):
        user_info=await self.user_info
        ntime=self.get_timestamp()
        time=float(self.get_argument('time',default=ntime))
        pagesize=int(self.get_argument('pagesize',default=10))
        user_id = self.get_argument('user_id',default= None)
        condition={'publisher':user_id,'pushTime':{'$lt':time},'state':'on'}
        postlist = await self.db.post.get_post_free(condition,'pushTime','-',pagesize,0)
        
        for i in range(0,len(postlist)):
            post=postlist[i]
            publisher=await self.db.master.get_by_user(post['publisher'])
            commentlist=[]
            for j in range(0,min(3,len(post['commentList']))):
                comment= await self.db.comment.get_by_id(post['commentList'][j])
                user = await self.db.user.get_by_id(comment['commenter'])
                commentlist.append({'userName':user['realName'],'content':comment['content']})
            post={
                '_id':post['_id'],
                'publisher':{
                    '_id':publisher['userId'],
                    'avatar':publisher['avatar'],
                    'realName':publisher['realName'],
                    'realTitle':publisher['realTitle']
                    },
                'like':    str(user_info['_id']) in post['likeUserList'],
                'likeNum':len(post['likeUserList']),
                'commentNum':len(post['commentList']),
                'commentList':commentlist,
                'favorMaster':str(publisher['userId']) in user_info['userFavorMaster'],
                'title':post['title'],
                'content':post['content'],
                'multiMedia':post['multiMedia'],
                'publishTime':post['publishTime'],
                'type':post['type'],
                'state':post['state'],
                'pushTime':post['pushTime'],            
            }
            postlist[i]=post
        self.finish_success(result=postlist)


routes.handlers += [
    (r'/v1.0/master/display', MasterPersonHandler),
    (r'/v1.0/master/display/post', MasterPostHandler),
    (r'/v1.0/master', MasterHandler),
    (r'/v1.0/master/update/masterinfo', MasterUpdateHandler),
    (r'/v1.0/master/all',MastersHandler),
    (r'/v1.0/master/index',MastersIndexHandler),
    (r'/v1.0/master/comment',MasterCommentHandler),
]
