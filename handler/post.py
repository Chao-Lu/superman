from handler.base import BaseHandler
import routes
import random
import config
from handler.unit.unit import get_timestamp
from handler.exceptions import ResourceNotExistError,PermissionDeniedError,ArgsError,StateError,RelateResError

'''
def isInSource(sourcelist,user_id):
    user_id=str(user_id)
    for s in sourcelist:
        if s['userId'] == user_id:
            return True
    return False
'''


class PostFreeHandler(BaseHandler):
    """
        @api {get} /v1.0/post/free    获取动态列表
        @apiGroup master
        @apiVersion  1.0.0
        @apiDescription 获取动态列表

        @apiPermission user
        
        @apiParam    {string}    condition    
        @apiParam    {string}    sortby
        @apiParam    {string}    sort
        @apiParam    {string}    limit
        @apiParam    {string}    skip
        
        @apiSuccess    {Object}    postlist    动态列表
    """
    async def get(self):
        user_info=await self.user_info


        condition = json.loads(self.get_argument('condition',default='{}'))
        sortby = str(self.get_argument('sortby',default='_id'))
        sort = str(self.get_argument('sort',default='+'))
        limit = int(self.get_argument('limit',default=10))
        skip = int(self.get_argument('skip',default=0))
        

        postlist = await self.db.post.get_post_free(condition,sortby,sort,limit,skip)
        for i in range(0,len(postlist)):
            postlist[i]=await self.post_common(postlist[i],user_info)

        self.finish_success(result=postlist)
        pass

class PostHandler(BaseHandler):

    async def get(self):
        """
            @api {get} /v1.0/post 获取动态详情
            @apiGroup post
            @apiVersion  1.0.0
            @apiDescription 获取动态详情

            @apiPermission all
        
            @apiParam {string} post_id       动态id
        
            @apiSuccess    {Object}    post    动态信息
        
        """
        user_info=await self.user_info
        post_id=self.get_argument('post_id',default=None)
        post = await self.db.post.get_by_id(post_id)
        if post is None:
            raise ResourceNotExistError("卡片不存在{0}".format(post_id))
        if post['state'] == 'off':
            raise ResourceNotExistError("卡片无效")
        post=await self.post_common(post,user_info)
        await self.db.post.insert_seenum(post_id)
        if post['belongCircle']['circle_id'] == '':
            post['circle']={
                'avatar':'',
                'postNum':0,
                'seeNum':0,
            }
        else:
            circle =await self.db.circle.get_by_id(post['belongCircle']['circle_id'])
            if circle !=None:
                post['circle']={
                    'avatar':circle['avatar'],
                    'postNum':len(circle['postList']),
                    'seeNum':circle['seeNum'],
                    'type':circle['type'],
                }
            else:
                post['circle']={
                    'avatar':'',
                    'postNum':0,
                    'seeNum':0,
                }
        self.finish_success(result=post)
        pass
