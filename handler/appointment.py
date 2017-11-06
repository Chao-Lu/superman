from handler.base import BaseHandler
import routes
from handler.exceptions import ResourceNotExistError,PermissionDeniedError,ArgsError,StateError,RelateResError
import config
import time
from handler.unit.unit import produce_notice_system_appointment
from handler.unit.yunpian import tpl_send_sigle_sms

#appointment_order_state={'nonpay','paying','accpaid','to_meet','to_evaluate','finish','off','refund'}
#order_state            ={'nonpay','paying','accpaid','to_meet','to_evaluate','finish','off','refund'}
#to_front_state         ={               'to_confirm','to_meet','to_evaluate','finish',      'refund'}

class AppointmentUser(BaseHandler):
    """
        @api {post} /v1.0/appointment/user 创建约见订单

        @apiGroup appointment
        @apiVersion  1.0.0
        @apiDescription 创建约见订单

        @apiPermission user
        @apiParam   {string}    event_id    事件Id
        @apiParam   {string}    remarkInfo  备注
        @apiParam   {string}    realName    真实姓名
        @apiParam   {string}    realPhone   联系电话

        @apiSuccess {string}    order_id    订单ID
    """
    async def post(self):
        price = 10
        

        print(self.request.headers['Access_token'])
        user_info=await self.user_info
        event_id = self.json_body['event_id']
        jsonObj=self.json_body
        event = await self.db.event.get_by_id(event_id)
        if event is None:
            raise ArgsError('belonged??')
        reamin_vcoin = await self.db.user.get_vcoin_number(user_info['_id'])
        if price > reamin_vcoin:
            raise ArgsError('not sfficient vcoins!!')
            return
        #创建约见订单成功则减少虚拟币
        await self.db.user.reduce_vcoin_number(user_info['_id'],price)
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
            'price':price,
            'state':'accpaid',
            'remarkInfo':jsonObj['remarkInfo'],
            'realName':jsonObj['realName'],
            'realPhone':jsonObj['realPhone']
        }
        
        order_dst=self.db.base.dict_match(order_src,self.db.base.get_order_default())
        order_id=await self.db.order.insert(order_dst)
        await self.db.user.insert_order(user_info['_id'],str(order_id))
        notice = produce_notice_system_appointment('order_request',event['belongedMaster'],{'orderId':str(order_id)})
        notice_id = await self.db.notice.insert(notice)
        self.finish_success(result=order_id)
        pass

    """
        @api {put} /v1.0/appointment/user 用户对约见进行评价

        @apiGroup appointment
        @apiVersion  1.0.0
        @apiDescription 用户对约见进行评价

        @apiPermission user
        @apiParam   {string}    order_id    订单id
        @apiParam   {string}    commentType 
        @apiParam {object}    comment     评论        
        @apiParam (comment)   {string}    content
        @apiParam (comment)   {array}     star    [4.5,4.5,4.5]
        @apiParam (comment)   {string}    multiMedia 
        
        
        @apiSuccess {string}    result      'ok'／'fail'
    """
    async def put(self):
        user_info = await self.user_info
        jsonObj = self.json_body
        order = await self.db.order.get_by_id(jsonObj['order_id'])
        comment = jsonObj['comment']
        comment_src={
            'commenter':str(user_info['_id']),
            'commentType':jsonObj['commentType'],
            'postId':order['belonged'],
            'commentTime':self.get_timestamp(),
            'content':comment['content'],
            'star':[float(comment['star'][0]),float(comment['star'][1]),float(comment['star'][2])],
            'multiMedia':comment['multiMedia'],
            'replyList':[],
            'likeUserList':[],
            'state':'on',
            'orderId':str(jsonObj['order_id']),
        }
        comment_dst=self.db.base.dict_match(comment_src,self.db.base.get_comment_default())
        
        if order:
            if order['state']=='to_evaluate':
                comment_id = await self.db.comment.insert(comment_dst)
                await self.db.order.update(jsonObj['order_id'],{'state':'finish','comment_id':comment_id})
                notice = produce_notice_system_appointment('order_comment',order['master'],{'orderId':str(order['_id'])})
                notice_id = await self.db.notice.insert(notice)
                
                self.finish_success(result='ok')
            else:
                self.finish_success(result='fail1')
        else:
            self.finish_success(result='fail2')

    """
        @api {delete} /v1.0/appointment/user 用户取消约见订单

        @apiGroup appointment
        @apiVersion  1.0.0
        @apiDescription 用户取消约见订单

        @apiPermission user
        
        @apiParam   {string}    order_id    订单id     
        
        @apiSuccess {string}    result 'ok'/'fail' 
    """
    async def delete(self):
        user_info=await self.user_info
        json = self.json_body
        order_id = json['order_id']
        order = await self.db.order.get_by_id(order_id)
        if order is None:
            raise ResourceNotExistError("订单不存在")
        elif order['state']=='accpaid':
            #将虚拟币返回给用户
            await self.db.user.add_vcoin_number(order['trainee'],order['price'])
            await self.db.order.update(order_id,{'state':'off'})
        elif order['state']=='to_meet':
            #进入退款状态
            await self.db.order.update(order_id,{'state':'refund'})
        elif order['state']=='to_evaluate':
            self.finish_success(result='fail')
        else:
            self.finish_success(result='fail')


