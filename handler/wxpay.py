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
from handler.unit.unit import produce_notice_system_tip
def parseWeixin(xmlstr, params):
    xmlstr = xmlstr[:5]+'\n'+xmlstr[5:]
    lines = xmlstr.split('\n')[1:-2]
    res = {}
    for line in lines:
        end = line.find('>')
        code = line[1:end]
        for key in params:
            if code == key:
                start = line.find('[CDATA[')
                end = line.find(']]><')
                value = line[start+7:end]
                res[key]=value
    return res

def wxSign(kv):
    stringA = ""
    for key, value in sorted(kv.items()):
        stringA +=(str(key)+"="+str(value)+"&")

    stringA +=("key="+config.wxpay_secretKey)
    sign  = hashlib.md5(stringA.encode()).hexdigest().upper()
    return sign

class WxpayHandler(BaseHandler):
    def id_generator(self,size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))
    def generateWXParam(self,openid,amount,order_number,event_title):
        kv = {}
        #date = datetime.datetime.now().strftime("%Y%m%d")
        #config.num += random.randint(10,1000)
        #mch_id = "1426868602"
        kv['appid'] = config.wxpay_appid
        kv['mch_id'] = config.wxpay_mch_id
        kv['nonce_str'] = self.id_generator(30)
        kv['body'] = "达人服务-"+event_title
        kv['out_trade_no'] = order_number
        kv['openid'] = openid
        kv['total_fee'] = amount
        kv['spbill_create_ip'] = config.wxpay_spbill_create_ip
        kv['notify_url'] = config.wxpay_notify_url
        kv['trade_type'] = config.wxpay_trade_type

        sign = wxSign(kv)
        kv['sign'] = sign
        strr= "<xml>\n"
        for (key, value) in kv.items():
            strr+=('<{}><![CDATA[{}]]></{}>\n'.format(key,  value,key))
        strr+="</xml>"
        print(strr)
        return strr
        
    async def getWxpayCode(self,s):
        url = config.wxpay_url
        strr = s
        request = HTTPRequest(
            url = url, 
            method = "POST", 
            body = strr,   
            client_key=config.wxpay_client_key,
            ca_certs=config.wxpay_ca_certs,  
            client_cert=config.wxpay_client_certs
        )
        client = AsyncHTTPClient()
        response = await client.fetch(request)
        print(response.body.decode('utf-8'))
        res = parseWeixin(response.body.decode('utf-8'),['result_code','return_code','prepay_id'])
        print(res)
        if res['return_code'] == 'SUCCESS' and res['result_code']=='SUCCESS' :
            return res['prepay_id']
        else :
            return None
                
    """
        @api {post} /v1.0/order/wxpay    微信支付下单
        @apiGroup order
        @apiVersion  1.0.0
        @apiDescription 微信支付下单
        @apiPermission user

        @apiParam    {string}    order_id    订单编号

        
        @apiSuccess    {string}    prepay_id    支付代码
    """
    async def post(self):

        print("/order/wxpay  --")
        user_info=await self.user_info
        order_id =self.json_body['order_id']
        order = await self.db.order.get_by_id(order_id)
        if order is None:
            raise ArgsError("Order_id err")
        if order['state'] !='nonpay':
            raise RelateResError("该订单已完成")
        if order['trainee'] != str(user_info['_id']):
            raise PermissionDeniedError("不是你的订单")
        print("make sttr")
        event = await self.db.event.get_by_id(order['belonged'])
        strr = self.generateWXParam(user_info['weixinopenid'],order['price'],order['orderNumber'],event['title'])
        prepay_id = await self.getWxpayCode(strr)
        if prepay_id is None:
            raise StateError("支付下单失败")
        #await self.db.order.update(order_id,{'ch_id':prepay_id})
        print(prepay_id)
        result = {}
        result['timeStamp'] = str(int(time.time()))
        result['nonceStr'] = self.id_generator(32)
        result['package'] = 'prepay_id='+prepay_id
        result['signType'] = 'MD5'
        result['appId'] = config.wxpay_appid
        result['paySign'] = wxSign(result)
        self.finish_success(result=result)
        
