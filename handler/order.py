from handler.base import BaseHandler
import routes
from handler.exceptions import ResourceNotExistError,PermissionDeniedError,ArgsError,StateError,RelateResError
import pingpp
import config
import time
from ORM.MongoDB.base import ObjectId
pingpp.api_key=config.pingpp_test_key

#appointment_order_state={'nonpay','paying','accpaid','to_meet','to_evaluate','finish','off','refund'}
#order_state        ={'nonpay','paying','accpaid','to_meet','to_evaluate','finish','off','refund'}
#to_front_state     ={           'to_confirm','to_meet','to_evaluate','finish',      'refund'}


class OrderListNumberHandler(BaseHandler):
    """
        @api {get} /v1.0/orderlist_number 获取事件产生的订单数

        @apiGroup order
        @apiVersion  1.0.0
        @apiDescription 获取事件产生的订单数

        @apiPermission user
        @apiParam    {string}    event_id    事件ID
        @apiSuccess    {int}        list_number    订单数目
    """
    async def get(self):
        user_info = await self.user_info
        event_id=self.get_argument('event_id',default=None)
        num = await self.db.order.get_orderlist_length(str(event_id))
        self.finish_success(result=num)

class OrderOneHandler(BaseHandler):
    """
        @api {get} /v1.0/order 获取订单详情

        @apiGroup order
        @apiVersion  1.0.0
        @apiDescription 获取订单详情

        @apiPermission user
        @apiParam    {string}    order_id    订单ID
        @apiSuccess    {object}    order    订单
    """
    async def get(self):
        user_info=await self.user_info
        
        order_id=self.get_argument('order_id',default=None)
        
        order = await self.db.order.get_by_id(order_id)
        if order is None:
            raise ResourceNotExistError("订单不存在")
        if order['trainee'] !=str(user_info['_id']) and order['master'] !=str(user_info['_id']):
            raise PermissionDeniedError("并不是你的订单")
        
        event = self.db.event.brief_event(await self.db.event.get_by_id(order['belonged']))
        master = self.db.master.brief_master(await self.db.master.get_by_user(order['master']))

        #if order['state']=='nonpay' or order['state']=='paying':
        #    raise ResourceNotExistError("订单无法查看")

        #对完成支付的状态进行转换
        if order['state']=='accpaid':
            pass
            #order['state']='to_confirm'

        comment ={
            'star':[5.0,5.0,5.0],
            'content':'',
        }
        
        if 'comment_id' in order and order['comment_id']!='':
            one_comment = await self.db.comment.get_by_id(ObjectId(order['comment_id']))
            if one_comment:
                comment['star'] = one_comment['star']
                comment['content'] = one_comment['content']
                
        if event['coverPhoto'] != '':
            coverP = event['coverPhoto']
        else:
            coverP = event['photosDisplay'][0]
        trainee = await self.db.user.get_by_id(order['trainee'])
        orderDetail = {
                '_id':order['_id'],
                'orderNumber':order['orderNumber'],
                'eventCover':coverP,
                'eventTitle':event['title'],
                'eventId':event['_id'],
                'state':order['state'],
                'price':order['price'],
                'master':order['master'],
                'trainee':order['trainee'],
                'masterName':master['realName'],
                'masterCover':master['avatar'],
                'userName':trainee['realName'],
                'userAvatar':trainee['avatar'],
                
                'avatar':master['avatar'],
                'time':order['orderTime'],
                'realPhone':order['realPhone'],
                'remarkInfo':order['remarkInfo'],
                'realName':order['realName'],
                'identity':user_info['identity'],
                'university':user_info['university'],
                'campus':user_info['campus'],
                'comment':comment,
                'comment_id':order['comment_id'],
                'belongedType':order['belongedType'],
                'masterContact':master['masterContact'],
            }
        self.finish_success(result=orderDetail)
    
    """
        @api {post} /v1.0/order 完成订单相关操作

        @apiGroup order
        @apiVersion  1.0.0
        @apiDescription 完成订单相关操作

        @apiPermission user
        @apiParam    {string}    order_id    订单ID
        @apiSuccess    {object}    orderlist    获取订单列表
    """
    async def post(self):
        pass
        

