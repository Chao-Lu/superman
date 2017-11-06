from handler.base import BaseHandler
import routes
import random
import config
from handler.unit.unit import get_timestamp
from handler.exceptions import ResourceNotExistError,PermissionDeniedError,ArgsError,StateError,RelateResError

def isInSource(sourcelist,user_id):
    user_id=str(user_id)
    for s in sourcelist:
        if s['userId'] == user_id:
            return True
    return False

class StarHandler(BaseHandler):
    """
        @api {get} /v1.0/comment/star 获取事件评分
        @apiGroup comment
        @apiVersion  1.0.0
        @apiDescription 获取事件评分
        @apiPermission all
        
        @apiParam {string} event_id   评论ID

        @apiSuccess {Object}  card
        @apiSuccess (card) {string}  score 
        @apiSuccess (card) {int}     num
    """
    async def get(self):
        jsonObj = self.json_body
        event_id = jsonObj['event_id']
        comment_list = await self.db.comment.get_by_event_id(event_id)
        score = 0.0
        length = 0
        if comment_list:
            for comment in comment_list:
                if comment['star']:
                    score = score + float(comment['star'][0]) + float(comment['star'][1]) + float(comment['star'][2])
                    length = length + 1.0
            score = score/3.0/length
            score = str(int(score*10) / 10.0)
        else:
            score = '5.0'
        card = {
            'score':score,
            'num':int(length),
        }
        self.finish_success(result = card)

class CommentHandler(BaseHandler):
    """
        @api {get} /v1.0/comment 获取评论详情
        @apiGroup comment
        @apiVersion  1.0.0
        @apiDescription 获取评论详情
        @apiPermission all
        
        @apiParam {string} comment_id   评论ID

        @apiSuccess {list}  comment 评论详情
    """
    async def get(self):
        user_info=await self.user_info
        comment_id=self.get_argument('comment_id',default=None)
        comment = await self.db.comment.get_by_id(comment_id)
        commenter = await self.db.user.get_by_id(comment['commenter'])
        if commenter is None:
            raise RelateResError("评论的发起者未找到")
        comment={
            '_id':comment['_id'],
            'commenter':{
                'user_id':str(commenter['_id']),
                'realName':commenter['realName'],
                'avatar':commenter['avatar'],
                'certificationInfo':commenter['certificationInfo'],
                },
            'postId':comment['postId'],
            'orderId':comment['orderId'],
            'commentType':comment['commentType'],
            'commentTime':comment['commentTime'],
            'content':comment['content'],
            'multiMedia':comment['multiMedia'],
            'replyNum':len(comment['replyList']),
            'likeNum':len(comment['likeUserList']),
            'like':str(user_info['_id']) in comment['likeUserList'],
            'replyList':comment['replyList'],
            'replyNum':len(comment['replyList']),
            'state':comment['state']
        }
        self.finish_success(result=comment)
    """
        @api {post} /v1.0/comment 上传评论
        @apiGroup comment
        @apiVersion  1.0.0
        @apiDescription 上传评论
        @apiPermission user


        @apiParam {string}    comment_type    'appointment'/'course'/'activity'/'service'
        @apiParam {string}    post_id         eventID
        @apiParam {string}    order_id        订单id        
        @apiParam {object}    comment     评论 
        
        @apiParam (comment)   {string}    content
        @apiParam (comment)   {array}     star    [4.5,4.5,4.5]
        @apiParam (comment)   {string}    multiMedia 

        
        @apiSuccess {string}    comment_id      评论ID
    """
    async def post(self):
        user_info=await self.user_info

        json = self.json_body
        comment= json['comment']
        comment_src={
            'commenter':str(user_info['_id']),
            'commentType':json['comment_type'],
            'postId':json['post_id'],
            'commentTime':self.get_timestamp(),
            'content':comment['content'],
            'star':[float(comment['star'][0]),float(comment['star'][1]),float(comment['star'][2])],
            'multiMedia':comment['multiMedia'],
            'replyList':[],
            'likeUserList':[],
            'state':'on',
            'orderId':str(json['order_id']),
        }

        event = await self.db.event.get_by_id(json['post_id'])

        if event is None:
            raise ResourceNotExistError("事件不存在{0}")
        comment_dst=self.db.base.dict_match(comment_src,self.db.base.get_comment_default())
        comment_id = await self.db.comment.insert(comment_dst)
        #将评论和订单关联
        await self.db.order.insert_comment_id(str(json['order_id']),str(comment_id))

        touser_id = ''
        await self.db.event.insert_comment(json['post_id'],comment_id)
        touser_id=event['belongedMaster']
        self.finish_success(result=comment_id)
        '''
        if touser_id == str(user_info['_id']):
            self.finish_success(result=comment_id)
        else:
            source={
                'userId':str(user_info['_id']),
                'avatar':user_info['avatar'],
                'realName':user_info['realName']
            }
            notice = self.produce_notice("卡片评论",source,touser_id,'comment',
                            {   
                                'commentId':comment_id,
                                'postId':comment_dst['postId'],
                                'content':comment_dst['content'],
                            })
        
            notice_id = await self.db.notice.insert(notice)
            #await self.check_noticeholder(touser_id)
            #print(touser_id)
            await self.db.noticeholder.insert_notice(touser_id,notice_id)

            self.finish_success(result=comment_id)
        '''
        
    """
        @api {delete} /v1.0/comment 删除评论
        @apiGroup comment
        @apiVersion  1.0.0
        @apiDescription 删除评论
        @apiPermission user

        @apiParam {string} comment_type     'course'/'activity'/'service'/'post'
        @apiParam {string} comment_id       评论ID

        @apiSuccess {string}    result "OK"
    """
    async def delete(self):
        user_info=await self.user_info

        json = self.json_body
        comment_id = json['comment_id']
        comment_type = json['comment_type']
        comment = await self.db.comment.get_by_id(comment_id)
        if comment is None:
            raise ResourceNotExistError("评论不存在{0}".format(comment_id))
        if comment['commenter'] == str(user_info['_id']):
            pass
        elif await self.is_supervise(str(user_info['_id'])):
            pass
        else:
            raise PermissionDeniedError("无权删除本条评论")

        if comment_type == 'post':
            await self.db.post.remove_comment(comment['postId'],comment_id)
        else:
            await self.db.event.remove_comment(comment['postId'],comment_id)   
        await self.db.comment.update(comment_id,{'state':'off'})
        self.finish_success(result='OK')


