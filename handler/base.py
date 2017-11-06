from tornado.web import RequestHandler
from unit.tools import json_decode, json_encode
from tornado.gen import coroutine,Return 
import time
import config
from sdk.alimsg import AliSendCodeMsg, AliCheckCodeMsg
from handler.exceptions import PermissionDeniedError, ArgsError, MissingArgumentError
from handler.unit.unit import get_timestamp,ObjectId


DEFAULT_TYPE = []

class nBaseHandler(RequestHandler):
    '''
        本部分为基础功能,基本不变
    '''
    #有关web跨站访问的
    async def options(self):
        self.prehandle()
        self.finish()    
    
    #有关web跨站访问的
    def prehandle(self):
        self.add_header('Access-Control-Allow-Origin','*')
        self.add_header('Access-Control-Allow-Methods','GET,POST,PUT,DELETE')
        self.add_header('Access-Control-Allow-Headers','content-type,Access_token')
    
    #高级动态管理员
    async def is_supervise(self,user_id):

        superviselist=await self.db.iconfig.get_by_title('superviselist')
        for supervise in superviselist['content']['superviselist']:
            if supervise['userId']==str(user_id):
                return True
        return False
    
    #产生订单编号/不重复的字符串
    def produce_order_number(self):
        time_str= time.strftime("%Y%m%d%H%M%S", time.localtime())
        orderNumber=time_str+str(self.settings['primary_number'])
        self.settings['primary_number']=self.settings['primary_number']+1
        return orderNumber
    
    def is_debug(self):
        return self.settings['debug_mode']
    
    
    #产生一个token结构体
    async def produce_accessToken(self,user_id):
        utoken=await self.db.token.get_by_user(user_id)
        if utoken is None:
            utoken=self.db.base.dict_match(
                {
                    'userId':ObjectId(user_id),
                    'accessToken':self.db.token.produce_token(),
                    'accessTime':self.get_timestamp()
                },
                self.db.base.get_token_default()
                )
            token_id = await self.db.token.insert(utoken)
            utoken=await self.db.token.get_by_user(user_id)
            return utoken
        else:
            return utoken
            

        
    #生成时间戳
    def get_timestamp(self):
        return get_timestamp()
        
    #是否为达人
    def is_master(self,master_id):
        #0:正常用户  #1:申请成为达人中 #2:处理中 #-1:拒绝
        if master_id == '':
            return False
        if master_id == '0' or master_id == '1' or master_id == '2' or master_id == '-1':
            return False
        else:
            return True
    
    #是否是后台管理员
    async def is_manager(self,masterid):
        if self.is_debug():
            return True
        return masterid == config.MANAGER_ID
    #async self.check_noticeholder(self,user_id):
    
    async def is_circleManager(self,circle_id,user_id) :
        if self.is_debug():
            return True
            
        superviselist=await self.db.iconfig.get_by_title('superviselist')
        for supervise in superviselist['content']['superviselist']:
            if supervise['userId']==str(user_id):
                return True
                
        circle = await self.db.circle.get_by_id(circle_id)
        if user_id in circle['circleManager']:
            return True
        else:
            return False
    #验证登陆token
    @property
    def token(self):
        if "Access_token" not in self.request.headers:
            raise PermissionDeniedError("access_token error")
        else:
            return self.request.headers['Access_token']

    #获取用户基本信息
    @property
    async def user_info(self):
        if not hasattr(self, '_user_info'):
            user_token= self.token
            utoken=await self.db.token.get_by_token(user_token)
            self._user_info=await self.db.user.get_by_id(utoken['userId'])
            return self._user_info
        else:
            return self._user_info
    
    #获取GET的参数
    def get_argument(self, name, default=DEFAULT_TYPE, strip=True):
        # 参数优先查询字符串里的参数
        if self.request.method in ('GET',):
            rs = self.get_query_argument(name,default)
            if rs is DEFAULT_TYPE:
                raise MissingArgumentError(name)
            return rs
        else:
            if name in self.json_body:
                rs = self.json_body[name]
                return rs
            elif default is DEFAULT_TYPE:
                raise MissingArgumentError(name)
            else:
                return default
                

    def finish_success(self, **kwargs):
        rs = {
            'status': 'success',
            'code':'0',
            'result':list(kwargs.values())[0]
        }
        self.finish(json_encode(rs))
        
    async def AliCheckCode(self,phone,code):
        AliCheckCode = AliCheckCodeMsg(config.ALIBAICHUAN_KEY, config.ALIBAICHUAN_SECRET)
        await AliCheckCode.check_code(mobile=phone, ver_code=code)
        if not AliCheckCode.success:
            return False
        return True
        
    def finish_err(self, status_code='1', result=''):
        rs = {
            'status': 'err',
            'code':'1',
            'result':result
        }
        #self.set_status(status_code)
        self.finish(json_encode(rs))
    @property
    def json_body(self):
        if not hasattr(self, '_json_body'):
            if hasattr(self.request, "body"):
                try:
                    self._json_body = json_decode(self.request.body.decode('utf-8'))
                except ValueError:
                    raise ArgError("参数不是json格式！")
        return self._json_body
        
    @property
    def qiniu_client(self):
        return self.settings['qiniu_client']
        
    @property
    def db(self):
        return self.settings['db']
            
    async def remove_card(self,card_id):
        card =await self.db.card.get_by_id(card_id)
        if card is None:
            return False
        await self.db.team.remove_card(card['belongTeam'],card_id)
        await self.db.card.delete(card_id)
        return True
        
class BaseHandler(nBaseHandler):
    '''
        常用的复用函数
    '''
        
    async def insert_new_user(self,user_info):    
        user_id=await self.db.user.insert(
            self.db.base.dict_match(
                user_info,
                self.db.base.get_oridinaryUser_default()
                )
            )
        
        if user_id is None:
            return None
            

        return user_id
            
    async def post_common(self,post,user_info):
        if post['state'] == 'ipush':
            post=await self.db.post.get_by_id(post['content'])
            post['state'] ='push'
        publisher=await self.db.user.get_by_id(post['publisher'])
        commentlist=[]
        for j in range(0,min(2,len(post['commentList']))):
            comment= await self.db.comment.get_by_id(post['commentList'][j])
            user = await self.db.user.get_by_id(comment['commenter'])
            commentlist.append({'userName':user['realName'],'content':comment['content']})
        post={
            '_id':post['_id'],
            'publisher':{
                '_id':publisher['_id'],
                'avatar':publisher['avatar'],
                'realName':publisher['realName'],
                'certificationInfo':publisher['certificationInfo']
                },
            'like':    str(user_info['_id']) in post['likeUserList'],
            'likeNum':len(post['likeUserList']),
            'commentNum':len(post['commentList']),
            'commentList':commentlist,
            'favorMaster':str(publisher['_id']) in user_info['userFavorMaster'],
            'title':post['title'],
            'content':post['content'],
            'multiMedia':post['multiMedia'],
            'publishTime':post['publishTime'],
            'type':post['type'],
            'state':post['state'],
            'pushTime':post['pushTime'],
            'isPush':post['isPush'],
            'isSpecial':post['isSpecial'],
            'belongCircle':{
                    'circle_id':post['belongCircle'],
                    'title':post['belongCircleTitle'],
                    'type':post['belongCircleType'],
                },
            'seeNum':post['seeNum'],
            'location':post['location'],
        }
        return post
