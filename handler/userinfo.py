from handler.base import BaseHandler
import routes
from tornado.httpclient import AsyncHTTPClient,HTTPError,HTTPRequest
import json
import time
import config
from handler.unit.unit import ObjectId
from handler.exceptions import ResourceNotExistError,PermissionDeniedError,ArgsError,StateError,RelateResError
class UserHandler(BaseHandler):    
    """
        @api {get} /v1.0/user 获取用户信息
        @apiGroup user
        @apiVersion  1.0.0
        @apiDescription 获取用户信息
        @apiPermission user
        
        @apiSuccess    {Object}    user    用户信息
    """
    async def get(self):
        user_info = await self.user_info
        user_info['orderNum'] = len(user_info['userOrders'])
        user_info['favorEventNum'] = len(user_info['userFavorTeam'])

        self.finish_success(result=user_info)
        pass
class testhandler(BaseHandler):
    def get(self):
        self.finish_success(result="OK")
class UserUpdateLabelHandler(BaseHandler):
    """
        @api {put} /v1.0/user/update/label 更新个人信息
        @apiGroup user
        @apiVersion  1.0.0
        @apiDescription 更新用户信息
        @apiPermission user
        
        @apiParam    {Object}    user    用户信息
        
        @apiSuccess    {string}    result "OK"
    """
    async def put(self):
        user_info=await self.user_info
        user_id=str(user_info['_id'])
        jsonObj= self.json_body
        #可更新内容列表
        Update_module={
            'labelList':[],
        }

        user_default = self.db.base.dict_match(user_info,Update_module)
        user_info=self.db.base.dict_match(
            jsonObj['user'],
            user_default
        )
        await self.db.user.update(user_id,user_info)
        condition= {'$or':[]}
        for _id in jsonObj['user']['labelList']:
            condition['$or'].append({'_id':ObjectId(_id)})
        await self.db.label.updateS(condition,{'$addtoSet':{'userList':str(user_info['_id'])}})
        self.finish_success(result="OK")

class UserUpdateHandler(BaseHandler):
    """
        @api {put} /v1.0/user/update/userinfo 更新个人信息
        @apiGroup user
        @apiVersion  1.0.0
        @apiDescription 更新用户信息
        @apiPermission user
        
        @apiParam    {Object}    user    用户信息
        
        @apiSuccess    {string}    result "OK"
    """
    async def put(self):
        user_info=await self.user_info
        user_id=str(user_info['_id'])
        jsonObj= self.json_body
        #可更新内容列表
        Update_module={
            #'phoneNumber':'',
            #'password':'',
            #'weixinopenid':'',
            'realName':'',
            'avatar':'',
            'gender':'',
            'university':'',
            'campus':'',
            'realIdentity':'',
            'certificationInfo':'',
            'identity':'',
            'campus':'',
            'location':'',
            'coverPhoto':'',
            #'masterId':'',
            #'userOrders':[],
            #'userBalance':[],
            #'userNotification':[]
            'isNew':'NO',
            'labelList':[],
        }

        user_default = self.db.base.dict_match(user_info,Update_module)
        user_info=self.db.base.dict_match(
            jsonObj['user'],
            user_default
        )
        if 'realName' in jsonObj['user'].keys() and 'avatar' in jsonObj['user'].keys() and len(jsonObj['user'].keys()) ==2:
            pass
        else:
            user_info['isNew']='NO'
        await self.db.user.update(user_id,user_info)
        user = await self.db.user.get_by_id(user_id)
        await self.db.user.update(user_id,user_info)

        if 'labelList' in jsonObj['user'].keys() and  jsonObj['user']['labelList']!=[]:

            condition= {'$or':[]}
            for _id in jsonObj['user']['labelList']:
                condition['$or'].append({'_id':ObjectId(_id)})
            await self.db.label.updateS(condition,{'$addToSet':{'userList':str(user_id)}})    
        if self.is_master(user['masterId']) == True:
            await self.db.master.update(user['masterId'],{
                'realName':user['realName'],
                'avatar':user['avatar'],
                'certificationInfo':user['certificationInfo'],
                'coverPhoto':user['coverPhoto'],
            })
        self.finish_success(result="OK")
        

    
class UserUppasswordHandler(BaseHandler):
    """
        @api {put} /v1.0/user/update/password 更新password
        @apiGroup user
        @apiVersion  1.0.0
        @apiDescription 更新password
        @apiPermission user
        
        @apiParam    {string}    Opassword    旧password
        @apiParam    {string}    Npassword    新password
        
        @apiSuccess    {string}    result "OK"
    """
    async def put(self):
        user_info=await self.user_info

        user_id=user_info['_id']
        json=self.json_body
        if json['Opassword']!=user_info['password']:
            raise RelateResError('旧密码错误')
        await self.db.user.update(user_id,{'password':json['Npassword']})
        self.finish_success(result="OK")