class PostMasterHandler(BaseHandler):
    """
        @api {POST} /v1.0/post 上传动态
        @apiGroup post
        @apiVersion  1.0.0
        @apiDescription 上传动态
        @apiPermission master
        
        @apiParam {object}    post    动态信息
        @apiParam {object}    ptype    动态t  affiche/normal
        @apiSuccess    {string}    post_id
    """
    async def post(self):
        user_info=await self.user_info
            
        jsonObj=self.json_body
        circle_id=jsonObj['post']['belongCircle']
        if 'ptype' in jsonObj.keys():
            ptype=jsonObj['ptype']
        else:
            ptype='normal'
        circle =await self.db.circle.get_by_id(circle_id)
        if circle is None or circle['state'] == 'off':
            raise ResourceNotExistError("circle 无效")
        if circle['state'] == 'news':
            if user_info['userTeam'] == '':
                raise PermissionDeniedError("无权限")
            else:
                userteam = await self.db.userteam.get_by_id(user_info['userTeam'])
                if str(user_info['_id']) not in userteam['teamMember']:
                    raise PermissionDeniedError("无权限")
        if ptype=='affiche' and not await self.is_circleManager(circle_id,str(user_info['_id'])) :
            raise PermissionDeniedError("无权限")
        if ptype == 'affiche':
            isAffiche='yes'
        else:
            isAffiche='no'
        post_src={
            'title':jsonObj['post']['title'],
            'publisher':str(user_info['_id']),
            'content':jsonObj['post']['content'],
            'multiMedia':jsonObj['post']['multiMedia'],
            'likeUserList':[],
            'commentList':[],
            'publishTime':self.get_timestamp(),
            'type':jsonObj['post']['type'],
            'state':'on',
            'pushTime':self.get_timestamp(),
            'belongCircle':circle_id,
            'belongCircleTitle':circle['title'],
            'belongCircleType':circle['type'],
            'isAffiche': isAffiche,
            'location':user_info['university'],
        }

        post_dst=self.db.base.dict_match(post_src,self.db.base.get_post_default())

        post_id= await self.db.post.insert(post_dst)
        
        if post_id is None:
            raise ResourceNotExistError("上传失败")
        await self.db.circle.insert_post(circle_id,str(post_id))
        if ptype=='affiche':
            await self.db.circle.insert_affiche(circle_id,str(post_id))
        self.finish_success(result=post_id)
        pass
    """
        @api {DELETE} /v1.0/post 删除动态
        @apiGroup card
        @apiVersion  1.0.0
        @apiDescription 删除动态
        @apiPermission user
        @apiParam    {string}    post_id        动态ID
        @apiSuccess    {string}    result        "OK"
    """
    async def delete(self):
        user_info=await self.user_info

        json = self.json_body
        post_id= json['post_id']
        post = await self.db.post.get_by_id(post_id)
        if post is None:
            raise ResourceNotExistError("动态不存在{0}".format(post_id))
        if post['publisher'] == str(user_info['_id']):
            pass
        elif await self.is_supervise(str(user_info['_id'])):
            pass
        else:
            raise PermissionDeniedError("无权删除本条动态")
        await self.db.post.update(post_id,{'state':'off'})
        postlist =await self.db.post.get_post_free({'content':post_id,'state':'ipush'},'_id','+',100,0)
        for post in postlist:
            await self.db.post.update(post['_id'],{'state':'off'})
        await self.db.circle.remove_post(post['belongCircle'],post_id)
        await self.db.circle.remove_special_post(post['belongCircle'],post_id)
        await self.db.circle.remove_affiche(post['belongCircle'],post_id)
        self.finish_success(result='OK')


class CommentHandler(BaseHandler):
    """
        @api {GET} /v1.0/post/comment 获取评论详情
        @apiGroup post
        @apiVersion  1.0.0
        @apiDescription 获取评论详情
        @apiPermission all
        
        @apiParam {string} comment_id    评论ID

        @apiSuccess    {list}    comment    评论详情
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
        @api {POST} /v1.0/post/comment 上传卡片评论
        @apiGroup post
        @apiVersion  1.0.0
        @apiDescription 上传卡片评论
        @apiPermission user
        
        @apiParam {object}    comment    卡片评论
        @apiParam    {string}    post_id    评论ID
        @apiSuccess    {string}    comment_id    评论ID
    """
    async def post(self):
        user_info=await self.user_info

        json = self.json_body
        comment= json['comment']
        comment_src={
            'commenter':str(user_info['_id']),
            'postId':json['post_id'],
            'commentTime':self.get_timestamp(),
            'content':comment['content'],
            'multiMedia':comment['multiMedia'],
            'replyList':[],
            'likeUserList':[],
            'state':'on'
        }
        post = await self.db.post.get_by_id(json['post_id'])
        if post is None:
            raise ResourceNotExistError("卡片不存在{0}")
        comment_dst=self.db.base.dict_match(comment_src,self.db.base.get_comment_default())
        comment_id = await self.db.comment.insert(comment_dst)
        
        await self.db.post.insert_comment(json['post_id'],comment_id)



        self.finish_success(result=comment_id)
        
    """
        @api {DELETE} /v1.0/post/comment 删除卡片评论
        @apiGroup card
        @apiVersion  1.0.0
        @apiDescription 删除卡片评论
        @apiPermission user
        @apiParam {string} comment_id    评论ID
        @apiSuccess    {string}    result "OK"
    """
    async def delete(self):
        user_info=await self.user_info

        json = self.json_body
        comment_id= json['comment_id']
        comment = await self.db.comment.get_by_id(comment_id)
        if comment is None:
            raise ResourceNotExistError("评论不存在{0}".format(comment_id))
        if comment['commenter'] == str(user_info['_id']):
            pass
        elif await self.is_supervise(str(user_info['_id'])):
            pass
        else:
            raise PermissionDeniedError("无权删除本条评论")
        await self.db.post.remove_comment(comment['postId'],comment_id)
        await self.db.comment.update(comment_id,{'state':'off'})
        self.finish_success(result='OK')