class ListCommentHandler(BaseHandler):
    """
        @api {get} /v1.0/comment/list 获取卡片/event评论列表
        @apiGroup comment
        @apiVersion  1.0.0
        @apiDescription 获取卡片评论
        @apiPermission all

        @apiParam {string} post_type    'course'/'activity'/'service'/'post'
        @apiParam {string} post_id      卡片ID
        @apiParam {string} time         页码
        @apiParam {string} pagesize     页大小

        @apiSuccess {list}  commentlist 卡片评论列表
    """
        
    async def get(self):
        user_info=await self.user_info
        post_id = self.get_argument('post_id',default=None)
        post_type = self.get_argument('post_type',default=None)
        if post_type == 'post':
            post = await self.db.post.get_by_id(post_id)
        else:
            post = await self.db.event.get_by_id(post_id)

        if post is None:
            raise ResourceNotExistError("卡片/event不存在{0}".format(post_id))
        if post['state'] == 'off':
            raise ResourceNotExistError("卡片/event无效")

        ntime=self.get_timestamp()
        time=float(self.get_argument('time',default=ntime))
        if time == ntime:
            condition = {'commentTime':{'$lt':time},'postId':post_id,'state':'on',"likeUserList.5": {'$exists':1}}
            speciallist= await self.db.comment.get_comment_free(condition,'likeUserList','-',3,0)
        else:
            speciallist=[]
        pagesize=int(self.get_argument('pagesize',default=10))
        condition = {'commentTime':{'$lt':time},'postId':post_id,'state':'on'}
        andlist=[]
        for s in speciallist:
            andlist.append({'commenter':{'$ne':s['commenter']}})
        clist = await self.db.comment.get_comment_free(condition,'commentTime','-',pagesize,0)
        commentlist=speciallist+clist
        for i in range(0,len(commentlist)):
            comment=commentlist[i]
            commenter = await self.db.user.get_by_id(comment['commenter'])
            comment={
                '_id':comment['_id'],
                'commenter':{
                    'user_id':str(commenter['_id']),
                    'realName':commenter['realName'],
                    'avatar':commenter['avatar'],
                    'certificationInfo':commenter['certificationInfo']

                    },
                'postId':comment['postId'],
                'commentTime':comment['commentTime'],
                'content':comment['content'],
                'multiMedia':comment['multiMedia'],
                'replyNum':len(comment['replyList']),
                'likeNum':len(comment['likeUserList']),
                'like':str(user_info['_id']) in comment['likeUserList'],
                'replyList':comment['replyList'],
                'replyNum':len(comment['replyList']),
                'state':comment['state'],
                'isHot':comment in speciallist,
            }
            commentlist[i]=comment
        self.finish_success(result=commentlist)
        
        pass