class RegisterTokenHandler(BaseHandler):
    """
        @api {post} /v1.0/user/register 用户注册
        @apiGroup user
        @apiVersion  1.0.0
        @apiDescription 用户注册

        @apiPermission all

        @apiParam    {string}    phone        手机号
        @apiParam    {string}    password    密码
        @apiParam    {string}    code        验证码
        
        @apiSuccess    {object}    utoken    用户登陆token
        
        @apiSuccess    (token)        {string}    userId
        @apiSuccess    (token)        {string}    accessToken
        @apiSuccess    (token)        {string}    accessTime
    """
    async def post(self):
        # 获取参数

        json = self.json_body
        phone = json["phone"]
        code = json["code"]
        password = json['password']
        
        #if not await self.AliCheckCode(phone,code):
        #    self.finish_err(result='验证码错误')
        #    return
            
        user=await self.db.user.get_by_phone(phone)

        if user is not None:
            self.finish_err(result='用户名已注册')
            return
        user_info={
            'phoneNumber':phone,
            'password':password,
            'entryDate':self.get_timestamp()
        }
        user_id = await self.insert_new_user(user_info)
        
        if user_id is None:
            self.finish_err(result='未知错误(注册错误)')
            return
        

        utoken = await self.db.token.get_by_user(user_id)
        if utoken is None:
            utoken=self.db.base.dict_match(
                {
                    'userId':user_id,
                    'accessToken':self.db.token.produce_token(),
                    'accessTime':self.get_timestamp()
                },
                self.db.base.get_token_default()
                )
            token_id = await self.db.token.insert(utoken)
            if token_id is None:
                self.finish_err()
                return
        self.finish_success(result=utoken)


class UserLoginHandler(BaseHandler):
    """
        @api {post} /v1.0/user/login 微信登陆
        @apiGroup user
        @apiVersion  1.0.0
        @apiDescription 微信登陆

        @apiPermission all

        @apiParam    {string}    code        手机号

        
        @apiSuccess    {object}    utoken    用户登陆token
        @apiSuccess    {string}    new        是否新用户
        @apiSuccess    (token)        {string}    userId
        @apiSuccess    (token)        {string}    accessToken
        @apiSuccess    (token)        {string}    accessTime
    """

    async def post(self):
        json_str = self.json_body
        code = json_str["code"]

        # 跟微信交互通过code拿到openid
        appid = config.wxlite_appid
        secret = config.wxlite_secret
        url = "https://api.weixin.qq.com/sns/jscode2session?appid={0}&secret={1}&js_code={2}&grant_type=authorization_code".format(appid,secret,code)

                
        http_client = AsyncHTTPClient()
        response = await http_client.fetch(url)
        response = json.loads(response.body.decode('utf-8'))
        openId=response['openid']
        user = await self.db.user.get_by_openid(openId)
        if user is None:
            user_info={
                        'weixinopenid':openId,
                        'entryDate':self.get_timestamp()
            }
            user_dst=self.db.base.dict_match(user_info,self.db.base.get_oridinaryUser_default())
            user_id = await self.insert_new_user(user_dst)

            
        else:
            user_id = user['_id']
            
        utoken =await self.produce_accessToken(user_id)
        user = await self.db.user.get_by_id(user_id)

        ismaster = self.is_master(user['masterId'])
        user_default=self.db.base.get_oridinaryUser_default()
        if user['phoneNumber']==user_default['phoneNumber'] :
            phone='no'
        else:
            phone='yes'
        issupervise = await self.is_supervise(user['_id'])
        if 'userTeam' not in user.keys() or user['userTeam']=='':
            isleader='null'
        else:
            userTeam=await self.db.userteam.get_by_id(user['userTeam'])
            if str(user['_id'])== userTeam['teamLeader']    :
                isleader='yes'
            else:
                isleader='no'
        if 'labelList' not in user.keys() or user['labelList']==[]:
            haveLabel='no'
        else:    
            haveLabel='yes'
        self.finish_success(result={'utoken':utoken,'new':user['isNew'],'location':user['university'],'issupervise':issupervise, 'ismaster':ismaster,'phone':phone,'isleader':isleader,'haveLabel':haveLabel})
        
class ManagerLoginHandler(BaseHandler):
    async def post(self):
        self.prehandle()
        json_str = self.json_body
        name = json_str["realName"]
        password = json_str['password']

        user = await self.db.user.get_manager_user()
        if user is None:
            user_info={
                        'masterId':config.MANAGER_ID,  
                        'realName':name,
                        'password':password
            }
            user_dst=self.db.base.dict_match(user_info,self.db.base.get_oridinaryUser_default())
            user_id = await self.insert_new_user(user_dst)
        else:
            if name==user['realName'] and password==user['password']:
                user_id = user['_id']
            else:
                print(name, password)
                self.finish_err()
                return
        utoken = await self.db.token.get_by_user(user_id)
        if utoken is None:
            utoken=self.db.base.dict_match(
                {
                    'userId':user_id,
                    'accessToken':self.db.token.produce_token(),
                    'accessTime':self.get_timestamp()
                },
                self.db.base.get_token_default()
                )
            token_id = await self.db.token.insert(utoken)
            if token_id is None:
                print("this question")
                self.finish_err()
                return

        self.finish_success(result={'utoken':utoken})
routes.handlers += [
    (r'/v1.0/test',testhandler),
    (r'/v1.0/user', UserHandler),
    (r'/v1.0/user/update/userinfo', UserUpdateHandler),
    (r'/v1.0/user/update/password', UserUppasswordHandler),
    (r'/v1.0/user/register', RegisterTokenHandler),
    (r'/v1.0/user/manager/login', ManagerLoginHandler),
    (r'/v1.0/user/login', UserLoginHandler),
]
