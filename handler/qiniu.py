from handler.base import BaseHandler
import config
import routes
import bson    

class QiniuHandler(BaseHandler):

    """
        @api {get} /v1.0/static/token 七牛上传token
        @apiName upload_token
        @apiGroup other
        @apiVersion  1.0.0
        @apiDescription 获取七牛用的上传token

        @apiPermission all

        @apiSuccess {String} key 分配的文件名
        @apiSuccess {String} token 上传使用的token

    """
    def get(self):
        key = str(bson.ObjectId())
        token = self.qiniu_client.upload_token(config.bucket_name, key, 7200)
        self.finish_success(result={'token':token, 'key':key,'domain':config.IMAGE_URL})
routes.handlers += [
    (r'/v1.0/static/qiniu',QiniuHandler),
]
