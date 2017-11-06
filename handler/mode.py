from handler.base import BaseHandler
import routes
from handler.exceptions import ResourceNotExistError,PermissionDeniedError,ArgsError,StateError,RelateResError
from handler.unit.unit import get_timestamp
from ORM.MongoDB.base import MongoDB_orm_base,ObjectId
class ModeHandler(BaseHandler):
    """
        @api {get} /v1.0/mode 获取圈子详情

        @apiGroup index
        @apiVersion  1.0.0
        @apiDescription 获取圈子详情

        @apiPermission user
        @apiParam    {string}    mode_id    圈子Id
        @apiSuccess    {list}        mode        圈子详情
    """
    async def get(self):
        user_info=await self.user_info
        mode_id=self.get_argument('mode_id',default=None)
        mode=await self.db.mode.get_by_id(mode_id)
        self.finish_success(result=mode)
        
class VoteModeHandler(BaseHandler):
    """
        @api {get} /v1.0/mode/vote 获取圈子详情

        @apiGroup index
        @apiVersion  1.0.0
        @apiDescription 获取圈子详情

        @apiPermission user
        @apiParam    {string}    mode_id    圈子Id
        @apiSuccess    {list}        mode        圈子详情
    """
    async def get(self):
        user_info=await self.user_info
        mode_id=self.get_argument('mode_id',default=None)
        mode = await self.db.mode.get_by_id(mode_id)
        if mode['type'] != 'vote':
            raise ResourceNotExistError('w')
        supportMap = mode['function']['supportMap']
        if mode['function']['typeAB']=='one':
            ntime=self.get_timestamp()
            if ntime > mode['beginTime'] and ntime < mode['endTime'] and str(user_info['_id']) not in mode['joinList']:
                hasVote = False
            else:
                hasVote= True
        else:
            if str(user_info['_id']) in supportMap.keys() and len(supportMap[str(user_info['_id'])]['voteList'])!=0:
                lastTime = supportMap[str(user_info['_id'])]['voteList'][-1]['time']
                ntime=self.get_timestamp()
                if ntime > mode['beginTime'] and ntime < mode['endTime'] and int(ntime/(3600*24))>int(lastTime/(3600*24)):
                    hasVote = False
                else:
                    hasVote=True
            elif str(user_info['_id']) not in supportMap.keys():
                hasVote=False
                await self.db.mode.update(mode_id,{'$set':{'function.supportMap.%s'%(str(user_info['_id'])):{'voteList':[]}}})
            else:
                hasVote=False
                
        voteNumMap = mode['function']['voteNumMap']
        for i in range(0,len(mode['function']['optList'])):
            mode['function']['optList'][i]['num']=voteNumMap[mode['function']['optList'][i]['feature']]
        mode={
            'beginTime':mode['beginTime'],
            'endTime':mode['endTime'],
            'title':mode['title'],
            'avatar':mode['avatar'],
            'content':mode['content'],
            'belongActivity':mode['belongActivity'],
            'state':mode['state'],
            'type':mode['type'],
            'joinNum':mode['function']['supportNum'],
            'function':{
                'optList':mode['function']['optList'],
                'hasVote':hasVote,
                'typeAB':mode['function']['typeAB'],
            }
        }
        self.finish_success(result=mode)
    """
        @api {post} /v1.0/mode/vote 获取圈子详情

        @apiGroup index
        @apiVersion  1.0.0
        @apiDescription 获取圈子详情

        @apiPermission user
        @apiParam    {string}    mode_id        圈子Id
        @apiParam    {string}    mtype        圈子Id
        @apiParam    {string}    feature        圈子Id
        @apiSuccess    {list}        mode        圈子详情
    """
    async def post(self):
        user_info=await self.user_info
        jsonObj=self.json_body
        mode_id=jsonObj['mode_id']
        mtype=jsonObj['mtype']
        feature=jsonObj['feature']
        mode = await self.db.mode.get_by_id(mode_id)
        ntime=self.get_timestamp()
        if mode['type'] != 'vote':
            raise ResourceNotExistError('w')
        supportMap = mode['function']['supportMap']
        if mode['function']['typeAB']=='one':
            ntime=self.get_timestamp()
            if ntime > mode['beginTime'] and ntime < mode['endTime'] and str(user_info['_id']) not in mode['joinList']:
                hasVote = False
            else:
                hasVote= True
        else:
            if str(user_info['_id']) in supportMap.keys() and len(supportMap[str(user_info['_id'])]['voteList'])!=0:
                lastTime = supportMap[str(user_info['_id'])]['voteList'][-1]['time']
                ntime=self.get_timestamp()
                if ntime > mode['beginTime'] and ntime < mode['endTime'] and int(ntime/(3600*24))>int(lastTime/(3600*24)):
                    hasVote = False
                else:
                    hasVote=True
            elif str(user_info['_id']) not in supportMap.keys():
                hasVote=False
                await self.db.mode.update(mode_id,{'$set':{'function.supportMap.%s'%(str(user_info['_id'])):{'voteList':[]}}})
            else:
                hasVote=False
        if hasVote == True:
            raise ResourceNotExistError('w')
        else:
            await self.db.mode.update(mode_id,
            {
                '$inc':{
                    'function.voteNumMap.%s'%(feature):1,'function.supportNum':1,
                },
                '$addToSet':{
                    'function.supportMap.%s.voteList'%(str(user_info['_id'])):{'feature':feature,'time':ntime},
                    'joinList':str(user_info['_id'])
                }
            })
        self.finish_success(result='OK')
        
