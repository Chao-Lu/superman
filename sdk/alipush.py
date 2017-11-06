from tornado.gen import coroutine
from sdk import top
import sdk.top.api
import json


class AliCloudPush(object):
    def __init__(self, ak, sk):
        self.req = top.api.CloudpushPushRequest(domain='http://gw.api.taobao.com')
        self.req.set_app_info(top.appinfo(ak, sk))
        self.req.device_type = 3
        self.req.remind = 'true'
        self.req.store_offline = 'true'
        self.req.type = 1

    @coroutine
    def push(self, user_id, content, target='account', title="达人荟"):
        self.req.target = target
        self.req.target_value = str(user_id)
        self.req.body = content
        self.req.title = title
        result = yield self.req.getResponse()
        self.success = result['cloudpush_push_response']['is_success']
        # self.message = result['cloudpush_push_response']['result']['message']

    @coroutine
    def push_all(self, content, title="达人荟"):
        self.req.target = 'all'
        self.req.target_value = ''
        self.req.body = content
        self.req.title = title
        result = yield self.req.getResponse()
        self.success = result['cloudpush_push_response']['is_success']

    @coroutine
    def user_order_push(self, user_id, content, order_id, state, price, target='account', title="达人荟"):
        android_ext_parameters = {
            'order_id': order_id,
            'order_state': state,
            'common_price': price,
        }
        ios_ext_parameters = {
            'view': 'user_order',
            'order_id': order_id,
        }
        self.req.target = target
        self.req.target_value = str(user_id)
        self.req.body = content
        self.req.title = title
        self.req.android_open_type = 2
        self.req.android_activity = 'com.dreamspace.superman.UI.Activity.Person.OrderDetailActivity'
        self.req.android_ext_parameters = json.dumps(android_ext_parameters)
        self.req.ios_badge = 1
        self.req.ios_ext_parameters = json.dumps(ios_ext_parameters)
        result = yield self.req.getResponse()
        self.success = result['cloudpush_push_response']['is_success']

    @coroutine
    def master_order_push(self, user_id, content, order_id, state, price, target='account', title="达人荟"):
        android_ext_parameters = {
            'order_id': order_id,
            'order_state': state,
            'common_price': price,
        }
        ios_ext_parameters = {
            'view': 'master_order',
            'order_id': order_id,
        }
        self.req.target = target
        self.req.target_value = str(user_id)
        self.req.body = content
        self.req.title = title
        self.req.android_open_type = 2
        self.req.android_activity = 'com.dreamspace.superman.UI.Activity.Superman.SmOrderDetailActivity'
        self.req.android_ext_parameters = json.dumps(android_ext_parameters)
        self.req.ios_badge = 1
        self.req.ios_ext_parameters = json.dumps(ios_ext_parameters)
        result = yield self.req.getResponse()
        self.success = result['cloudpush_push_response']['is_success']

    @coroutine
    def lesson_push(self, less_id, content, title="达人荟", target='account', user_id='Null'):
        android_ext_parameters = {
            'LESSON_INFO': less_id,
        }
        ios_ext_parameters = {
            'view': 'lesson',
            'less_id': less_id,
        }
        self.req.target = target
        self.req.target_value = str(user_id)
        self.req.body = content
        self.req.title = title
        self.req.android_open_type = 2
        self.req.android_activity = 'com.dreamspace.superman.UI.Activity.Main.LessonDetailInfoActivity'
        self.req.android_ext_parameters = json.dumps(android_ext_parameters)
        self.req.ios_badge = 1
        self.req.ios_ext_parameters = json.dumps(ios_ext_parameters)
        result = yield self.req.getResponse()
        self.success = result['cloudpush_push_response']['is_success']

class AliCloudPushNoticeToIOS(object):
    def __init__(self, ak, sk):
        self.req = top.api.CloudpushNoticeIosRequest(domain='http://gw.api.taobao.com')
        self.req.set_app_info(top.appinfo(ak, sk))
        self.req.env = 'DEV'
        self.req.target = 'account'

    @coroutine
    def push(self, user_id, summary, ext, target='account', title="达人荟"):
        _ext = ext.replace('\"', '\\\"')
        self.req.ext = _ext
        self.req.summary = summary
        self.req.target_value = user_id
        result = yield self.req.getResponse()
        self.success = result['cloudpush_notice_ios_response']['is_success']