class PostCommentHandler(BaseHandler):
    """
        @api {GET} /v1.0/post/comment/list 获取卡片评论列表
        @apiGroup post
        @apiVersion  1.0.0
        @apiDescription 获取卡片评论
        @apiPermission all
        
        @apiParam {string} post_id    卡片ID
        @apiParam {string} time        页码
        @apiParam {string} pagesize    页大小

        @apiSuccess    {list}    commentlist    卡片评论列表
    """
        
    async def get(self):
        user_info=await self.user_info
        post_id=self.get_argument('post_id',default=None)
        post = await self.db.post.get_by_id(post_id)
        if post is None:
            raise ResourceNotExistError("卡片不存在{0}".format(post_id))
        if post['state'] == 'off':
            raise ResourceNotExistError("卡片无效")

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
        @api {POST} /v1.0/post/reply 上传二级评论
        @apiGroup card
        @apiVersion  1.0.0
        @apiDescription 上传二级评论
        @apiPermission user
        @apiParam {object}  reply    二级评论
        @apiParam {string}  comment_id    所属评论ID
        
        @apiSuccess    {string}    result "OK"
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
        @api {DELETE} /v1.0/card/reply 删除二级评论
        @apiGroup card
        @apiVersion  1.0.0
        @apiDescription 删除卡片评论
        @apiPermission user
        @apiParam {object}  reply    二级评论
        @apiParam {string}  comment_id    所属评论ID
        
        @apiSuccess    {string}    result "OK"
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
        @api {POST} /v1.0/post/comment/like 评论点赞
        @apiGroup post
        @apiVersion  1.0.0
        @apiDescription 评论点赞
        @apiPermission user
        @apiParam {string}  comment_id    评论ID
        
        @apiSuccess    {string}    result "OK"
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
        
    
        
class likePostHandler(BaseHandler):
    """
        @api {POST} /v1.0/post/like 动态点赞
        @apiGroup post
        @apiVersion  1.0.0
        @apiDescription 动态点赞
        @apiPermission user
        @apiParam {string}  post_id    评论ID
        
        
        @apiSuccess    {string}    result "OK"
    """
    async def post(self):
        user_info=await self.user_info
        jsonObj = self.json_body
        post_id= jsonObj['post_id']
        post = await self.db.post.get_by_id(post_id)
        if post is None:
            raise ResourceNotExistError("评论不存在{0}".format(post_id))
        if str(user_info['_id']) in post['likeUserList']:
            await self.db.post.remove_like(post_id,str(user_info['_id']))
            post = await self.db.post.get_by_id(post_id)
            self.finish_success(result={'state':'unlike','likeNum':len(post['likeUserList'])})
        else:
            await self.db.post.insert_like(post_id,str(user_info['_id']))
            post = await self.db.post.get_by_id(post_id)
            self.finish_success(result={'state':'like','likeNum':len(post['likeUserList'])})


        



routes.handlers += [
    (r'/v1.0/post/master', PostMasterHandler),
    (r'/v1.0/post', PostHandler),
    (r'/v1.0/post/comment', CommentHandler),
    (r'/v1.0/post/comment/list',PostCommentHandler),
    (r'/v1.0/post/reply', ReplyHandler),
    (r'/v1.0/post/comment/like', likeCommentHandler),
    (r'/v1.0/post/like',likePostHandler),
]