class SeatModeHandler(BaseHandler):
    """
        @api {get} /v1.0/mode/seat 获取圈子详情

        @apiGroup index
        @apiVersion  1.0.0
        @apiDescription 获取圈子详情

        @apiPermission user
        @apiParam    {string}    mode_id    圈子Id
        @apiSuccess    {list}        mode        圈子详情
    """
    async def get(self):
        user_info=await self.user_info
        mode_id=self.get_argument('mode_id',default=None)
        mode = await self.db.mode.get_by_id(mode_id)
        if mode['type'] != 'seat':
            raise ResourceNotExistError('w')
        joinMap = mode['function']['joinMap']
        if str(user_info['_id']) in joinMap.keys():
            userBehave=mode['function']['joinMap'][str(user_info['_id'])]
        else:
            await self.db.mode.update(mode_id,{'$set':{'function.joinMap.%s'%(str(user_info['_id'])):{'chooseList':[]}}})
            userBehave={}

        mode={
            'beginTime':mode['beginTime'],
            'endTime':mode['endTime'],
            'title':mode['title'],
            'avatar':mode['avatar'],
            'content':mode['content'],
            'belongActivity':mode['belongActivity'],
            'state':mode['state'],
            'type':mode['type'],
            'joinNum':len(mode['joinList']),
            'function':{
                'seatStateList':mode['function']['seatStateList'],
                'HTmap':mode['function']['HTmap'],
                'hasJoin':str(user_info['_id']) in mode['function']['userList'],
                'userBehave':userBehave,
                'state':mode['state'],
            }
        }
        self.finish_success(result=mode)
    """
        @api {post} /v1.0/mode/seat 获取圈子详情

        @apiGroup index
        @apiVersion  1.0.0
        @apiDescription 获取圈子详情

        @apiPermission user
        @apiParam    {string}    mode_id        圈子Id
        @apiParam    {string}    mtype        圈子Id
        @apiParam    {string}    seatNumber    圈子Id
        @apiSuccess    {list}        mode        圈子详情
    """
    async def post(self):
        user_info=await self.user_info
        jsonObj=self.json_body
        mode_id=jsonObj['mode_id']
        mtype=jsonObj['mtype']
        seatNumber=int(jsonObj['seatNumber'])
        mode = await self.db.mode.get_by_id(mode_id)
        if mode['type'] != 'seat':
            raise ResourceNotExistError('w')
        ntime=self.get_timestamp()
        if mode['endTime']<ntime or mode['beginTime']>ntime:
            raise ResourceNotExistError('')
        if str(user_info['_id']) in mode['function']['userList']:
            raise ResourceNotExistError('')
        
        
        joinMap = mode['function']['joinMap']
        if str(user_info['_id']) not in joinMap.keys():
            await self.db.mode.update(mode_id,{'$set':{'function.joinMap.%s'%(str(user_info['_id'])):{'chooseList':[]}}}) 
            
            
        if mtype =='select':
            await self.db.mode.updateS(
            {'_id':ObjectId(mode_id),'function.userList':{'$ne':str(user_info['_id'])},'function.seatStateList.%d'%(seatNumber):0},
            {'$addToSet':{'joinList':str(user_info['_id']),'function.userList':str(user_info['_id']),'function.joinMap.%s.chooseList'%(str(user_info['_id'])):{'seatNumber':seatNumber,'type':mtype,'time':ntime}},'$set':{'function.seatStateList.%d'%(seatNumber):1,'function.seatUserList.%d'%(seatNumber):str(user_info['_id'])}}
            )
            mode = await self.db.mode.get_by_id(mode_id)
            if mode['function']['seatUserList'][seatNumber] == str(user_info['_id']):
                re="OK"
            else:
                re='NO'
        elif mtype =='reselect':
            await self.db.mode.updateS(
            {'_id':ObjectId(mode_id),'function.seatStateList.%d'%(seatNumber):1,'function.seatUserList.%d'%(seatNumber):str(user_info['_id'])},
            {'$addToSet':{'joinList':str(user_info['_id']),'function.joinMap.%s.chooseList'%(str(user_info['_id'])):{'seatNumber':seatNumber,'type':mtype,'time':ntime}},'$pull':{'function.userList':str(user_info['_id'])},'$set':{'function.seatStateList.%d'%(seatNumber):0,'function.seatUserList.%d'%(seatNumber):''}}
            )
            mode = await self.db.mode.get_by_id(mode_id)
            if mode['function']['seatUserList'][seatNumber] == str(user_info['_id']):
                re="NO"
            else:
                re='OK'
        self.finish_success(result=re)
routes.handlers += [
    (r'/v1.0/mode', ModeHandler),
    (r'/v1.0/mode/vote', VoteModeHandler),
    (r'/v1.0/mode/seat', SeatModeHandler),
]
