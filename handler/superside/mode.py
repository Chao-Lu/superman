from handler.base import BaseHandler
import routes
import time
import json
from handler.exceptions import ResourceNotExistError,PermissionDeniedError,ArgsError,StateError,RelateResError
from handler.unit.unit import get_timestamp
class ModeHandler(BaseHandler):
    """
        @api {get} /v1.0/manager/mode/all 获取圈子详情

        @apiGroup index
        @apiVersion  1.0.0
        @apiDescription 获取圈子详情

        @apiPermission user
        @apiParam    {string}    condition    
        @apiParam    {string}    sortby
        @apiParam    {string}    sort
        @apiParam    {string}    limit
        @apiParam    {string}    skip
        @apiSuccess    {list}        mode        圈子详情
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
        modelist = await self.db.mode.get_mode_free(condition,sortby,sort,limit,skip)
        
        self.finish_success(result=modelist)
    
class VoteModeHandler(BaseHandler):
    """
        @api {get} /v1.0/manager/mode/vote 获取圈子详情

        @apiGroup index
        @apiVersion  1.0.0
        @apiDescription 获取圈子详情

        @apiPermission user
        @apiParam    {string}    mode_id    圈子Id
        @apiParam    {string}    mtype    圈子Id
        @apiParam    {string}    position    圈子Id
        @apiSuccess    {list}        mode        圈子详情
    """
    async def get(self):


        user_info=await self.user_info
        mode_id=self.get_argument('mode_id',default=None)
        mode = await self.db.mode.get_by_id(mode_id)
        if mode['type'] != 'vote':
            raise ResourceNotExistError('w')
        if  mode['belongActivity']!='':
            activity=await self.db.circle.get_by_id(mode['belongActivity'])
            activity={
                '_id':activity['_id'],
                'title':activity['title'],
            }
        else:
            activity={
                '_id':'',
                'title':''
                }
        voteNumMap = mode['function']['voteNumMap']
        for i in range(0,len(mode['function']['optList'])):
            mode['function']['optList'][i]['num']=voteNumMap[mode['function']['optList'][i]['feature']]
        mode={
            'beginTime':mode['beginTime'],
            'endTime':mode['endTime'],
            'title':mode['title'],
            'avatar':mode['avatar'],
            'content':mode['content'],
            'belongActivity':activity,
            'state':mode['state'],
            'type':mode['type'],
            'joinNum':mode['function']['supportNum'],
            'function':{
                'optList':mode['function']['optList'],
                'typeAB':mode['function']['typeAB'],
            }
        }
        self.finish_success(result=mode)



    """
        @api {post} /v1.0/manager/mode/vote 获取圈子详情

        @apiGroup index
        @apiVersion  1.0.0
        @apiDescription 获取圈子详情

        @apiPermission user
        @apiParam    {string}    mode.beginTime    圈子Id
        @apiParam    {string}    mode.endTime        圈子Id
        @apiParam    {string}    mode.content        圈子Id
        @apiParam    {string}    mode.title        圈子Id
        @apiParam    {string}    mode.optList        圈子Id
        @apiParam    {string}    mode.typeAB        圈子Id
        @apiParam    {string}    mode.avatar        圈子Id
        @apiParam    {string}    mode.activity_id        圈子Id
        
        @apiSuccess    {list}        mode_id        圈子详情
    """
    async def post(self):
        user_info=await self.user_info
        mode=self.json_body['mode']
        beginTime=time.mktime(time.strptime(mode['beginTime'],'%Y-%m-%d %H:%M:%S'))
        endTime=time.mktime(time.strptime(mode['endTime'],'%Y-%m-%d %H:%M:%S'))
        content=mode['content']
        optList=mode['optList']
        typeAB=mode['typeAB']
        title=mode['title']
        avatar=mode['avatar']
        activity_id=mode['activity_id']
        voteNumMap={}
        if(activity_id!=""):
            activity=await self.db.circle.get_by_id(activity_id)
            if(activity is None or activity['type']!='activity'):
                raise ResourceNotExistError("")

        for i in range(0,len(optList)):
            optList[i]={'content':optList[i],'feature':self.produce_order_number(),'state':'on'}
            voteNumMap[optList[i]['feature']]=0
        mode_default = self.db.base.get_mode_default('vote')
        
        mode_default={
            'beginTime':beginTime,
            'endTime':endTime,
            'title':title,
            'avatar':avatar,
            'content':content,
            'state':'on',
            'type':'vote',
            'joinList':[],
            'entryDate':self.get_timestamp(),
            'belongActivity':activity_id,
            'function':{
                'optList':optList,
                'supportMap':{},
                'typeAB':typeAB,
                'supportNum':0,
                'voteNumMap':voteNumMap,
            }
        }
        mode_id = await self.db.mode.insert(mode_default)
        if(activity_id!=""):
            await self.db.circle.insert_mode(activity_id,str(mode_id))
        self.finish_success(result=mode_id)
    """
        @api {put} /v1.0/manager/mode/vote 获取圈子详情

        @apiGroup index
        @apiVersion  1.0.0
        @apiDescription 获取圈子详情

        @apiPermission user
        @apiParam    {string}    mode_id        圈子Id
        @apiParam    {string}    mtype        圈子Id
        @apiParam    {string}    content        圈子Id
        
        @apiSuccess    {list}        mode_id        圈子详情
    """
    async def put(self):
        user_info=await self.user_info
        json_body=self.json_body
        mode_id=json_body['mode_id']
        mtype=json_body['mtype']
        content=json_body['content']
        mode =await self.db.mode.get_by_id(mode_id)
        if mode is None or mode['type']!='vote':
            raise ResourceNotExistError("")
        if mtype == "insert_opt":
            optList=mode['function']['optList']
            voteNumMap=mode['function']['voteNumMap']
            for opt in content['optList']:
                feature=self.produce_order_number()
                optList.append({'content':opt,'feature':feature,'state':'on'})
                voteNumMap[feature]=0
            await self.db.mode.update(mode_id,{"$set":{'function.optList':optList,'function.voteNumMap':voteNumMap}})
        elif  mtype == "remove_opt":
            feature=content['feature']
            optList=[]
            for opt in mode['function']['optList']:
                if opt['feature'] !=feature:
                    optList.append(opt)
            await self.db.mode.update(mode_id,{'$set':{'function.optList':optList}})
        elif mtype == 'non_belong':
            activity_id=mode['belongActivity']
            if activity_id == '':
                pass
            else:
                self.db.mode.update(mode_id,{'$set':{'belongActivity':''}})
                self.db.circle.remove_mode(activity_id,mode_id)
        elif mtype == 'delete':
            activity_id=mode['belongActivity']
            if activity_id == '':
                pass
            else:
                await self.db.mode.update(mode_id,{'$set':{'belongActivity':''}})
                await self.db.circle.remove_mode(activity_id,mode_id)
            await self.db.mode.update(mode_id,{'$set':{'state':'removed'}})
        elif mtype == 'ch_belong':
            activity = await self.db.circle.get_by_id
            activity_id=mode['belongActivity']
            if activity_id != '':
                raise ResourceNotExistError("")
            else:
                newa_id=content['activity_id']
                activity = await self.db.circle.get_by_id(newa_id)
                if activity is None:
                    raise ResourceNotExistError("")
                await self.db.mode.update(mode_id,{'$set':{'belongActivity':newa_id}})
                await self.db.circle.insert_mode(newa_id,mode_id)
        elif mtype == 'ch_state':
            if mode['state']=='on':
                await self.db.mode.update(mode_id,{'$set':{'state':'off'}})
            else:
                await self.db.mode.update(mode_id,{'$set':{'state':'on'}})
        elif mtype == 'update_other':
            new_mode=content
            if 'beginTime' in new_mode.keys():
                new_mode['beginTime']=time.mktime(time.strptime(new_mode['beginTime'],'%Y-%m-%d %H:%M:%S'))
            if 'endTime' in new_mode.keys():    
                new_mode['endTime']=time.mktime(time.strptime(new_mode['endTime'],'%Y-%m-%d %H:%M:%S'))
            if 'typeAB' in new_mode.keys():
                await self.db.mode.update(mode_id,{'$set':{'function.typeAB':new_mode['typeAB']}})
                new_mode.pop('typeAB')
            mode_default={
                'beginTime':'',
                'endTime':'',
                'title':'',
                'avatar':'',
                'content':'',
            }
            mode_default= self.db.base.dict_match(mode,mode_default)
            mode_default= self.db.base.dict_match(new_mode,mode_default)
            await self.db.mode.update(mode_id,{'$set':mode_default})
        self.finish_success(result=mode_id)
class SeatModeHandler(BaseHandler):
    """
        @api {get} /v1.0/manager/mode/seat 获取圈子详情

        @apiGroup index
        @apiVersion  1.0.0
        @apiDescription 获取圈子详情

        @apiPermission user
        @apiParam    {string}    mode_id    圈子Id
        @apiParam    {string}    mtype    圈子Id
        @apiParam    {string}    position    圈子Id
        @apiSuccess    {list}        mode        圈子详情
    """
    async def get(self):
        user_info=await self.user_info
        mode_id=self.get_argument('mode_id',default=None)
        mode = await self.db.mode.get_by_id(mode_id)
        mode={
            'beginTime':mode['beginTime'],
            'endTime':mode['endTime'],
            'title':mode['title'],
            'avatar':mode['avatar'],
            'content':mode['content'],
            'belongActivity':mode['belongActivity'],
            'state':mode['state'],
            'type':mode['type'],
            'ajoinNum':len(mode['ajoinList']),
            'function':{
                'seatMap':mode['seatMap'],
                'userMap':mode['userMap'],
                'userList':mode['userList'],
                'state':mode['state'],
                
            }
        }
        self.finish_success(result=mode)
    """
        @api {post} /v1.0/manager/mode/vote 获取圈子详情

        @apiGroup index
        @apiVersion  1.0.0
        @apiDescription 获取圈子详情

        @apiPermission user
        @apiParam    {string}    mode.beginTime        圈子Id
        @apiParam    {string}    mode.endTime        圈子Id
        @apiParam    {string}    mode.content        圈子Id
        @apiParam    {string}    mode.title        圈子Id
        @apiParam    {string}    mode.avatar        圈子Id
        @apiParam    {string}    mode.HTmap        圈子Id#close open space block stage
        @apiParam    {string}    mode.seatStateList    圈子Id
        @apiParam    {string}    mode.seatNameList    圈子Id
        @apiSuccess    {list}        mode_id            圈子详情
    """
    async def post(self):
        user_info=await self.user_info
        mode=self.json_body['mode']
        beginTime=time.mktime(time.strptime(mode['beginTime'],'%Y-%m-%d %H:%M:%S'))
        endTime=time.mktime(time.strptime(mode['endTime'],'%Y-%m-%d %H:%M:%S'))
        content=mode['content']
        HTmap=mode['HTmap']
        seatStateList=mode['seatStateList']
        seatNameList=mode['seatNameList']
        seatUserList=['' for i in range(0,len(seatNameList))]
        title=mode['title']
        avatar=mode['avatar']
        
        
        mode_default = self.db.base.get_mode_default('seat')
        mode_default={
            'beginTime':beginTime,
            'endTime':endTime,
            'title':title,
            'avatar':avatar,
            'content':content,
            'belongActivity':'',
            'state':'on',
            'type':'seat',
            'joinList':[],
            'joinNum':0,
            'entryDate':self.get_timestamp(),
            'function':{
                'seatStateList':seatStateList,
                'seatNameList':seatNameList,
                'seatUserList':seatUserList,
                'HTmap':HTmap,
                'userList':[],
                'state':'on',
                'joinMap':{},
            }
        }
        mode_id = await self.db.mode.insert(mode_default)
        self.finish_success(result=mode_id)
routes.handlers += [
    (r'/v1.0/manager/mode/all', ModeHandler),
    (r'/v1.0/manager/mode/vote',VoteModeHandler),
    (r'/v1.0/manager/mode/seat',SeatModeHandler),
]