class ReplyHandler(BaseHandler):
    """
        @api {post} /v1.0/comment/reply 上传二级评论
        @apiGroup comment
        @apiVersion  1.0.0
        @apiDescription 上传二级评论
        @apiPermission user
        @apiParam {object}  reply   二级评论
        @apiParam {string}  comment_id  所属评论ID
        
        @apiSuccess {string}    result "OK"
    """
    async def post(self):
        user_info=await self.user_info
        json = self.json_body
        reply= json['reply']
        comment_id = json['comment_id']
        reply_src={
            'replyerId':str(user_info['_id']),
            'replyerName':user_info['realName'],
            'content':reply['content'],
            'replyTime':self.get_timestamp(),
        }
        comment = await self.db.comment.get_by_id(comment_id)
        if comment is None:
            raise RelateResError("评论不存在:{0}".format(comment_id))
        await self.db.comment.insert_reply(comment_id,reply_src)


        self.finish_success(result="OK")
        
    """
        @api {delete} /v1.0/comment/reply 删除二级评论
        @apiGroup comment
        @apiVersion  1.0.0
        @apiDescription 删除卡片评论
        @apiPermission user
        @apiParam {object}  reply   二级评论
        @apiParam {string}  comment_id  所属评论ID
        
        @apiSuccess {string}    result "OK"
    """
    async def delete(self):
        user_info=await self.user_info

        json = self.json_body
        comment_id= json['comment_id']
        reply = json['reply']
        if reply['replyerId'] == str(user_info['_id']):
            pass
        elif  await self.is_supervise(str(user_info['_id'])):
            pass
        else:
            raise PermissionDeniedError("无权删除本条回复")
            
        comment = await self.db.comment.get_by_id(comment_id)
        if comment is None:
            raise ResourceNotExistError("评论不存在{0}".format(comment_id))
        await self.db.comment.remove_reply(comment_id,reply)
        self.finish_success(result='OK')
    
        
class likeCommentHandler(BaseHandler):
    """
        @api {post} /v1.0/comment/like_comment     评论点赞
        @apiGroup comment
        @apiVersion  1.0.0
        @apiDescription 评论点赞
        @apiPermission user
        @apiParam {string}  comment_id  评论ID
        
        @apiSuccess {string}    result "OK"
    """
    async def post(self):
        user_info=await self.user_info
        jsonObj = self.json_body
        comment_id= jsonObj['comment_id']
        comment = await self.db.comment.get_by_id(comment_id)
        if comment is None:
            raise ResourceNotExistError("评论不存在{0}".format(comment_id))      
        if str(user_info['_id']) in comment['likeUserList']:
            await self.db.comment.remove_like(comment_id,str(user_info['_id']))
            comment = await self.db.comment.get_by_id(comment_id)
            self.finish_success(result={'state':'unlike','likeNum':len(comment['likeUserList'])})
        else:
            await self.db.comment.insert_like(comment_id,str(user_info['_id']))
            self.finish_success(result={'state':'like','likeNum':len(comment['likeUserList'])})
        
    

class likeContentHandler(BaseHandler):
    """
        @api {post} /v1.0/comment/like_content     动态点赞/event点赞
        @apiGroup comment
        @apiVersion  1.0.0
        @apiDescription 动态点赞/event点赞
        @apiPermission user
        @apiParam   {string}    post_id         评论ID
        @apiParam   {string}    comment_type    course/activity/service/post
        
        
        @apiSuccess {string}    result "OK"
    """
    async def post(self):
        user_info=await self.user_info
        jsonObj = self.json_body
        post_id = jsonObj['post_id']
        comment_type = jsonObj['comment_type']
        title_type = ''
        like_type = ''
        touser_id = ''

        if comment_type == 'post':
            post = await self.db.post.get_by_id(post_id)  
            title_type = '动态点赞'
            like_type = 'post_like' 
        else:
            post = await self.db.event.get_by_id(post_id)
            title_type = 'event点赞'
            like_type = 'event_like'
        
        if post is None:
            raise ResourceNotExistError("评论不存在{0}".format(post_id))

        #点两次相当于取消点赞
        if str(user_info['_id']) in post['likeUserList']:
            if comment_type == 'post':
                await self.db.post.remove_like(post_id,str(user_info['_id']))
                post = await self.db.post.get_by_id(post_id)
            else:
                await self.db.event.remove_like(post_id,str(user_info['_id']))
                post = await self.db.event.get_by_id(post_id)
            self.finish_success(result={'state':'unlike','likeNum':len(post['likeUserList'])})
        else:
            if comment_type == 'post':
                await self.db.post.insert_like(post_id,str(user_info['_id']))
                touser_id=post['publisher']
            else:
                await self.db.event.insert_like(post_id,str(user_info['_id']))
            
            if like_type == 'post_like':
                post = await self.db.post.get_by_id(post_id)
            elif like_type == 'event_like':
                post = await self.db.event.get_by_id(post_id)
            self.finish_success(result={'state':'like','likeNum':len(post['likeUserList'])})
    


routes.handlers += [
    (r'/v1.0/comment', CommentHandler),
    (r'/v1.0/comment/list',ListCommentHandler),
    (r'/v1.0/comment/reply', ReplyHandler),
    (r'/v1.0/comment/like_comment', likeCommentHandler),
    (r'/v1.0/comment/like_content',likeContentHandler),
]
