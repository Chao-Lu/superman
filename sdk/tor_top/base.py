import datetime
import hashlib
import operator
from collections import OrderedDict
from urllib.parse import urlencode

from tornado.httpclient import HTTPRequest, AsyncHTTPClient

TEST_URL = 'http://gw.api.tbsandbox.com/router/rest'
URL = 'http://gw.api.taobao.com/router/rest'

class TOPClient(object):
    def __init__(self, app_key, version='2.0', sign_method='md5'):
        self.app_key = app_key
        self.version = version
        self.sign_method=sign_method
        self.http_client = AsyncHTTPClient()

    async def _fetch(self, **kwargs):
        data = dict(kwargs)
        data['timestamp'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data['format'] = 'JSON'
        data['app_key'] = self.app_key
        data['v'] = self.version
        data['app_key'] = self.app_key
        data['sign_method'] = self.sign_method
        data['sign'] = self._sign(data)
        print(data)
        request = HTTPRequest(
            TEST_URL,
            method='POST',
            headers={'Content-Type':'application/x-www-form-urlencoded;charset=utf-8'},
            body=urlencode(data)
        )

        res = await self.http_client.fetch(request)
        return res.body

    async def fetch(self):
        raise NotImplementedError

    def _sign(self, data):
        if self.sign_method == 'md5':
            sorted_data = sorted(data.items(), key=operator.itemgetter(0))
            _sign_string = self.app_key + ''.join(x + y for x, y in sorted_data) + self.app_key
            return hashlib.new('md5', _sign_string.encode('utf-8')).hexdigest().upper()
        else:
            raise


