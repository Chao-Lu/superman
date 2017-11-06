from handler.base import BaseHandler
import routes
import json
from handler.exceptions import ResourceNotExistError,PermissionDeniedError,ArgsError,StateError,RelateResError
class uUserTeamHandler(BaseHandler):
    """
        @api {get} /v1.0/manager/userTeam/user 获取用户所属用户组 
        @apiGroup user
        @apiVersion  1.0.0
        @apiPermission user
        @apiDescription 获取用户所属用户组

        @apiParam    {Object}    user_id    用户id
        @apiSuccess    {string}    result "OK"    
    """
    async def get(self):
        self.prehandle()
        user_info=await self.user_info
        #print(user_info)
        if not self.is_manager(user_info['masterId']):
            raise PermissionDeniedError("需要管理员用户")
        user_id=self.get_argument("user_id",default=None)
        user_info=await self.db.user.get_by_id(user_id)
        userTeam={}
        if 'userTeam' not in user_info.keys() or user_info['userTeam'] == '':
            isleader='null'
        else:
            userteam=await self.db.userteam.get_by_id(user['userTeam'])
            if str(user['_id'])== userTeam['teamLeader']    :
                isleader='yes'
            else:
                isleader='no'
            teamLeader_token = await self.db.token.get_by_user(userTeam['teamLeader'])
            teamLeader_info = await self.db.user.get_by_id(userTeam['teamLeader'])
            userTeam['teamLeader']={
                'token':teamLeader_token['token'],
                'userId':userTeam['teamLeader'],
                'realName':teamLeader_info['realName'],
                'avatar':teamLeader_info['avatar'],
            }
            for i in range(0,len(userTeam['teamMember'])):
                member_id=userTeam['teamMember'][i]
                member_token = await self.db.token.get_by_user(member_id)
                member_info = await self.db.master.get_by_user(member_id)
                member={
                    'token':member_token['token'],
                    'userId':member_id,
                    'realName':member_info['realName'],
                    'avatar':member_info['avatar'],
                }
                userTeam['teamMember'][i]=member
        self.finish_success(result={'isleader':isleader,'userTeam':userTeam})
    """
        @api {put} /v1.0/manager/userTeam/user 修改用户的Member身份(可否为Member)
        @apiGroup user
        @apiVersion  1.0.0
        @apiPermission user
        @apiDescription 修改用户的Member身份

        @apiParam    {Object}    user_id    用户id
        @apiParam    {Object}    mtype    ('Member'/'noMember')    
        
        @apiSuccess    {string}    result "OK"    
    """
    async def put(self):
        self.prehandle()
        user_info=await self.user_info
        #print(user_info)
        if not self.is_manager(user_info['masterId']):
            raise PermissionDeniedError("需要管理员用户")
        user_id=self.get_argument("user_id",default=None)
        mtype=self.get_argument("mtype",default=None)
        user=await self.db.user.get_by_id(user_id)
        if not self.is_master(user['masterId']):
            raise StateError('需要为达人')
        if mtype == 'Member':
            await self.db.user.update(user_id,{'userType':'member'})
        if mtype == 'noMember':
            await self.db.user.update(user_id,{'userType':'user'})
        self.finish_success(result='OK')
