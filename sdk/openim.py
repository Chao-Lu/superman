import datetime

from tornado.httpclient import AsyncHTTPClient

class OpenIMClient(object):
    _asy_client = AsyncHTTPClient()
    URL="https://eco.taobao.com/router/rest"
    DATETIME_FORMAT = '%Y-%m-%d'
    def __init__(self):
        pass

    def _sender(self):
        data = {
            'timestamp':datetime.datetime.now().strftime()
        }