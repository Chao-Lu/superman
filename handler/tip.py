from handler.base import BaseHandler
import routes
import time
from handler.exceptions import ResourceNotExistError,PermissionDeniedError,ArgsError,StateError,RelateResError

class ListNumberTip(BaseHandler):
    """
        @api {get} /v1.0/tip/list_number 获取打赏用户数

        @apiGroup tip
        @apiVersion  1.0.0
        @apiDescription 获取打赏用户数

        @apiPermission user

        @apiSuccess {int}   list_number 打赏用户数目
        
    """
    async def get(self):
        user_info = await self.user_info
        tip_list = await self.db.tip.find_by_to_user_id(user_info['_id'])
        user_list = []
        for tip in tip_list:
            user_list.append(tip['from_user'])

        list_number = len(user_list)
        self.finish_success(result = list_number)

class ListTip(BaseHandler):
    """
        @api {get} /v1.0/tip/list 获取打赏用户列表

        @apiGroup tip
        @apiVersion  1.0.0
        @apiDescription 获取打赏用户列表

        @apiPermission user
        @apiParam   {string}    event_id    事件id


        @apiSuccess {Object}      user_list    打赏用户
        @apiSuccess (user_list)   {list}  user_id_list         打赏的用户id
        @apiSuccess (user_list)   {list}  user_avatar_list     打赏用户头像  
        @apiSuccess (user_list)   {int}   list_number          打赏订单数目
    """
    async def get(self):
        user_info = await self.user_info
        jsonObj = self.json_body

        tip_list = await self.db.tip.find_by_to_event_id(jsonObj['event_id'])
        user_id_list = []
        #打赏多次就显示多次吧，哈哈哈哈哈哈哈哈哈哈
        for tip in tip_list:
            user_id_list.append(tip['from_user'])

        user_avatar_list = []
        for one_user_id in user_id_list:
            user = await self.db.user.get_by_id(one_user_id)
            user_avatar_list.append(user['avatar'])

        list_number = len(user_id_list)
        user_list = {
            'user_id_list':user_id_list,
            'user_avatar_list':user_avatar_list,
            'list_number':list_number,
        }
        self.finish_success(result = user_list)

class Tip(BaseHandler):

    """
        @api {post} /v1.0/tip 插入一张打赏订单

        @apiGroup tip
        @apiVersion  1.0.0
        @apiDescription 插入一张打赏订单

        @apiPermission user
        
        @apiParam   {string}    to_user_id
        @apiParam   {string}    event_id
        @apiParam   {string}    order_id  
        @apiParam   {string}    price  

        @apiSuccess {string}   tip_order_id          打赏订单id
    """
    async def post(self):
        user_info = await self.user_info
        jsonObj = self.json_body
        tipOrderNumber=self.produce_order_number()

        tip_order_src = {
            'tipOrderNumber':tipOrderNumber,
            'tipOrderTime':time.time(),
            'payTime':'',
            'to_user':jsonObj['to_user_id'],
            'from_user':user_info['_id'],
            'price':int(jsonObj['price']*100),
            'order_id':jsonObj['order_id'],
            'state':'nonpay',
            'to_event_id':str(jsonObj['event_id']),
        }
        
        tip_order_dst=self.db.base.dict_match(tip_order_src,self.db.base.get_tip_order_default())
        tip_order_id=await self.db.tip.insert(tip_order_dst)
        print(tip_order_id)
        self.finish_success(result=tip_order_id)
        pass

routes.handlers += [
    (r'/v1.0/tip/list_number',ListNumberTip),
    (r'/v1.0/tip/list', ListTip),
    (r'/v1.0/tip', Tip),
]   

        






