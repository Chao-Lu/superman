from handler.base import BaseHandler
import routes
from tornado.httpclient import AsyncHTTPClient,HTTPError,HTTPRequest
import json
import time
import config
from handler.unit.unit import ObjectId
from handler.exceptions import ResourceNotExistError,PermissionDeniedError,ArgsError,StateError,RelateResError



            
class UserApplicationHandler(BaseHandler):
    """
        @api {post} /v1.0/user/application 用户提出申请
        @apiGroup user
        @apiVersion  1.0.0
        @apiDescription 用户提出申请
        @apiPermission user
        
        @apiParam    {string}    application    用户申请
        
        @apiSuccess    {string}    result "OK"
    """
    async def post(self):
        user_info=await self.user_info

        json = self.json_body
        application = json['application']
        application_src = {
            'title':application['title'],
            'userId':user_info['_id'],
            'type':application['type'],
            'content':application['content'],
            'time':self.get_timestamp(),
            'state':'new',
        }
        application_dst = self.db.base.dict_match(application_src,self.db.base.get_application_default())
        (success, result) = await self.db.application.insert(application_dst)
        if success:
            self.finish_success(result=result)
        else:
            self.finish_err(400,result)
    """
        @api {get} /v1.0/user/application 查询用户申请
        @apiGroup user
        @apiVersion  1.0.0
        @apiDescription 查询用户申请
        @apiPermission user
        
        @apiParam    {string}    page        页数
        @apiParam    {string}    pagesize    页大小
        
        @apiSuccess    {list}    applicationlist    用户申请列表
    """
    async def get(self):
        user_info=await self.user_info

        page = int(self.get_argument('page',default=1))
        pagesize = int(self.get_argument('pagesize',default=10))
        applicationlist = await self.db.application.get_application_free(
            condition = {'userId':user_info['_id']},
            sortby='time',
            sort='-',
            limit=pagesize,
            skip=(page-1)*pagesize)
        self.finish_success(result=applicationlist)

class UserFavorHandler(BaseHandler):
    """
        @api {get} /v1.0/user/favor 查询用户收藏
        @apiGroup user
        @apiVersion  1.0.0
        @apiDescription 查询用户收藏
        @apiPermission user
        
        @apiParam    {string}    type(master)    收藏类型
        
        @apiSuccess    {list}    favorlist    收藏内容列表
    """
    async def get(self):
        user_info=await self.user_info

        type=self.get_argument("type",default=None)

        if type == 'master':
            favormaster=user_info['userFavorMaster']
            for i in range(0,len(favormaster)):
                user=await self.db.user.get_by_id(favormaster[i])
                favormaster[i]={
                    '_id':user['_id'],
                    'avatar':user['avatar'],
                    'realName':user['realName'],
                    'certificationInfo':user['certificationInfo']
                }
            self.finish_success(result=favormaster)
        elif type == 'appointment':
            favorappointment = user_info['userFavorTeam']
            for i in range(0,len(favorappointment)):
                event = await self.db.event.get_by_id(favorappointment[i])
                event['favorNum'] = len(event['likeUserList'])
                event['appointmentNum'] = await self.db.order.get_event_orderlist_length(str(event['_id']))
                tip_list = await self.db.tip.find_by_to_event_id(str(event['_id']))
                event['tipNum'] = len(tip_list)
                master = await self.db.master.get_by_user(event['belongedMaster'])
                if master:
                    event['belongedMaster'] = self.db.master.brief_master(master)
                event['isFavor'] = str(user_info['_id']) in str(event['likeUserList'])
                favorappointment[i]=event
            self.finish_success(result=favorappointment)
        elif type == 'event':
            favorevent = user_info['userFavorEvent']
            for i in range(0,len(favorevent)):
                event = await self.db.event.get_by_id(favorevent[i])
                event['favorNum'] = len(event['likeUserList'])
                event['appointmentNum'] = await self.db.order.get_event_orderlist_length(str(event['_id']))
                tip_list = await self.db.tip.find_by_to_event_id(str(event['_id']))
                event['tipNum'] = len(tip_list)
                master = await self.db.master.get_by_user(event['belongedMaster'])
                if master:
                    event['belongedMaster'] = self.db.master.brief_master(master)
                event['isFavor'] = str(user_info['_id']) in str(event['likeUserList'])
                favorevent[i]=event
            self.finish_success(result=favorevent)
        else:
            self.finish_err()
    """
        @api {POST} /v1.0/user/favor 添加用户收藏
        @apiGroup user
        @apiVersion  1.0.0
        @apiDescription 添加用户收藏
        @apiPermission user
        
        @apiParam    {string}    type(master)    收藏类型
        @apiParam    {string}    id                收藏对象ID
        
        @apiSuccess    {string}    result "OK"
    """
    async def post(self):
        user_info=await self.user_info

        json = self.json_body
        type=json['type']
        id=json['id']
        #TO DO
        if type is None:
            self.finish_err()
            return
        if type == 'master':
            user = await self.db.user.get_by_id(id)
            if user is None:
                raise ResourceNotExistError("用户不存在")
            await self.db.user.insert_favor_master(str(user_info['_id']),id)
            await self.db.user.insert_favorMe(id,str(user_info['_id']))
            self.finish_success(result="OK")
        elif type == 'appointment':
            appointment = await self.db.event.get_by_id(id)
            if appointment is None:
                raise ResourceNotExistError("用户不存在")
            await self.db.user.insert_favor_team(str(user_info['_id']),id)
            await self.db.event.insert_like(id,str(user_info['_id']))
            self.finish_success(result="OK")
        elif type == 'event':
            event = await self.db.event.get_by_id(id)
            if event is None:
                raise ResourceNotExistError("用户不存在")
            await self.db.user.insert_favor_event(str(user_info['_id']),id)
            await self.db.event.insert_like(id,str(user_info['_id']))
            self.finish_success(result="OK")
        else:
            self.finish_err()
    
    """
        @api {delete} /v1.0/user/favor 删除用户收藏
        @apiGroup user
        @apiVersion  1.0.0
        @apiPermission user
        @apiDescription 删除用户收藏


        @apiParam    {string}    type(1:master)    收藏类型
        @apiParam    {string}    id                收藏对象ID
        
        @apiSuccess    {string}    result "OK"    
    """
    async def delete(self):
        user_info=await self.user_info

        json = self.json_body
        type=json['type']
        id=json['id']
        if type is None:
            self.finish_err()
            return
        if type == 'master':
            await self.db.user.remove_favor_master(str(user_info['_id']),id)
            await self.db.user.remove_favorMe(id,str(user_info['_id']))
            self.finish_success(result="OK")
        elif type == 'appointment':
            await self.db.user.remove_favor_team(str(user_info['_id']),id)
            await self.db.event.remove_like(id,str(user_info['_id']))
            self.finish_success(result="OK")
        elif type == 'event':
            await self.db.user.remove_favor_event(str(user_info['_id']),id)
            await self.db.event.remove_like(id,str(user_info['_id']))
            self.finish_success(result="OK")
        else:
            self.finish_err()




