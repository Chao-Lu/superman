from handler.base import BaseHandler
import routes
from handler.exceptions import ResourceNotExistError,PermissionDeniedError,ArgsError,StateError,RelateResError
import random
import hashlib
from tornado.web import RequestHandler
import config
import string
from tornado.httpclient import HTTPRequest, AsyncHTTPClient
import time
import http
import urllib
import json
import random
import re

sms_host = config.yp_sms_host
port = config.yp_port
version = config.yp_version

sms_single_send_uri = config.yp_sms_single_send_uri
sms_tpl_single_send_uri = config.yp_sms_tpl_single_send_uri

yunpian_apikey = config.yp_yunpian_apikey

def generate_code(len):
    code_str = ''
    for i in range(0,len):
        code_str += str(random.randint(0,9))
    return code_str

class SendCodeHandler(BaseHandler):
    async def send_single_sms(self, apikey, text, mobile):
        """通用接口发短信"""
        params = urllib.parse.urlencode({'apikey':apikey,'text':text,'mobile':mobile})
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        conn = http.client.HTTPSConnection(sms_host, port=port, timeout=30)
        conn.request("POST", sms_single_send_uri, params, headers)
        response = conn.getresponse()
        response_str = response.read()
        conn.close()

    async def tpl_send_sigle_sms(self, apikey, tpl_id, tpl_value, mobile):
        """模板接口发送短信"""
        params = urllib.parse.urlencode({'apikey':apikey,'tpl_id':tpl_id,'tpl_value':urllib.parse.urlencode(tpl_value),'mobile':mobile})
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        #使用长连接
        conn = http.client.HTTPSConnection(sms_host, port=port, timeout=30)
        conn.request("POST", sms_tpl_single_send_uri, params, headers)
        response = conn.getresponse()
        response_str = response.read()
        conn.close()

    async def post(self):
        """
        @api {get} /v1.0/phone/sendcode 
        @apiGroup sendcode
        @apiVersion  1.0.0
        @apiDescription 发送短信验证码
        @apiPermission user

        @apiParam    {string}    mobile    手机号
        """
        json = self.json_body    
        mobile = json['mobile']
        p2=re.compile('^0\d{2,3}\d{7,8}$|^1\d{10}$')
        phonematch=p2.match(mobile)
        if not phonematch:
            self.finish_err(result='手机号码格式错误')
            return
        code = await self.db.code.get_by_mobile(mobile)
        if code:
            '''验证码超时'''
            if time.time()-code['time']>300:
                pass
            #'''5分钟内不需要重复发送验证码'''
            else:
                self.finish_err(result='5分钟内不需要重复发送验证码')
                return 

        code_str = generate_code(4)
        generate_time = time.time()
        await self.db.code.delete(mobile)
        #await self.db.code.update(mobile,{'state':'off'})
        await self.db.code.insert(mobile, code_str, generate_time)
        tpl_id = 1
        tpl_value = {'#code#':code_str,'#company#':'达人荟'}
        await self.tpl_send_sigle_sms(yunpian_apikey, tpl_id, tpl_value, mobile)

class CheckCodeHandler(BaseHandler):
    async def post(self):
        """
        @api {get} /v1.0/phone/checkcode 
        @apiGroup sendcode
        @apiVersion  1.0.0
        @apiDescription 发送短信验证码
        @apiPermission user

        @apiParam    {string}    mobile    手机号
        @apiParam    {string}    code_str    验证码

        @apiSuccess    {boolean}    confirmed    验证通过True/False
        @apiSuccess {string}    text         错误描述
        """
        json = self.json_body    
        mobile = json['mobile']
        p2=re.compile('^0\d{2,3}\d{7,8}$|^1\d{10}$')
        mobilematch=p2.match(mobile)
        if not mobilematch:
            self.finish_err(result='手机号码格式错误')
            return
        code_str = json['code_str']
        code = await self.db.code.get_by_mobile(mobile)
        if code:
            if code['code_str'] == code_str:
                if code['time']+300<time.time():
                    """验证码超时"""
                    self.finish_success(result={'confirmed':False,'text':'验证码超时'})
                else:
                    """验证成功，将手机号插入用户信息中"""
                    await self.db.code.delete(mobile)
                    #await self.db.code.update(mobile,{'state':'off'})
                    user_info = await self.user_info
                    await self.db.user.update_phone(user_info['_id'],mobile)
                    self.finish_success(result={'confirmed':True,'text':'验证成功，手机号绑定成功'})
            else:
                self.finish_success(result={'confirmed':False,'text':'验证码错误'})
        else:
            self.finish_success(result={'confirmed':False,'text':'尚未获得验证码'})



routes.handlers += [
    (r'/v1.0/phone/sendcode',SendCodeHandler),
    (r'/v1.0/phone/checkcode',CheckCodeHandler)
]
