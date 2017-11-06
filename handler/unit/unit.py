import time
import bson
def ObjectId(id):
    return bson.objectid.ObjectId(id)
def get_timestamp():
    return time.time()

def produce_notice_system_tip(topic,toUser,content):
    if topic == 'tip_finish':
        rcontent = {
            'tipId':content['tipId'], 
        }
    else:
        return None
    notice = {
        'type':'system',# system/
        'unit':'tip',#appointment
        'topic':topic,#order_request/order_finish/order_accept/order_comment
        'toUser':toUser,
        'content':rcontent,
        'time':get_timestamp(),
        'state':'on',
        'handled':False,
    }
    return notice
def produce_notice_system_appointment(topic,toUser,content):
    if topic == 'order_request' :
        rcontent={
            'orderId':content['orderId'],
        }
    elif topic == 'order_accept':
        rcontent={
            'orderId':content['orderId'],
        }
    elif topic == 'order_finish':
        rcontent={
            'orderId':content['orderId'],
        }
    elif topic == 'order_comment':
        rcontent={
            'orderId':content['orderId'],
        }
    else:
        return None
    notice={
        'type':'system',# system/
        'unit':'appointment',#appointment
        'topic':topic,#order_request/order_finish/order_accept/order_comment
        'toUser':toUser,
        'content':rcontent,
        'time':get_timestamp(),
        'state':'on',
        'handled':False,
    }
    return notice
    
