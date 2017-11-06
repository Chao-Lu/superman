from handler.base import BaseHandler
import routes
from handler.exceptions import ResourceNotExistError,PermissionDeniedError,ArgsError,StateError,RelateResError

class NoticeholderHandler(BaseHandler):
    async def get_notice_info(self,notice):
        if notice['type'] == 'system' and notice['unit'] == 'appointment':
            return await self.get_notice_system_appointment(notice)
        
        elif notice['type'] == 'system' and notice['unit'] == 'tip':
            return await self.get_notice_system_tip(notice)
        return None
        pass
    async def get_notice_system_tip(self,notice):
        tip = await self.db.tip.get_by_id(notice['content']['tipId'])
        user_info = await self.db.user.get_by_id(tip['from_user'])
        appointment = await self.db.event.get_by_id(tip['to_event_id'])
        order = await self.db.order.get_by_id(tip['order_id'])
        master_info = await self.db.master.get_by_user(order['master'])
        appointment = {
            '_id':appointment['_id'],
            'coverPhoto':appointment['coverPhoto'],
            'title':appointment['title'],
            'realName':master_info['realName'],
            'realTitle':master_info['realTitle'],
        }
        order = {
            '_id':order['_id'],
            'orderNumber':order['orderNumber'],
            'remarkInfo':order['remarkInfo'],
            'realName':order['realName'],
            'realPhone':order['realPhone'],
            'price':order['price'],
            'orderType':order['belongedType'],
        }
        user_info = {
            '_id':user_info['_id'],
            'avatar':user_info['avatar'],
            'realName':user_info['realName'],
        }
        if notice['topic'] == 'tip_finish':
            content = {
                'appointment':appointment,
                'order':order,
                'producer_info':user_info,
                'title':'您收到了打赏%s元'%str(float(tip['price'])/100)
            }
        notice['content'] = content
        return notice
    async def get_notice_system_appointment(self,notice):
        order = await self.db.order.get_by_id(notice['content']['orderId'])
        appointment = await self.db.event.get_by_id(order['belonged'])
        user_info = await self.db.user.get_by_id(order['trainee'])
        master_info = await self.db.master.get_by_user(order['master'])
        if order['comment_id'] != '':
            comment = await self.db.comment.get_by_id(order['comment_id'])
        appointment = {
            '_id':appointment['_id'],
            'coverPhoto':appointment['coverPhoto'],
            'title':appointment['title'],
            'realName':master_info['realName'],
            'realTitle':master_info['realTitle'],
        }
        order = {
            '_id':order['_id'],
            'orderNumber':order['orderNumber'],
            'remarkInfo':order['remarkInfo'],
            'realName':order['realName'],
            'realPhone':order['realPhone'],
            'price':order['price'],
            'orderType':order['belongedType'],
        }
        user_info = {
            '_id':user_info['_id'],
            'avatar':user_info['avatar'],
            'realName':user_info['realName'],
        }
        master_info = {
            '_id':master_info['_id'],
            'avatar':master_info['avatar'],
            'realName':master_info['realName'],
            'contact':master_info['contact'],
        }
        if notice['topic'] == 'order_request':
            content = {
                'appointment':appointment,
                'order':order,
                'producer_info':user_info,
                'title':'用户请求约见'
            }
        elif notice['topic'] == 'order_accept':
            content = {
                'appointment':appointment,
                'order':order,
                'producer_info':master_info,
                'title':'达人接受了你的约见请求'
            }
        elif notice['topic'] == 'order_finish':
            content = {
                'appointment':appointment,
                'order':order,
                'producer_info':master_info,
                'title':'约见已完成'
            }
        elif notice['topic'] == 'order_comment':
            content = {
                'appointment':appointment,
                'producer_info':user_info,
                'comment':comment,
                'order':order,
                'title':'用户完成了对你的评价'
            }
        else:
            return None
        notice['content'] = content
        return notice
    """
        @api {get} /v1.0/noticeholder 获取通知列表

        @apiGroup notice
        @apiVersion  1.0.0
        @apiDescription 获取通知列表

        @apiPermission user
        
        @apiParam    {string}    type    info/list/num
        
        @apiParam    {string}    time    页码
        @apiParam    {string}    pagesize    页大小
        
        @apiSuccess    {list}    cardlist    卡片列表
    """
    async def get(self):
        user_info=await self.user_info

        ntime=self.get_timestamp()
        typ = self.get_argument('type',default=None)
        if typ == 'list':
            time=float(self.get_argument('time',default=ntime))
            pagesize=int(self.get_argument('pagesize',default=10))
        
            condition = {'time':{'$lt':time},'state':'on','toUser':str(user_info['_id'])}
            noticelist = await self.db.notice.get_notice_free(condition,'time','-',pagesize,0)
            for i in range(0,len(noticelist)):
                noticelist[i]=await self.get_notice_info(noticelist[i])
                await self.db.notice.update(str(noticelist[i]['_id']),{'handled':True})
            self.finish_success(result=noticelist)
        elif typ == 'info':
            noticeId =float(self.get_argument('noticeId',default=None))
            notice = await self.get_notice_info(noticeId)
            self.finish_success(result=notice)
        elif typ == 'num':
            res = {}
            condition = {'state':'on','toUser':str(user_info['_id']),'handled':True}
            res['handledNum'] = await self.db.notice.get_count(condition)
            condition = {'state':'on','toUser':str(user_info['_id']),'handled':False}
            res['unhandledNum'] = await self.db.notice.get_count(condition)
            self.finish_success(result=res)

routes.handlers += [
    (r'/v1.0/noticeholder', NoticeholderHandler),
]
