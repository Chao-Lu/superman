from handler.base import BaseHandler
import routes
from tornado.httpclient import AsyncHTTPClient,HTTPError,HTTPRequest
import json
import time
import config
from handler.unit.unit import ObjectId
from handler.exceptions import ResourceNotExistError,PermissionDeniedError,ArgsError,StateError,RelateResError

class CategoryHandler(BaseHandler):
    """
        @api {get} /v1.0/category 获取某一类所有事件列表
        @apiGroup event
        @apiVersion  1.0.0
        @apiDescription 获取事件列表

        @apiPermission user
        
        @apiParam   {string}    category    其实我也不知道类别叫什么名字,调用的时候打印了所有类别
        @apiParam   {string}    type        'course'/'activity'/'service'/'appointment':

        
        @apiSuccess {Object}    eventlist   事件列表
    """
    async def get(self):
        user_info=await self.user_info
        category = self.get_argument('category',default=None)
        typ = self.get_argument('type',default=None)

        sortby = '_id'
        sort = '+'
        limit = 1000
        skip = 0
        condition={}
        categorylist = await self.db.category.get_category_free(condition,sortby,sort,limit,skip)
        print(categorylist)
        #类型满足条件
        if typ == 'course' or typ == 'activity' or typ == 'service' or typ == 'appointment':
            condition['type']=typ
        else:
            raise ArgsError("type?")
            return 
        #匹配相应的类别id
        category_example = {}
        for category_example in categorylist:
            if category == category_example['title']:
                condition['category']=category_example[i]['_id']
                break
        #不存在相应的类别
        if 'category' not in condition:
            raise ArgsError("category?")
        #选择尚未关闭的事件
        condition['$or']=[{'state':'on'},{'state':'onno'}]
        
        eventlist = []
        elist=await self.db.event.get_event_free(condition,sortby,sort,limit,skip)
        if len(elist) == 0:
            pass
        else:
            eventlist.append({'category':category_example,'events':elist})
        self.finish_success(result=eventlist)


routes.handlers += [
    (r'/v1.0/category', CategoryHandler),
]