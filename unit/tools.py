import json
import re
from datetime import datetime
import time
import random
from math import sin, cos, pi, acos

import math
from bson import ObjectId

import config

image_name_pattern = re.compile(r'.+/(\w+)\?*')


def distance(mlata, mlona, mlatb, mlonb):
    mlata, mlona, mlatb, mlonb = float(mlata), float(mlona), float(mlatb), float(mlonb)
    R = 6378137
    C = sin(mlata) * sin(mlatb) * cos(mlona - mlonb) + cos(mlata) * cos(mlatb)
    return float(abs(R * acos(C) * pi / 180))


def get_str_from_time(mytime):
    if mytime is None:
        return "2000-01-01 00:00:00"
    if isinstance(mytime, datetime):
        return mytime.strftime("%Y-%m-%d %H:%M:%S")


def get_time_from_str(time_str):
    assert isinstance(time_str, str)
    return datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")

def phone_num_encode(phone_num):
    return phone_num[:2] + "******" + phone_num[len(phone_num) - 3:]

class MilakuluJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            encoded_object = o.strftime(config.DATETIME_FORMAT)
        elif isinstance(o, ObjectId):
            encoded_object = str(o)
        else:
            encoded_object = super(MilakuluJSONEncoder, self).default(o)

        return encoded_object


def json_encode(o):
    return json.dumps(o, cls=MilakuluJSONEncoder)


def json_decode(o):
    return json.loads(o)


def get_image_url(image_name, size=''):
    return "%s%s?%s" % (config.IMAGE_URL, image_name, size)


def get_image_name(image_url):
    rs = image_name_pattern.match(image_url)
    if rs:
        return rs.groups()[0]
    else:
        return image_url


#返回tuple，第一个是验证码，第二个是剩余有效时间
def get_dynamic_code():
    i = int(time.time()-427641)
    j = i>>5<<5
    random.seed(j)
    code = str(random.randrange(10000000,99999999))
    return (code,32-i+j)
    