class AppointmentRefund(BaseHandler):
    """
        @api {post} /v1.0/appointment/refund 达人对用户取消约见订单的行为进行确认

        @apiGroup appointment
        @apiVersion  1.0.0
        @apiDescription 达人对用户取消约见订单的行为进行确认

        @apiPermission master
        
        @apiParam   {string}    order_id    订单id     
        
        @apiSuccess {string}    result 'ok'/'fail' 
    """
    async def post(self):
        user_info = await self.user_info
        master = await self.db.master.get_by_user(user_info['_id'])
        if master:
            jsonObj = self.json_body
            order = await self.db.order.get_by_id(jsonObj['order_id'])
            if order:
                if order['state']=='accpaid':
                    await self.db.order.update(order_id,{'state':'off'})
                    await self.db.user.add_vcoin_number(order['trainee'],order['price'])
                    await self.db.user.reduce_vcoin_number(master['_id'],order['price'])
                    self.finish_success(result='ok')
                else:
                    self.finish_success(result='fail')
            else:
                self.finish_success(result='fail')

        else:
            raise PermissionDeniedError("不是达人")


class AppointmentMaster(BaseHandler):    
    """
        @api {post} /v1.0/appointment/master 同意约见

        @apiGroup appointment
        @apiVersion  1.0.0
        @apiDescription 同意约见

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
                #将虚拟币返转给达人
                await self.db.user.add_vcoin_number(user_info['_id'],order['price'])
                #完成约见订单
                await self.db.order.update(order_id,{'state':'to_meet'})
                notice = produce_notice_system_appointment('order_accept',order['trainee'],{'orderId':str(order_id)})
                notice_id = await self.db.notice.insert(notice)
                trainee = await self.db.user.get_by_id(order['trainee'])
                appointment = await self.db.event.get_by_id(order['belonged'])
                await tpl_send_sigle_sms(1818646,{'#userName#':trainee['realName'],'#masterName#':user_info['realName'],'#appointment_title#':"'%s'"%appointment['title']},order['realPhone'])
            self.finish_success(result='ok')
        else:
            raise PermissionDeniedError("不是达人")

    """
        @api {put} /v1.0/appointment/master 达人确认完成线下约见

        @apiGroup appointment
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
                notice = produce_notice_system_appointment('order_finish',order['trainee'],{'orderId':str(order_id)})
                notice_id = await self.db.notice.insert(notice)
            self.finish_success(result='ok')
        else:
            raise PermissionDeniedError("不是达人")


    """
        @api {delete} /v1.0/appointment/master 达人拒绝约见

        @apiGroup appointment
        @apiVersion  1.0.0
        @apiDescription 达人拒绝约见

        @apiPermission master
        
        @apiParam   {string}    order_id    订单id     
        
        @apiSuccess {string}    result 'ok' 
    """
    async def delete(self):
        user_info=await self.user_info
        json = self.json_body
        master = await self.db.master.get_by_user(user_info['_id'])
        if master:
            order_id = json['order_id']
            order = await self.db.order.get_by_id(order_id)
            if order is None:
                raise ResourceNotExistError("订单不存在")
            elif order['state']=='accpaid':
                #将虚拟币返回给用户
                await self.db.user.add_vcoin_number(order['trainee'],order['price'])
                #关闭约见订单
                await self.db.order.update(order_id,{'state':'off'})
            self.finish_success(result='ok')
        else:
            raise PermissionDeniedError("不是达人")
class AppointmentCommentHandler(BaseHandler):
    """
        @api {get} /v1.0/appointment/comment 达人拒绝约见

        @apiGroup appointment
        @apiVersion  1.0.0
        @apiDescription 达人拒绝约见

        @apiPermission master
        @apiParam {string}  pagesize    页大小
        @apiParam {string}  time    页大小
        @apiParam   {string}    appointment_id    订单id     
        
        @apiSuccess {string}    result 'ok' 
    """

    async def get(self):
        user_info=await self.user_info
        ntime=self.get_timestamp()
        pagesize=int(self.get_argument('pagesize',default=10))
        time=float(self.get_argument('time',default=ntime))
        appointment_id = self.get_argument('appointment_id',default=None)
        condition = {'state':'on','commentTime':{'$lt':time},'commentType':'appointment','postId':appointment_id}
        commentlist = await self.db.comment.get_comment_free(condition,'commentTime','-',pagesize,0)
        for i in range(0,len(commentlist)):
            comment =     commentlist[i]
            comment['commenter'] = self.db.user.brief_user(await self.db.user.get_by_id(comment['commenter']))
            comment['event'] = await self.db.event.get_by_id(comment['postId'])
            comment['event']['belongedMaster'] = self.db.master.brief_master(await self.db.master.get_by_user(comment['event']['belongedMaster']))
            commentlist[i] = comment
        self.finish_success(result=commentlist)
        pass

            
routes.handlers += [
    (r'/v1.0/appointment/user', AppointmentUser),
    (r'/v1.0/appointment/master', AppointmentMaster),
    (r'/v1.0/appointment/refund',AppointmentRefund),
    (r'/v1.0/appointment/comment',AppointmentCommentHandler),
]   
