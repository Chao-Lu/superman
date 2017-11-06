from sdk import top
import sdk.top.api
import json

class AliSendCodeMsg(object):
    def __init__(self, ak, sk):
        self.req = top.api.OpenSmsSendvercodeRequest(domain='http://gw.api.taobao.com')
        self.req.set_app_info(top.appinfo(ak, sk))

    async def send_code(self, mobile, domain="vercode"):
        values = {'mobile': str(mobile), 'domain': domain}
        jdata = json.dumps(values)
        self.req.send_ver_code_request = jdata
        result = await self.req.getResponse()
        self.success = result['open_sms_sendvercode_response']['result']['successful']
        self.message = result['open_sms_sendvercode_response']['result']['message']

class AliCheckCodeMsg(object):
    def __init__(self, ak, sk):
        self.req = top.api.OpenSmsCheckvercodeRequest(domain='http://gw.api.taobao.com')
        self.req.set_app_info(top.appinfo(ak, sk))

    async def check_code(self, mobile, ver_code, domain="vercode"):
        values = {'mobile': str(mobile), 'ver_code': str(ver_code), 'domain': domain}
        jdata = json.dumps(values)
        self.req.check_ver_code_request = jdata
        result = await self.req.getResponse()
        self.success = result['open_sms_checkvercode_response']['result']['successful']
        self.message = result['open_sms_checkvercode_response']['result']['message']

class AliSendMsg(object):
    def __init__(self, ak, sk):
        self.req = top.api.OpenSmsSendmsgRequest(domain='http://gw.api.taobao.com')
        self.req.set_app_info(top.appinfo(ak, sk))

    async def ban_user_msg(self, mobile, ban):
        if ban:
            context = "【达人荟】抱歉，您的达人主页暂时被禁，详情请联系达人荟客服"
        else:
            context = "【达人荟】您好，您的达人主页已被解禁，可以继续正常使用" 
        values = {'mobile': str(mobile), 'context': context}
        jdata = json.dumps(values)
        self.req.send_ver_code_request = jdata
        result = await self.req.getResponse()
        self.success = result['open_sms_sendvercode_response']['result']['successful']
        self.message = result['open_sms_sendvercode_response']['result']['message']

    async def send_msg(self, mobile, context):
        values = {'mobile': str(mobile), 'context': context}
        jdata = json.dumps(values)
        self.req.send_ver_code_request = jdata
        result = await self.req.getResponse()
        self.success = result['open_sms_sendvercode_response']['result']['successful']
        self.message = result['open_sms_sendvercode_response']['result']['message']


