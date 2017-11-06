from handler.base import BaseHandler
import routes
import json
import config
from handler.exceptions import ResourceNotExistError,PermissionDeniedError,ArgsError,StateError,RelateResError
import string
import random
import hashlib
from tornado.web import RequestHandler
from tornado.httpclient import HTTPRequest, AsyncHTTPClient
import time
def wxSign(kv):
    stringA = ""
    for key, value in sorted(kv.items()):
        stringA +=(str(key)+"="+str(value)+"&")

    stringA +=("key="+config.wxpay_secretKey)
    sign  = hashlib.md5(stringA.encode()).hexdigest().upper()
    return sign
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
class sOrderAllHandler(BaseHandler):    

    """
        @api {get} /v1.0/manager/order/all 获取订单列表
        @apiGroup manager
        @apiVersion  1.0.0
        @apiDescription 获取订单列表

        @apiPermission manager
        
        @apiParam    {string}    condition    
        @apiParam    {string}    sortby
        @apiParam    {string}    sort
        @apiParam    {string}    limit
        @apiParam    {string}    skip
        
        @apiSuccess    {Object}    orderlist    订单信息
    """
    async def get(self):
        self.prehandle()
        user_info=await self.user_info
        if not self.is_manager(user_info['masterId']):
            raise PermissionDeniedError("需要管理员用户")
        condition = json.loads(self.get_argument('condition',default='{}'))
        sortby = str(self.get_argument('sortby',default='_id'))
        sort = str(self.get_argument('sort',default='-'))
        limit = int(self.get_argument('limit',default=1000))
        skip = int(self.get_argument('skip',default=0))
        
        orderlist = await self.db.order.get_order_free(condition,sortby,sort,limit,skip)
        for i in range(0,len(orderlist)):
            master = await self.db.master.get_by_user(orderlist[i]['master'])
            event = await self.db.event.get_by_id(orderlist[i]['belonged'])
            user = await self.db.user.get_by_id(orderlist[i]['trainee'])
            orderlist[i]['master']=master
            orderlist[i]['belonged']=event
            orderlist[i]['trainee']=user
        orderlist.reverse()
        self.finish_success(result=orderlist)
        pass

class sOrderOneHandler(BaseHandler):    

    """
        @api {get} /v1.0/manager/order 获取订单信息
        @apiGroup manager
        @apiVersion  1.0.0
        @apiDescription 获取订单信息

        @apiPermission manager
        
        @apiParam    {string}    order_id    订单ID
        
        @apiSuccess    {Object}    order    订单信息
    """
    async def get(self):
        self.prehandle()
        user_info=await self.user_info

        if not self.is_manager(user_info['masterId']):
            raise PermissionDeniedError("需要管理员用户")
        order_id = self.get_argument('order_id',default=None)
        order = await self.db.order.get_by_id(order_id)
        if order is None:
            raise ArgsError("order_id??")
        self.finish_success(result=order)
        pass
    """
        @api {post} /v1.0/manager/order 完成订单
        @apiGroup manager
        @apiVersion  1.0.0
        @apiDescription 完成订单

        @apiPermission manager
        
        @apiParam    {string}    order_id    订单ID
        
        @apiSuccess    {Object}    result    'OK'
    """
    async def post(self):
        self.prehandle()
        user_info=await self.user_info

        if not self.is_manager(user_info['masterId']):
            raise PermissionDeniedError("需要管理员用户")
        order_id = self.get_argument('order_id',default=None)
        order = await self.db.order.get_by_id(order_id)
        if order is None:
            raise ArgsError("order_id??")
        if order['state']!='accpaid':
            raise StateError('订单不可完成')
        await self.db.order.update(order_id,{'state':'complete','finishTime':self.get_timestamp()})
        self.finish_success(result='ok')
        pass
    """
        @api {put} /v1.0/manager/order 支付订单(临时)
        @apiGroup manager
        @apiVersion  1.0.0
        @apiDescription 支付订单

        @apiPermission manager
        
        @apiParam    {string}    order_id    订单ID
        
        @apiSuccess    {Object}    result    'OK'
    """
    async def put(self):
        self.prehandle()
        user_info=await self.user_info

        if not self.is_manager(user_info['masterId']):
            raise PermissionDeniedError("需要管理员用户")
        order_id = self.get_argument('order_id',default=None)
        order = await self.db.order.get_by_id(order_id)
        if order is None:
            raise ArgsError("order_id??")

        await self.db.order.update(order_id,{'state':'accpaid'})
        self.finish_success(result='ok')
        pass
    async def delete(self):
        self.prehandle()
        user_info=await self.user_info

        if not self.is_manager(user_info['masterId']):
            raise PermissionDeniedError("需要管理员用户")
        order_id = self.get_argument('order_id',default=None)
        order = await self.db.order.get_by_id(order_id)
        if order is None:
            raise ArgsError("order_id??")
        if order['removed'] == 'yes':
            await self.db.order.update(order_id,{'removed':'no'})
        else:
            await self.db.order.update(order_id,{'removed':'yes'})
        self.finish_success(result='ok')
        pass
class OrderRedfundHandler(BaseHandler):
    def id_generator(self,size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))
    def generateWXParam(self,total_amount,refund_amount,order_number,refund_number):
        kv = {}
        #date = datetime.datetime.now().strftime("%Y%m%d")
        #config.num += random.randint(10,1000)
        #mch_id = "1426868602"
        kv['appid'] = config.wxpay_appid
        kv['mch_id'] = config.wxpay_mch_id
        kv['nonce_str'] = self.id_generator(30)

        kv['out_trade_no'] = order_number
        kv['out_refund_no'] = refund_number

        kv['total_fee'] = total_amount
        kv['refund_fee'] = refund_amount
        kv['op_user_id'] = config.wxpay_mch_id

        sign = wxSign(kv)
        kv['sign'] = sign
        strr= "<xml>\n"
        for (key, value) in kv.items():
            strr+=('<{}><![CDATA[{}]]></{}>\n'.format(key,  value,key))
        strr+="</xml>"
        print(strr)
        return strr
        
    async def WxpayRefund(self,s):
        url = config.wxpay_refund_url
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
        res = parseWeixin(response.body.decode('utf-8'),['result_code','return_code'])
        print(res)
        if res['return_code'] == 'SUCCESS' and res['result_code']=='SUCCESS' :
            return True
        else :
            return False

    """
        @api {post} /v1.0/manager/order/refund 订单退款
        @apiGroup manager
        @apiVersion  1.0.0
        @apiDescription 订单退款

        @apiPermission manager
        
        @apiParam    {string}    order_id    订单ID
        
        @apiSuccess    {string}    result "OK"
    """
    async def post(self):
        self.prehandle()
        user_info=await self.user_info

        if not self.is_manager(user_info['masterId']):
            raise PermissionDeniedError("需要管理员用户")
        order_id = self.json_body['order_id']
        order = await self.db.order.get_by_id(order_id)
        if order is None:
            raise ArgsError("order_id??")


        if order['state'] not in ['accpaid','complete'] :
            raise StateError('订单不可退款')
        else:
            refund_number=self.produce_order_number()
            strr=self.generateWXParam(order['price'],order['price'],order['orderNumber'],refund_number)
            if await self.WxpayRefund(strr):
                await self.db.order.update(order_id, {'state':'refund','refundNumber':refund_number})
                self.finish_success(result='OK')
        raise ArgsError("order_id??")

routes.handlers += [
    (r'/v1.0/manager/order/all', sOrderAllHandler),
    (r'/v1.0/manager/order', sOrderOneHandler),
    (r'/v1.0/manager/order/refund', OrderRedfundHandler),
]