class UserTeamHandler(BaseHandler):
    """
        @api {get} /v1.0/manager/userTeam 获取用户组 
        @apiGroup user
        @apiVersion  1.0.0
        @apiPermission user
        @apiDescription 获取用户组

        @apiParam    {Object}    userTeam_id    用户组id
        @apiSuccess    {string}    result "OK"    
    """
    async def get(self):
        self.prehandle()
        user_info=await self.user_info
        #print(user_info)
        if not self.is_manager(user_info['masterId']):
            raise PermissionDeniedError("需要管理员用户")
        userTeam_id=self.get_argument("userTeam_id",default=None)
        userTeam=await self.db.userteam.get_by_id(userTeam_id)
        if userTeam['teamLeader']=='':
            pass 
        else:
            teamLeader_info = await self.db.user.get_by_id(userTeam['teamLeader'])
            userTeam['teamLeader']={
                'userId':userTeam['teamLeader'],
                'realName':teamLeader_info['realName'],
                'avatar':teamLeader_info['avatar'],
            }
        for i in range(0,len(userTeam['teamMember'])):
            member_id=userTeam['teamMember'][i]
            member_info = await self.db.master.get_by_user(member_id)
            member={
                'userId':member_id,
                'realName':member_info['realName'],
                'avatar':member_info['avatar'],
            }
            userTeam['teamMember'][i]=member
        self.finish_success(result={'userTeam':userTeam})

    """
        @api {post} /v1.0/manager/userTeam 创建用户组 
        @apiGroup user
        @apiVersion  1.0.0
        @apiPermission user
        @apiDescription 创建用户组
        @apiSuccess    {string}    userTeam_id 用户组id    
    """
    async def post(self):
        self.prehandle()
        user_info=await self.user_info
        #print(user_info)
        if not self.is_manager(user_info['masterId']):
            raise PermissionDeniedError("需要管理员用户")
        userTeam=self.db.base.get_userteam_default()
        userTeam_id=await self.db.userteam.insert(userTeam)

        self.finish_success(result=userTeam_id)
        
    """
        @api {put} /v1.0/manager/userTeam 修改用户组信息 
        @apiGroup user
        @apiVersion  1.0.0
        @apiPermission user
        @apiDescription 修改用户组信息
        @apiParam    {Object}    userTeam_id    用户组id
        @apiParam    {Object}    user_id    用户id        
        @apiParam    {Object}    mtype    操作类型    ('insertMember'/'insertLeader'/'removeMember'/'removeLeader'/)    
        
        @apiSuccess    {string}    result "OK"    
    """
    async def put(self):
        self.prehandle()
        user_info=await self.user_info
        #print(user_info)
        if not self.is_manager(user_info['masterId']):
            raise PermissionDeniedError("需要管理员用户")
        userTeam_id=self.get_argument("userTeam_id",default=None)
        userteam=await self.db.userteam.get_by_id(userTeam_id)
        user_id=self.get_argument("user_id",default=None)
        mtype=self.get_argument("mtype",default=None)
        user = await self.db.user.get_by_id(user_id)
        if mtype == 'insertMember':
            if user['userTeam'] !='':
                raise StateError('已有小组')
            if user['userType'] !='member':
                raise StateError('不是Member')
            await self.db.userteam.insert_member(userTeam_id,str(user['_id']))
            await self.db.user.update(user['_id'],{'userTeam':str(userTeam_id)})
        if mtype == 'insertLeader':
            if user['userTeam'] !='':
                raise StateError('已有小组')
            if userteam['teamLeader'] !='':
                raise StateError('已有teamLeader')
            if user['userType'] =='Member' or user['weixinopenid'] =='':
                raise StateError('是Member或无主用户')
            await self.db.userteam.update(userTeam_id,{'teamLeader':str(user['_id'])})
            await self.db.user.update(user['_id'],{'userTeam':str(userTeam_id)})
        if mtype == 'removeMember':
            if user['userTeam'] =='':
                raise StateError('无小组')
            await self.db.userteam.remove_member(userTeam_id,str(user['_id']))
            await self.db.user.update(user['_id'],{'userTeam':''})
        if mtype == 'removeLeader':
            if user['userTeam'] =='':
                raise StateError('无小组')
            if userteam['teamLeader'] !=str(user['_id']):
                raise StateError('不是teamLeader')
            await self.db.userteam.update(userTeam_id,{'teamLeader':''})
            await self.db.user.update(user['_id'],{'userTeam':''})

        self.finish_success(result='OK')
