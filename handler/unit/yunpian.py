


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
    
async def send_single_sms( text, mobile):
    """通用接口发短信"""
    apikey = yunpian_apikey
    params = urllib.parse.urlencode({'apikey':apikey,'text':text,'mobile':mobile})
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = http.client.HTTPSConnection(sms_host, port=port, timeout=30)
    conn.request("POST", sms_single_send_uri, params, headers)
    response = conn.getresponse()
    response_str = response.read()
    conn.close()
async def tpl_send_sigle_sms( tpl_id, tpl_value, mobile):
    """模板接口发送短信"""
    apikey = yunpian_apikey
    params = urllib.parse.urlencode({'apikey':apikey,'tpl_id':tpl_id,'tpl_value':urllib.parse.urlencode(tpl_value),'mobile':mobile})
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    #使用长连接
    conn = http.client.HTTPSConnection(sms_host, port=port, timeout=30)
    conn.request("POST", sms_tpl_single_send_uri, params, headers)
    response = conn.getresponse()
    response_str = response.read()
    conn.close()