class WxReturnHandler(BaseHandler):
    """
        @api {post} /v1.0/order/wxpay/return    微信支付前端回调
        @apiGroup order
        @apiVersion  1.0.0
        @apiDescription 微信支付前端回调
        @apiPermission user

        @apiParam    {string}    order_id    订单编号
        @apiParam    {string}    result        'success'/'fail'
        
        @apiSuccess    {string}    result        'OK'
    """
    async def post(self):

        user_info=await self.user_info
        order_id = self.json_body['order_id']
        result = self.json_body['result']
        print(result)
        order = await self.db.order.get_by_id(order_id)
        if order is None:
            raise ArgsError("Order_id err")
        if order['state'] !='nonpay':
            self.finish_success(result='paid')
            return
        if order['trainee'] != str(user_info['_id']):
            raise PermissionDeniedError("不是你的订单")
        if result == 'success':
            await self.db.order.update(order_id,{'state':'paying'})
        print('fail ---')
        self.finish_success(result='OK')
        
class WxCallbackHandler(BaseHandler):
    """
        @api {post} /v1.0/order/wxpay/wx_callback    微信支付腾讯回调
        @apiGroup order
        @apiVersion  1.0.0
        @apiDescription 微信支付回调
        @apiPermission user

    """
    async def post(self):
        jsonObj = parseWeixin(self.request.body.decode('utf-8'),['result_code','return_code','time_end','out_trade_no'])
        print('wxpay/wx_callback')
        if jsonObj['return_code']=='SUCCESS' and jsonObj['result_code'] =='SUCCESS':
            order_number = jsonObj['out_trade_no']
            time_end = jsonObj['time_end']
            order = await self.db.order.get_by_orderNumber(order_number)
            print('find order')
            if order is None:
                self.finish_wx()
                return
            await self.db.order.update(order["_id"],{'state':'accpaid','payTime':self.get_timestamp(),'channel':'wx_lite_pay'})
            await self.db.master.add_money_by_user_id('order_money',order['master'],int(tip['price']))
            print('order update')
            self.finish_wx()
            return
        else:
            print('order fail')
            self.finish_wx(result=prepay_id)
    
    def finish_wx(self):
        self.finish('<xml><return_code><![CDATA[SUCCESS]]></return_code><return_msg><![CDATA[OK]]></return_msg></xml>')






class TipWxpayHandler(BaseHandler):
    def id_generator(self,size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))
    def generateWXParam(self,openid,amount,order_number,event_title):
        kv = {}
        #date = datetime.datetime.now().strftime("%Y%m%d")
        #config.num += random.randint(10,1000)
        #mch_id = "1426868602"
        kv['appid'] = config.wxpay_appid
        kv['mch_id'] = config.wxpay_mch_id
        kv['nonce_str'] = self.id_generator(30)
        kv['body'] = "打赏服务"+event_title
        kv['out_trade_no'] = order_number
        kv['openid'] = openid
        kv['total_fee'] = amount
        kv['spbill_create_ip'] = config.wxpay_spbill_create_ip
        kv['notify_url'] = config.wxpay_notify_url2
        kv['trade_type'] = config.wxpay_trade_type

        sign = wxSign(kv)
        kv['sign'] = sign
        strr= "<xml>\n"
        for (key, value) in kv.items():
            strr+=('<{}><![CDATA[{}]]></{}>\n'.format(key,  value,key))
        strr+="</xml>"
        #print(strr)
        return strr
        
    async def getWxpayCode(self,s):
        url = config.wxpay_url
        strr = s
        request = HTTPRequest(
            url = url, 
            method = "POST", 
            body = strr,   
            client_key=config.wxpay_client_key,
            ca_certs=config.wxpay_ca_certs,  
            client_cert=config.wxpay_client_certs
        )
        client = AsyncHTTPClient()
        response = await client.fetch(request)
        #print(response.body.decode('utf-8'))
        res = parseWeixin(response.body.decode('utf-8'),['result_code','return_code','prepay_id'])
        #print(res)
        if res['return_code'] == 'SUCCESS' and res['result_code']=='SUCCESS' :
            return res['prepay_id']
        else :
            return None
                
    """
        @api {post} /v1.0/tip/wxpay    微信打赏下单
        @apiGroup order
        @apiVersion  1.0.0
        @apiDescription 微信打赏下单
        @apiPermission user

        @apiParam    {string}    tip_id    订单编号

        
        @apiSuccess    {string}    prepay_id    支付代码
    """
    async def post(self):

        print("/tip/wxpay  --")
        user_info=await self.user_info
        tip_id =self.json_body['tip_id']
        tip = await self.db.tip.get_by_id(tip_id)
        print(tip)
        if tip is None:
            raise ArgsError("Order_id err")
        if str(tip['from_user']) != str(user_info['_id']):
            raise PermissionDeniedError("不是你的订单")
        print("make sttr")
        event = await self.db.event.get_by_id(tip['to_event_id'])
        strr = self.generateWXParam(user_info['weixinopenid'],int(tip['price']),tip['tipOrderNumber'],event['title'])
        prepay_id = await self.getWxpayCode(strr)
        if prepay_id is None:
            raise StateError("支付下单失败")
        #await self.db.order.update(order_id,{'ch_id':prepay_id})
        print(prepay_id)
        result = {}
        result['timeStamp'] = str(int(time.time()))
        result['nonceStr'] = self.id_generator(32)
        result['package'] = 'prepay_id='+prepay_id
        result['signType'] = 'MD5'
        result['appId'] = config.wxpay_appid
        result['paySign'] = wxSign(result)
        self.finish_success(result=result)
        