class OrderUserHandler(BaseHandler):
    """
        @api {get} /v1.0/order/user 获取订单列表(用户)

        @apiGroup order
        @apiVersion  1.0.0
        @apiDescription 获取订单列表(用户)

        @apiPermission user
        @apiParam {string} pagesize    页大小
        @apiParam {string} time    页大小
        
        @apiSuccess    {object}    orderlist    获取订单列表
    """
    async def get(self):
        user_info=await self.user_info
        
        ntime=self.get_timestamp()
        pagesize=int(self.get_argument('pagesize',default=10))
        time=float(self.get_argument('time',default=ntime))
        
        condition={'trainee':str(user_info['_id']), 'orderTime':{'$lt':time}, 'state':{'$ne':'off'}}
        order_list = await self.db.order.get_order_free(condition, 'orderTime', '-', pagesize, 0)

        #将未完成支付的订单筛选出来，不显示
        orderlist = []
        for order in order_list:
            #if order['state']=='nonpay' or order['state']=='paying':
            #    pass
            #else:
            orderlist.append(order)

        only_need_number = self.get_argument('only_number', default=0);
        if int(only_need_number) == 1:
            self.finish_success(result=len(orderlist))
            return

        for i in range(0,len(orderlist)):
            #对完成支付的状态进行转换
            if orderlist[i]['state']=='accpaid':
                pass
                #orderlist[i]['state']='to_confirm'

            master = await self.db.master.get_by_user(orderlist[i]['master'])
            event = await self.db.event.get_by_id(orderlist[i]['belonged'])
            if event['coverPhoto'] != '':
                coverP = event['coverPhoto']
            else:
                coverP = event['photosDisplay'][0]
            orderlist[i]={
                '_id':orderlist[i]['_id'],
                'orderNumber':orderlist[i]['orderNumber'],
                'eventCover':coverP,
                'eventTitle':event['title'],
                'state':orderlist[i]['state'],
                'price':orderlist[i]['price'],
                'masterName':master['realName'],
                'masterCover':master['avatar'],
                'time':orderlist[i]['orderTime'],
                'belongedType':orderlist[i]['belongedType'],
                'avatar':master['avatar'],
            }
        self.finish_success(result=orderlist)
        pass
    """
        @api {post} /v1.0/order/user 创建订单

        @apiGroup order
        @apiVersion  1.0.0
        @apiDescription 创建订单

        @apiPermission user
        @apiParam    {string}    event_id    事件Id
        @apiParam    {string}    remarkInfo    备注
        @apiParam    {string}    realName    真实姓名
        @apiParam    {string}    realPhone    联系电话

        @apiSuccess    {string}    order_id    订单ID
    """
    async def post(self):
        user_info=await self.user_info
        event_id = self.json_body['event_id']
        jsonObj=self.json_body
        
        event = await self.db.event.get_by_id(event_id)
        if event is None:
            raise ArgsError('belonged??')
        orderNumber=self.produce_order_number()
        order_src={
            'orderNumber':orderNumber,
            'orderTime':self.get_timestamp(),
            #'payTime':'',
            #'refundTime':'',
            #'finishedTime':'',
            'belongedType':event['type'],
            'belonged':event_id,
            'trainee':str(user_info['_id']),
            'master':event['belongedMaster'],
            'price':int(float(event['price'])*100),
            'state':'nonpay',
            'remarkInfo':jsonObj['remarkInfo'],
            'realName':jsonObj['realName'],
            'realPhone':jsonObj['realPhone']
        }
        
        order_dst=self.db.base.dict_match(order_src,self.db.base.get_order_default())
        order_id=await self.db.order.insert(order_dst)
        
        self.finish_success(result=order_id)
        pass

    """
        @api {put} /v1.0/order/user 用户对订单进行评价

        @apiGroup order
        @apiVersion  1.0.0
        @apiDescription 用户对订单进行评价

        @apiPermission user

        @apiParam    {string}    order_id    订单id

        @apiSuccess {string}     result      'ok'/'fail'
    """
    async def put(self):
        user_info = await self.user_info
        jsonObj = self.json_body
        order = await self.db.order.get_by_id(jsonObj['order_id'])
        if order:
            if order['state']=='to_evaluate':
                await self.db.order.update(jsonObj['order_id'],{'state':'finish'})
                self.finish_success(result='ok')
            else:
                self.finish_success(result='fail')
        else:
            self.finish_success(result='fail')
    
    """
        @api {delete} /v1.0/order/user 取消订单

        @apiGroup order
        @apiVersion  1.0.0
        @apiDescription 取消订单

        @apiPermission user
        @apiParam    {string}    order_id    订单id        
        @apiSuccess    {string}    result 'OK'    
    """
    async def delete(self):
        user_info=await self.user_info
        json = self.json_body
        order_id = json['order_id']
        order = await self.db.order.get_by_id(order_id)
        if order is None:
            raise ResourceNotExistError("订单不存在")
        if order['state']!='nonpay':
            raise StateError("该订单不可取消")
        await self.db.order.update(jsonObj['order_id'],{'state':'off'})
        self.finish_success(result='OK')
        pass


