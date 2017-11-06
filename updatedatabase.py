# coding=utf-8
import bson
import copy

def ObjectId(id):
    return bson.objectid.ObjectId(id)

class MongoDB_orm_base():

    def ObjectId(id):
        return bson.objectid.ObjectId(id)

    def dict_match(self,dict_src,dict_default):

        if type(dict_src)==list:
            for (k,v) in dict_src:
                dict_v=copy.deepcopy(dict_default)
                for i in v:
                    if i in dict_v:
                        dict_v[i]=v[i]
                for i in dict_v:
                    if dict_v[i]==None:
                        dict_v=None
                        break
                dict_dst[k]=dict_v
            return dict_dst
        for i in dict_src:
            if i in dict_default:
                dict_default[i]=dict_src[i]
        for i in dict_default:
            if dict_default[i]==None:
                return None;
        return dict_default;

    def get_oridinaryUser_default(self):
        oridinaryUser={
            'phoneNumber':'',
            'password':'',
            'weixinopenid':'',
            'realName':'',
            'avatar':'',
            'gender':'',
            'university':'',
            'campus':'',
            'realIdentity':'',
            'masterId':'',
            'userOrders':[],
            'userBalance':[],
            'userNotification':[],
            'userFavorMaster':[],
            'userFavorTeam':[],
            'userFavorEvent':[],
            'favorMeList':[],
            'certificationInfo':'',
            'entryDate':'',
            'noticeFlag':'',
            'isNew':'YES',
            'userTeam':'',
            'coverPhoto':'',
            'userType':'user',
            'labelList':[],
            'vcoin':99,
            'signup_days':[],
            'isAward':'No',
            'masterContact':{'wxNumber':'','QQNumber':'','phoneNumber':''},
        }
        return oridinaryUser
        
    def get_master_default(self):
        master={
            'userId':'', 
            'state':'',
            'realName':'',
            'avatar':'',
            'coverPhoto':'',
            'location':'',
            'category':'',
            'realTitle':'',
            'masterLabel':[],
            'personalDetails':'',
            'entryDate':'',
            'masterPhoto':[],
            'phone':'',
            # 下面的数据暂时不用
            'contact':'',
            'certificationInfo':'',
            'masterLargEvent':[],
            'masterOrders':[],
            'masterFiance':[],
            'masterNotification':[],
            'masterMessage':[],
            'collectionQuantity':'',
            'relatePhoto':[],
            'interest':[],
            'masterSign':'',
            'masterContact':{'wxNumber':'','QQNumber':'','phoneNumber':''},
            'total_money':0,
            'order_money':0,
            'tip_money':0,
        }
        return master
        
    def get_event_default(self):
        event={
            'versionId':'',
            'type':'',
            'state':'',
            'label':'',
            'location':'',
            'category':'',
            'slogan':'',    #一句话
            'title':'',
            'serviceLead':'',   #说明
            'goalsText':'',
            'importantinfo':'', #活动安排
            'coverPhoto':'',
            'photosDisplay':[],
            'extendedPhotosTitle':'',
            'extendedPhotos':[],
            'price':'',
            'hour':'',
            'plan':'',
            'belongedMaster':'',
            'masterLabel':[],
            'masterIntroduction':'',
            'upperLimit':'',
            'uclass':'',
            'orderQuantity':'',
            'collectionQuantity':'',
            'lastChangeTime':'',
            'eventLead':'',
            'unitName':'',
            'likeUserList':[],
            'commentList':[],
            'location':'',
        }
        return event
        
    def get_order_default(self):
        order = {
            'orderNumber':'',
            'orderTime':'',
            'payTime':'',
            'refundTime':'',
            'finishedTime':'',
            'belongedType':'',
            'belonged':'',
            'trainee':'',
            'master':'',
            'price':'',
            'state':'',
            'removed':'no',
            'remarkInfo':'',
            'ch_id':'',
            'channel':'',
            'refund_id':'',
            'realName':'',
            'realPhone':'',
            'removed':'',
            'comment_id':'',
        }
        return order

    def get_comment_default(self):
        comment={
            'commenter':'',
            'commentType':'',
            'postId':'',
            'orderId':'',
            'commentTime':'',
            'content':'',
            'star':[5,5,5],
            'multiMedia':[],
            'replyList':[],
            'likeUserList':[],
            'state':''
        }
        return comment

Obj = MongoDB_orm_base()

import pymongo
import random

conn = pymongo.MongoClient("127.0.0.1",27017)#('testapi.idarenhui.com:27017')
db = conn.tank #连接库

comment_src = db.comment.find_one()
comment_dst = Obj.dict_match(comment_src,Obj.get_comment_default())
print(comment_src)
print(comment_dst)
db.comment.update({'_id':comment_src['_id']},{'$set':comment_dst})
comment = db.comment.find_one({'_id':comment_src['_id']})


comment_cursor = db.comment.find()
for comment_src in comment_cursor:
    comment_dst = Obj.dict_match(comment_src,Obj.get_comment_default())
    db.comment.update({'_id':comment_src['_id']},{'$set':comment_dst})

event_cursor = db.event.find()
for event_src in event_cursor:
    event_dst = Obj.dict_match(event_src,Obj.get_event_default())
    db.event.update({'_id':event_src['_id']},{'$set':event_dst})

master_cursor = db.master.find()
for master_src in master_cursor:
    master_dst = Obj.dict_match(master_src,Obj.get_master_default())
    db.master.update({'_id':master_src['_id']},{'$set':master_dst})

user_cursor = db.user.find()
for user_src in user_cursor:
    user_dst = Obj.dict_match(user_src,Obj.get_oridinaryUser_default())
    db.user.update({'_id':user_src['_id']},{'$set':user_dst})

order_cursor = db.order.find()
for order_src in order_cursor:
    order_dst = Obj.dict_match(order_src,Obj.get_order_default())
    db.order.update({'_id':order_src['_id']},{'$set':order_dst})