class TipWxReturnHandler(BaseHandler):
    """
        @api {post} /v1.0/tip/wxpay/return    微信支付前端回调
        @apiGroup order
        @apiVersion  1.0.0
        @apiDescription 微信支付前端回调
        @apiPermission user

        @apiParam    {string}    tip_id    订单编号
        @apiParam    {string}    result        'success'/'fail'
        
        @apiSuccess    {string}    result        'OK'
    """
    async def post(self):

        user_info=await self.user_info
        tip_id = self.json_body['tip_id']
        result = self.json_body['result']
        print(result)
        tip = await self.db.tip.get_by_id(tip_id)
        if tip is None:
            raise ArgsError("Tip_id err")
        if tip['state'] !='nonpay':
            self.finish_success(result='paid')
            return
        if str(tip['from_user']) != str(user_info['_id']):
            raise PermissionDeniedError("不是你的打赏")
        if result == 'success':
            await self.db.tip.update(tip_id,{'state':'paying'})
        self.finish_success(result='OK')
        
class TipWxCallbackHandler(BaseHandler):
    """
        @api {post} /v1.0/tip/wxpay/wx_callback    微信支付腾讯回调
        @apiGroup order
        @apiVersion  1.0.0
        @apiDescription 微信支付回调
        @apiPermission user

    """
    async def post(self):
        jsonObj = parseWeixin(self.request.body.decode('utf-8'),['result_code','return_code','time_end','out_trade_no'])
        print(jsonObj)
        print('wxpay/wx_callback')
        if jsonObj['return_code']=='SUCCESS' and jsonObj['result_code'] =='SUCCESS':
            order_number = jsonObj['out_trade_no']
            time_end = jsonObj['time_end']
            tip = await self.db.tip.get_by_orderNumber(order_number)
            print('find order')
            if tip is None:
                self.finish_wx()
                return
            await self.db.tip.update(tip["_id"],{'state':'accpaid','payTime':self.get_timestamp()})
            await self.db.master.add_money_by_user_id('tip_money',tip['to_user'],int(tip['price']))
            notice = produce_notice_system_tip('tip_finish',tip['to_user'],{'tipId':tip['_id']})
            notice_id = await self.db.notice.insert(notice)
            print('order update')
            self.finish_wx()
            return
        else:
            print('order fail')
            self.finish_wx(result=prepay_id)
    
    def finish_wx(self):
        self.finish('<xml><return_code><![CDATA[SUCCESS]]></return_code><return_msg><![CDATA[OK]]></return_msg></xml>')







routes.handlers += [
    (r'/v1.0/order/wxpay', WxpayHandler),
    (r'/v1.0/order/wxpay/return', WxReturnHandler),
    (r'/v1.0/order/wxpay/wx_callback', WxCallbackHandler),
    (r'/v1.0/tip/wxpay', TipWxpayHandler),
    (r'/v1.0/tip/wxpay/return', TipWxReturnHandler),
    (r'/v1.0/tip/wxpay/wx_callback', TipWxCallbackHandler),
]
