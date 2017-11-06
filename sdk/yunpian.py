# coding=utf-8
from tornado.httpclient import AsyncHTTPClient, HTTPRequest

import config

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode


class YunpianClient(object):
    def __init__(self, api_key, url):
        self.url = url
        self.api_key = api_key
        self._asy_sender = AsyncHTTPClient()

    def _sender(self, phone, text):
        data = {
            'mobile': phone,
            'text': text,
            'apikey': self.api_key,
        }
        request = HTTPRequest(
            self.url,
            method='POST',
            body=urlencode(data)
        )

        return self._asy_sender.fetch(request)

    def send_code(self, phone, code):
        text = "【%s】您的验证码是%s。如非本人操作，请忽略本短信" % (config.APP_NAME, code)
        return self._sender(phone, text)

    def send_code2(self,phone, code):
        # 验证码被封印,采用接口
        text = "【%s】您的口令是%s。如非本人操作，请忽略本短信" % (config.APP_NAME, code)
        return self._sender(phone, text)

    def send_master_change_info(self,phone,state):
        if state:
            text = "【达人荟】您好，您修改的达人资料已通过审核，请前去达人主页查看"
        else:
            text = "【达人荟】您好，很抱歉的通知您：您修改的达人资料没有通过审核，请重新查看您的申请资料，如有问题请联系达人荟客服"
        return self._sender(phone,text)

    def send_master_apply(self,phone,state):
        if state:
            text = "【达人荟】恭喜您已经通过验证，请去发布课程吧"

        else:
            text = "【达人荟】抱歉，您提交的材料未满足达人荟的认证要求，具体原因客服会电话和您交流，谢谢对达人荟的支持"

        return self._sender(phone,text)

    def ban_user(self,phone,ban):
        if ban:
            text = "【达人荟】抱歉，您的达人主页暂时被禁，详情请联系达人荟客服"
        else:
            text = "【达人荟】您好，您的达人主页已被解禁，可以继续正常使用"

        return self._sender(phone,text)

    def send_recv_comment(self,phone):
        text = "【达人荟】您收到一个新的评价快去看看吧"
        return self._sender(phone,text)

    def confirm_order(self,phone):
        text = "【达人荟】达人已同意您的预约，前去付款吧"
        return self._sender(phone,text)

    def reject_order(self,phone,less_name,reason):
        text = "您预约的%s没有被达人同意，具体原因如下:%s。欢迎体验达人荟其他精彩课程"%(less_name,reason)
        return self._sender(phone,text)

    def refund(self,phone):
        text = "【达人荟】您有一个退款正在进行"
        return self._sender(phone,text)

    def order_cancel(self,phone):
        text = "【达人荟】您有一个预约被取消"
        return self._sender(phone,text)

    def notice_master_new_order(self,phone):
        text = "【达人荟】您有一个新的预约课程，快去确认吧"
        return self._sender(phone,text)

    def notice_master_user_pay_order(self,phone):
        text = "【达人荟】您有一个课程学员已付款，请尽快安排授课哦"
        return self._sender(phone,text)

    def confitm_master_info_update(self,phone,state):
        if state:
            text = "【达人荟】您好，您修改的达人资料已通过审核，请前去达人主页查看"
        else:
            text = "【达人荟】您好，很抱歉的通知您：您修改的达人资料没有通过审核，请重新查看您的申请资料，如有问题请联系达人荟客服"

        return self._sender(phone,text)