class UserTeamHandler(BaseHandler):
    """
        @api {get} /v1.0/userTeam 获取用户组 
        @apiGroup user
        @apiVersion  1.0.0
        @apiPermission user
        @apiDescription 获取用户组

        
        @apiSuccess    {string}    result "OK"    
    """
    async def get(self):
        user_info=await self.user_info
        userTeam={}
        uTeam=[]
        if 'userTeam' not in user_info.keys() or user_info['userTeam'] == '':
            isleader='null'
            token = await self.db.token.get_by_user(user_info['_id'])
            noticeholder=await self.db.noticeholder.get_by_user(user_info['_id'])
            uTeam.append(
                {
                    'accessToken':token['accessToken'],
                    'userId':user_info['_id'],
                    'realName':user_info['realName'],
                    'avatar':user_info['avatar'],
                    'isleader':'null',
                    'noticeNum':len(noticeholder['unhandle']),
                    'issupervise':await self.is_supervise(user_info['_id'])
                }
            )
        else:
            userTeam=await self.db.userteam.get_by_id(user_info['userTeam'])
            if str(user_info['_id'])== userTeam['teamLeader']    :
                isleader='yes'
            else:
                isleader='no'
            teamLeader_token = await self.db.token.get_by_user(ObjectId(userTeam['teamLeader']))
            teamLeader_info = await self.db.user.get_by_id(userTeam['teamLeader'])
            noticeholder=await self.db.noticeholder.get_by_user(userTeam['teamLeader'])
            userTeam['teamLeader']={
                'accessToken':teamLeader_token['accessToken'],
                'userId':userTeam['teamLeader'],
                'realName':teamLeader_info['realName'],
                'avatar':teamLeader_info['avatar'],
                'isleader':'yes',
                'noticeNum':len(noticeholder['unhandle']),
                'issupervise':await self.is_supervise(userTeam['teamLeader'])
            }
            
            uTeam.append(userTeam['teamLeader'])
            for i in range(0,len(userTeam['teamMember'])):
                member_id=userTeam['teamMember'][i]
                member_token =await self.produce_accessToken(member_id)
                member_info = await self.db.master.get_by_user(member_id)
                noticeholder=await self.db.noticeholder.get_by_user(member_id)
                member={
                    'accessToken':member_token['accessToken'],
                    'userId':member_id,
                    'realName':member_info['realName'],
                    'avatar':member_info['avatar'],
                    'isleader':'no',
                    'noticeNum':len(noticeholder['unhandle']),
                    'issupervise':await self.is_supervise(member_id)
                }
                uTeam.append(member)
        self.finish_success(result={'isleader':isleader,'uTeam':uTeam})
        
class UserPersonHandler(BaseHandler):
    """
        @api {get} /v1.0/user/display 个人主页信息
        @apiGroup master
        @apiVersion  1.0.0
        @apiDescription 个人主页信息
        @apiPermission user

        @apiParam    {string}    user_id

        
        @apiSuccess    {list}    user    个人主页信息
    """
    async def get(self):
        user_info=await self.user_info
        user_id = self.get_argument('user_id',default= None)
        user = await self.db.user.get_by_id(user_id)
        person={}
        person['user']={
            '_id':user['_id'],
            'avatar':user['avatar'],
            'coverPhoto':user['coverPhoto'],
            'realName':user['realName'],
            'favorMaster':user_id in user_info['userFavorMaster'],
            'certificationInfo':user['certificationInfo'],
            'userType':user['userType'],
            'favorMeNum':len(user['favorMeList']),
        }
        if self.is_master(user['masterId']):
            master = await self.db.master.get_by_user(user_id)
            person['isMaster']='yes'
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
            person['masterinfo']={
                'imageList':imageList,
                'eventList':eventList,
            }
        else:
            person['isMaster']='no'
        self.finish_success(result=person)
class UserPostHandler(BaseHandler):
    """
        @api {get} /v1.0/user/deisplay/post 获取圈子

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
            postlist[i]=await self.post_common(postlist[i],user_info)
        self.finish_success(result=postlist)
routes.handlers += [
    (r'/v1.0/user/application', UserApplicationHandler),
    (r'/v1.0/user/favor', UserFavorHandler),

    (r'/v1.0/userTeam',UserTeamHandler),
    (r'/v1.0/user/display',UserPersonHandler),
    (r'/v1.0/user/display/post', UserPostHandler),
]