class uUserTeamMemberHandler(BaseHandler):
    """
        @api {get} /v1.0/manager/userTeam/member 获取所有member用户
        @apiGroup user
        @apiVersion  1.0.0
        @apiPermission user
        @apiDescription 获取用户所属用户组
        @apiParam    {string}    condition    
        @apiParam    {string}    sortby
        @apiParam    {string}    sort
        @apiParam    {string}    limit
        @apiParam    {string}    skip
        @apiSuccess    {string}    memberlist "OK"    
    """
    async def get(self):
        self.prehandle()
        user_info=await self.user_info
        #print(user_info)
        if not self.is_manager(user_info['masterId']):
            raise PermissionDeniedError("需要管理员用户")
        condition = json.loads(self.get_argument('condition',default='{}'))
        sortby = str(self.get_argument('sortby',default='_id'))
        sort = str(self.get_argument('sort',default='+'))
        limit = int(self.get_argument('limit',default=1000))
        skip = int(self.get_argument('skip',default=0))
        
        memberlist = await self.db.user.get_user_free(condition,sortby,sort,limit,skip)
        for i in range(0,len(memberlist)):
            memberlist[i]={
                '_id':memberlist[i]['_id'],
                'realName':memberlist[i]['realName'],
                'avatar':memberlist[i]['avatar'],
                'gender':memberlist[i]['gender'],
                'university':memberlist[i]['university'],
                'campus':memberlist[i]['campus'],
                'realIdentity':memberlist[i]['realIdentity'],
                'masterId':memberlist[i]['masterId'],
                'userTeam':memberlist[i]['userTeam'],
                'coverPhoto':memberlist[i]['coverPhoto'],
                'userType':memberlist[i]['userType'],
            }

        self.finish_success(result=memberlist)
    """
        @api {put} /v1.0/manager/userTeam/member 创建member用户
        @apiGroup user
        @apiVersion  1.0.0
        @apiPermission user
        @apiDescription 创建member用户

        @apiParam    {Object}    user    用户信息
        
        @apiSuccess    {string}    result "OK"    
    """
    async def post(self):
        self.prehandle()
        user_info=await self.user_info
        #print(user_info)
        if not self.is_manager(user_info['masterId']):
            raise PermissionDeniedError("需要管理员用户")
        user_id=self.get_argument("user_id",default=None)
        user_json=self.json_body['user']
        user_src=self.db.base.dict_match(user_json,
            {
                'phoneNumber':'',
                'realName':'',
                'avatar':'',
                'university':'',
                'campus':'',
                'realIdentity':'',
                'certificationInfo':'',
                'coverPhoto':'',
                'location':'',
                'category':'',
                'realTitle':'',
                'personalDetails':'',
            }
        )
        user_info={
            'phoneNumber':user_src['phoneNumber'],
            'realName':user_src['realName'],
            'avatar':user_src['avatar'],
            'university':user_src['university'],
            'campus':user_src['campus'],
            'realIdentity':user_src['realIdentity'],
            'certificationInfo':user_src['certificationInfo'],
            'entryDate':self.get_timestamp(),
            'isNew':'NO',
            'coverPhoto':user_src['coverPhoto'],
            'userType':'member',
        }
        user_id=await self.insert_new_user(user_info)
        master_info={
            'userId':str(user_id), 
            'state':'off',
            'realName':user_src['realName'],
            'avatar':user_src['avatar'],
            'coverPhoto':user_src['coverPhoto'],
            'location':user_src['location'],
            'category':user_src['category'],
            'realTitle':user_src['realTitle'],
            'personalDetails':user_src['personalDetails'],
            'entryDate':self.get_timestamp(),
            'phone':user_src['phoneNumber'],
            'certificationInfo':user_src['certificationInfo'],
        }
        master_id=await self.db.master.insert(
            self.db.base.dict_match(
                master_info,
                self.db.base.get_master_default()
                )
            )
        await self.db.user.update(user_id,{'masterId':str(master_id)})
        self.finish_success(result=user_id)
routes.handlers += [
    (r'/v1.0/manager/userTeam', UserTeamHandler),
    (r'/v1.0/manager/userTeam/user', uUserTeamHandler),
    (r'/v1.0/manager/userTeam/member', uUserTeamMemberHandler),
]
