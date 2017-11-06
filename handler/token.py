# coding=utf-8
import hashlib
import uuid
import config
import json
import re
from sdk.alimsg import AliSendCodeMsg, AliCheckCodeMsg
from datetime import datetime, timedelta
from tornado.escape import json_decode
from tornado.gen import coroutine
from tornado.httpclient import AsyncHTTPClient, HTTPRequest
from handler.base import BaseHandler
import routes
import time
from handler.exceptions import ResourceNotExistError,PermissionDeniedError,ArgsError,StateError,RelateResError
class CodeSenderHandler(BaseHandler):
    """
        @api {post} /v1.0/token/smscode 发送短信验证码
        @apiGroup token
        @apiVersion  1.0.0
        @apiDescription 发送短信验证码
        @apiPermission all
        
        @apiParam    {string}    phone    手机号
        
        @apiSuccess    {string}    result "OK"
        @apiError    {string}    message
    """
    async def post(self):
        phone = self.get_argument('phone')
        p2=re.compile('^0\d{2,3}\d{7,8}$|^1[358]\d{9}$|^147\d{8}')
        phonematch=p2.match(phone)
        if not phonematch:
            self.finish_err(result='手机号码格式错误')
            return
        AliSendCode = AliSendCodeMsg(config.ALIBAICHUAN_KEY, config.ALIBAICHUAN_SECRET)
        await AliSendCode.send_code(mobile=phone)
        if AliSendCode.success:
            self.finish_success(result='OK')
        else:
            self.finish_success(result=AliSendCode.message, code=400)
class AccessTokenHandler(BaseHandler):
    """
        @api {post} /v1.0/token/access 获取access token
        @apiGroup token
        @apiVersion  1.0.0
        @apiDescription 获取access token
        @apiPermission all
        
        @apiParam    {string}    phone        手机号
        @apiParam    {string}    password    密码
        
        @apiSuccess    {Object}    token
        @apiSuccess    (token)        {string}    userId
        @apiSuccess    (token)        {string}    accessToken
        @apiSuccess    (token)        {string}    accessTime
    """
    async def post(self):
        phone = self.get_argument("phone")
        password = self.get_argument("password")
        user= await self.db.user.check_password(phone,password)
        if user is None:
            raise RelateResError('用户不存在或密码错误')

        token = self.db.token.produce_token()
        await self.db.token.delete_by_user(user['_id'])
        utoken=self.db.base.dict_match(
            {
            'user':user['_id'],
            'token':token,
            'time':datetime.now()
            },
            self.db.base.get_token_default()
            )
        if utoken is None:
            raise StateError('未知登陆错误')
        await self.db.token.add(utoken)
        self.finish_success(result=utoken)
    """
        @api {delete} /v1.0/token/access 注销access token
        @apiGroup token
        @apiVersion  1.0.0
        @apiDescription 注销access token
        @apiPermission user
        
        @apiSuccess    {string}    result "OK"
    """
    async def delete(self):
        user_info=await self.user_info
        await self.db.token.delete_by_user(user_info['_id'])
        self.finish_success(result="OK")
        
        
routes.handlers += [
    (r'/v1.0/token/smscode', CodeSenderHandler),
    (r'/v1.0/token/access', AccessTokenHandler),
]
