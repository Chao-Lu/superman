# coding=utf-8
import ssl
import os
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from motor import MotorClient
from tornado.options import options, define
import random
import config
#from database import mongo_client
from ORM.MongoDB_ORM import MongoDB_ORM
import routes
import qiniu
#from sdk.yunpian import YunpianClient
#from sdk.umengpush import UmengPushClient


define("port", default=8555, help="本地监听端口", type=int)
define("DEBUG", default=True, help="是否开启debug模式", type=bool)
define("TEST",default=True,help="测试服务器，支持跨域访问,推送测试模式",type=bool)
define("mongo_db", default="tank", help="mongo数据", type=str)
tornado.options.parse_command_line()

mongo_client = MotorClient('127.0.0.1:27017')#('testapi.idarenhui.com:27017')

application = tornado.web.Application(
    handlers=routes.handlers,
    db = MongoDB_ORM(mongo_client[options.mongo_db]),
    qiniu_client = qiniu.Auth(config.qiniu_ak,config.qiniu_sk),
    #yunpian_client = YunpianClient(config.YUN_PIAN_APIKEY,config.YUN_PIAN_URL),
    #umengpush_client = UmengPushClient(options.TEST),
    TEST = options.TEST,
    debug = options.DEBUG,
    compiled_template_cache = True,
    static_hash_cache = True,
    autoreload = True,
    primary_number = random.randint(0,10000),
    debug_mode=False,

)
application.listen(options.port)
#server = tornado.httpserver.HTTPServer(
#    application,
#    ssl_options={
#           "certfile": os.path.join(os.path.abspath("."), "213931700560380.pem"),
#           "keyfile": os.path.join(os.path.abspath("."), "213931700560380.key"),
#    }
#)
#server.listen(options.port)
ioloop = tornado.ioloop.IOLoop.current()

ioloop.start()