class OrderMasterHandler(BaseHandler):    
    """
        @api {get} /v1.0/order/master 获取订单列表(达人)

        @apiGroup order
        @apiVersion  1.0.0
        @apiDescription 获取订单列表(达人)

        @apiPermission master

        @apiParam {string} pagesize    页大小
        @apiParam {string} time    页大小
        @apiSuccess    {object}    orderlist        获取订单列表
    """
    async def get(self):
        user_info=await self.user_info
        ntime=self.get_timestamp()
        pagesize=int(self.get_argument('pagesize',default=10))
        time=float(self.get_argument('time',default=ntime))
        master = await self.db.master.get_by_user(str(user_info['_id']))
        if master:
            condition={'master':str(master['userId']),'orderTime':{'$lt':time},'state':{'$ne':'off'}}
            order_list = await self.db.order.get_order_free(
                condition=condition,sortby='orderTime',sort='-'
                )

            #将未完成支付的订单筛选出来，不显示
            orderlist = []
            for order in order_list:
                if order['state']=='nonpay' or order['state']=='paying':
                    pass
                else:
                    orderlist.append(order)

            only_need_number = self.get_argument('only_number', default=0);
            if int(only_need_number) == 1:
                self.finish_success(result=len(orderlist))
                return

            for i in range(0,len(orderlist)):
                #对完成支付的状态进行转换
                if orderlist[i]['state']=='accpaid':
                    pass
                    #orderlist[i]['state']='to_confirm'

                master = await self.db.master.get_by_user(orderlist[i]['master'])
                user = await self.db.user.get_by_id(ObjectId(orderlist[i]['trainee']))
                event = await self.db.event.get_by_id(orderlist[i]['belonged'])
                orderlist[i]={
                    '_id':orderlist[i]['_id'],
                    'orderNumber':orderlist[i]['orderNumber'],
                    'eventCover':event['coverPhoto'],
                    'eventTitle':event['title'],
                    'state':orderlist[i]['state'],
                    'price':orderlist[i]['price'],
                    'masterName':master['realName'],
                    'masterCover':master['avatar'],
                    'avatar':master['avatar'],
                    'time':orderlist[i]['orderTime'],
                    'belongedType':orderlist[i]['belongedType'],
                    'userName':user['realName'],
                    'userAvatar':user['avatar'],
                    'userUniversity':user['university'],
                    'usercampus':user['campus'],
                    
                }
            self.finish_success(result=orderlist)
        else:
            raise PermissionDeniedError("不是达人")
    """
        @api {post} /v1.0/order/master 同意约见

        @apiGroup order
        @apiVersion  1.0.0
        @apiDescription 同意订单约见

        @apiPermission master

        @apiParam   {string}    order_id    订单id     

        @apiSuccess {string}    result 'ok' 
    """
    async def post(self):
        user_info=await self.user_info
        master = await self.db.master.get_by_user(user_info['_id'])
        if master:
            json = self.json_body
            order_id = json['order_id']
            order = await self.db.order.get_by_id(order_id)
            if order is None:
                raise ResourceNotExistError("订单不存在")
            elif order['state']=='accpaid':
                #给达人记录现金收益
                await self.db.master.add_money_by_user_id(user_info['_id'],order['price'])
                #完成约见订单
                await self.db.order.update(order_id,{'state':'to_meet'})
            self.finish_success(result='ok')
        else:
            raise PermissionDeniedError("不是达人")

    """
        @api {put} /v1.0/order/master 达人确认完成线下约见

        @apiGroup order
        @apiVersion  1.0.0
        @apiDescription 达人确认完成线下约见

        @apiPermission master
    
        @apiParam   {string}    order_id    订单id     
    
        @apiSuccess {string}    result 'ok' 
    """
    async def put(self):
        user_info=await self.user_info
        json = self.json_body
        master = await self.db.master.get_by_user(user_info['_id'])
        if master:
            order_id = json['order_id']
            order = await self.db.order.get_by_id(order_id)
            if order is None:
                raise ResourceNotExistError("订单不存在")
            elif order['state']=='to_meet':
                await self.db.order.update(order_id,{'state':'to_evaluate'})
            self.finish_success(result='ok')
        else:
            raise PermissionDeniedError("不是达人")
        
routes.handlers += [
    (r'/v1.0/order/list_number',OrderListNumberHandler),
    (r'/v1.0/order', OrderOneHandler),
    (r'/v1.0/order/user', OrderUserHandler),
    (r'/v1.0/order/master',OrderMasterHandler),
]    
