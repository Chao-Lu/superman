# coding=utf-8
import bson
import copy
import pymongo

def ObjectId(id):
    return bson.objectid.ObjectId(id)
    
class MongoDB_orm_base(object):
    def __init__(self, mongo_control):
        self.db = mongo_control
        
class MongoDB_control(object):
    def __init__(self, mongo_client):
        self.db = mongo_client
        
    
    def ObjectId(id):
        return bson.objectid.ObjectId(id)

    # To match dict_src to dict_dst(like 'right join' in sql)
    def dict_match(self, dict_src, dict_default,default = None):
        for i in dict_src:
            if i in dict_default:
                dict_default[i] = dict_src[i]
        for i in dict_default:
            if dict_default[i] == default:
                return None;
        return dict_default
    
    # get one document
    async def get_document_one(self, condition, colName):
        document = await self.db[colName].find_one(condition)
        return document
        
    # get count of documents
    async def get_document_count(self, condition, colName):
        n = await self.db[colName].find(condition).count()
        return n
        
    # get document List by condition, sortby, sort, limit, skip
    async def get_document_list(self, condition, sortby, sort, limit, skip, colName):
        sortlist = {
            '+':pymongo.ASCENDING ,
            '-':pymongo.DESCENDING
        }
        cursor = self.db[colName].find(condition)
        cursor.sort(sortby, sortlist[sort]).limit(limit).skip(skip)
        documentlist = []
        async for document in cursor:
            documentlist.append(document)
        return documentlist
        
    # update document
    async def update(self, condition, document, colName):
        await self.db[colName].update(condition,document)
    
    # insert doucumnet
    async def insert(self, document, colName):
        result=await self.db[colName].insert(document)
        return result
    
    # delete document
    async def delete(self, condition, colName):
        await self.db[colName].delete_many(condition)
    
    # @token ----------------------------------------
    # be used to identity user
    def get_token_default(self):
        token={
            'userId':'',
            'accessToken':'',
            'accessTime':''
        }
        return token
        
    def brief_token(self, document, type = 'brief'):
        if type == 'brief':
            brief_document = {
                'userId':'',
                'accessToken':'',
                'accessTime':''
            }
            r_document = self.dict_match(document, brief_document)
        return r_document
       
    # @mode --------------------------------
    # vote and ?
    def get_mode_default(self,type):
        mode = {
                'beginTime':'',
                'endTime':'',
                'content':'',
                'belongActivity':'',
                'joinList':[],
                'state':'on',
                'type':type,
                'title':'',
                'avatar':'',
                'entryDate':'',
            }
        if type == 'vote':
            mode['function']={
                'optList':[],#optList:[{'info':'','title':'','avatar':'','num'}]
                'voteNumMap':{},
                'supportMap':{},#supportMap: 'userId':{'voteList':[{'feature':'','time':''}]}
                'supportNum':0,
                'lastTime':'',
                'state':'on',
                'typeAB':'',
            }
        if type == 'seat':
            mode['function']={
                'seatStateList':'',
                'seatNameList':'',
                'seatUserList':'',
                'HTmap':'',
                'userList':[],
                'state':'on',
                'joinMap':{},#'userId':{'chooseList':[{'positionX':'','positionY':'','type':'','time':''}]}
            }
        return mode
    
    def brief_mode(self, document, type = 'brief'):
        if type == 'brief':
            brief_document = {
                '_id':'',
                'beginTime':'',
                'endTime':'',
                'content':'',
                'belongActivity':'',
                'joinList':[],
                'state':'on',
                'type':'',
                'title':'',
                'avatar':'',
                'entryDate':'',
                'function':'',
            }
            r_document = self.dict_match(document, brief_document)
        return r_document
        
    # @circle ---------------------------------
    # activity 
    def get_circle_default(self):
        circle={
            'avatar':'',
            'title':'',
            'postList':[],
            'seeNum':0,
            'circleInfo':'',
                #'normal','news'  {'backImage','content'}
                #'activity'   {'backImage','content','orgaList'}
                #
            'moreInfo':'',
            'specialPost':[],
            'topPost':[],
            'circleManager':[],
            'state':'off',
            'type':'normal',
            'location':'',
            'modeList':[],
            'activityList':[],
            'afficheList':[],
            'position':0,
            'entryDate':'',
        }
        return circle
    
    def brief_circle(self, document, type = 'brief'):
        if type == 'brief':
            brief_document = {
                '_id':'',
                'avatar':'',
                'title':'',
                'postList':[],
                'seeNum':0,
                'circleInfo':'',
                'state':'',
                'type':'',
                'entryDate':'',
                'location':'',
            }
            r_document = self.dict_match(document, brief_document)
        return r_document
    
    # @ordi
    # user_info
    def get_user_default(self):
        user={
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
            'identity':'',
        }
        return user
        
    def get_oridinaryUser_default(self):
        return self.get_user_default()
    
    def brief_user(self, document, type = 'brief'):
        if type == 'brief':
            brief_document = {
                '_id':'',
                'realName':'',
                'avatar':'',
                'gender':'',
                'university':'',
                'campus':'',
                'realIdentity':'',
                'masterId':'',
                'userTeam':'',
                'coverPhoto':'',
                'userType':'',
            }
            r_document = self.dict_match(document, brief_document)
        return r_document
        
    # @master
    # master_info only be obtained by master
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
        
    def brief_master(self, document, type = 'brief'):
        if type == 'brief':
            brief_document = {
                'userId':'',
                'state':'',
                'realName':'',
                'avatar':'',
                'coverPhoto':'',
                'location':'',
                'category':'',
                'realTitle':[],
                'masterLabel':[],
                'personalDetails':'',
                'entryDate':'',
                'certificationInfo':'',
                'masterSign':'',
                'total_money':0,
                'order_money':0,
                'tip_money':0,
                'masterContact':'',
            }
            r_document = self.dict_match(document, brief_document)
        return r_document
    
 
    # @notice
    # notice
    def get_notice_default(self):
        notice={
            'type':'',# system/
            'unit':'',#appointment
            'topic':'',#order_request/order_finish/order_accept/order_comment
            'toUser':'',
            'content':{},
            'time':'',
            'state':'',
            'handled':'',
        }
        return notice
        
    def brief_notice(self, document, type = 'brief'):
        if type == 'brief':
            brief_document = {
                '_id':'',
                'type':'',# system/
                'unit':'',#appointment
                'topic':'',#order_request/order_finish/order_accept/order_comment
                'toUser':'',
                'content':{},
                'time':'',
                'state':'',
                'handled':'',
            }
            r_document = self.dict_match(document, brief_document)
        return r_document
        
    # @application
    # to be used to report to CustomerService by normal user
    def get_application_default(self):
        application = {
            'title':'',
            'userId':'',
            'type':'',
            'content':{},
            'time':'',
            'state':'',
            'handler':'',
            'illustrate':''
        }
        return application
    
    def brief_application(self, document, type = 'brief'):
        if type == 'brief':
            brief_document = {
                '_id':'',
                'title':'',
                'userId':'',
                'type':'',
                'content':'',
                'time':'',
                'state':'',
                'handler':'',
                'illustrate':''
            }
            r_document = self.dict_match(document, brief_document)
        return r_document
        
    # @event   
    # event ,like activity,lesson,service,appointment
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
            'serviceLead':'',    #说明
            'goalsText':'',
            'importantinfo':'',    #活动安排
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
        
    def brief_event(self, document, type = 'brief'):
        if type == 'brief':
            brief_document = {
                'type':'',
                '_id':'',
                'state':'',
                'location':'',
                'category':'',
                'slogan':'',
                'title':'',
                'goalsText':'',
                'importantinfo':'',
                'photosDisplay':[],
                'extendedPhotosTitle':'',
                'extendedPhotos':[],
                'price':'',
                'hour':'',
                'belongedMaster':'',
                'masterLabel':[],
                'masterIntroduction':'',
                'lastChangeTime':'',
                'eventLead':'',
                'unitName':'',
                'likeUserList':[],
                'commentList':[],
                'coverPhoto':'',
                'serviceLead':'',
            }
            r_document = self.dict_match(document, brief_document)
        return r_document

    # @order
    # order ,be used to pay real money for event
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
            'comment_id':'',
        }
        return order

    def brief_order(self, document, type = 'brief'):
        if type == 'brief':
            brief_document = {
                '_id':'',
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
                'remarkInfo':'',
                'ch_id':'',
                'refund_id':'',
                'realName':'',
                'realPhone':'',
                'removed':'',
                'comment_id':'',
            }
            r_document = self.dict_match(document, brief_document)
        return r_document

    # @tip
    # tip, be used as tip to master(Da Shang)
    def get_tip_default(self):
        tip = {
            'tipOrderNumber':'',
            'tipOrderTime':'',
            'payTime':'',
            'to_user':'',
            'from_user':'',
            'price':'',
            'state':'',
            'order_id':'',
            'to_event_id':'',
        }
        return tip
        
    def get_tip_order_default(self):
        return self.get_tip_default()
        
    def brief_tip(self, document, type = 'brief'):
        if type == 'brief':
            brief_document = {
                '_id':'',
                'tipOrderNumber':'',
                'tipOrderTime':'',
                'payTime':'',
                'to_user':'',
                'from_user':'',
                'price':'',
                'state':'',
                'order_id':'',
                'to_event_id':'',
            }
            r_document = self.dict_match(document, brief_document)
        return r_document
    
    # @category
    # be used to classify events
    def get_category_default(self):
        category={
            'title':'',
            'father':'',
            'type':'',
            'image':'',
            'foundtime':'',
        }
        return category
        
    def brief_category(self, document, type = 'brief'):
        if type == 'brief':
            brief_document = {
                '_id':'',
                'title':'',
                'father':'',
                'type':'',
                'image':'',
                'foundtime':'',
            }
            r_document = self.dict_match(document, brief_document)
        return r_document
        
    # @index
    # to be recommended by manager
    def get_index_default(self):
        index={
            'type':'',
            'contentId':'',
            'recommendDate':'',
            'state':'1',
            'position':''
        }
        return index
        
    def brief_index(self, document, type = 'brief'):
        if type == 'brief':
            brief_document = {
                '_id':'',
                'type':'',
                'contentId':'',
                'recommendDate':'',
                'state':'1',
                'position':''
            }
            r_document = self.dict_match(document, brief_document)
        return r_document
    
    # @banner
    # card to be shown in window
    def get_banner_default(self):
        banner={
            'state':'1',
            'type':'',
            'contentId':'',
            'content':'',
            'image':'',
            'time':'',
            'position':'',
        }
        return banner
        
    def brief_banner(self, document, type = 'brief'):
        if type == 'brief':
            brief_document = {
                '_id':'',
                'type':'',
                'contentId':'',
                'content':'',
                'image':'',
                'time':'',
                'state':'',
                'position':'',
            }
            r_document = self.dict_match(document, brief_document)
        return r_document
        
    # @post
    # post 
    def get_post_default(self):
        post={
            'title':'',
            'publisher':'',
            'content':'',
            'multiMedia':[],
            'likeUserList':[],
            'commentList':[],
            'publishTime':'',
            'type':'',
            'state':'',
            'pushTime':'',
            'isPush':'NO',
            'isSpecial':'no',
            'belongCircle':'',
            'belongCircleTitle':'',
            'seeNum':0,
            'belongCircleType':'',
            'isAffiche':'',
            'location':'',
        }
        return post
        
    def brief_post(self, document, type = 'brief'):
        if type == 'brief':
            brief_document = {
                '_id':'',
                'title':'',
                'publisher':'',
                'content':'',
                'multiMedia':[],
                'likeUserList':[],
                'commentList':[],
                'publishTime':'',
                'type':'',
                'state':'',
                'pushTime':'',
                'isPush':'',
                'isSpecial':'',
                'belongCircle':'',
                'belongCircleTitle':'',
                'seeNum':1,
                'belongCircleType':'',
                'location':'',
            }
            r_document = self.dict_match(document, brief_document)
        return r_document
        
    # @userteam
    #
    def get_userteam_default(self):
        userteam={
            'teamLeader':'',
            'teamMember':[],
        }
        return userteam
        
    def brief_userteam(self, document, type = 'brief'):
        if type == 'brief':
            brief_document = {
                '_id':'',
                'teamLeader':'',
                'teamMember':[],
            }
            r_document = self.dict_match(document, brief_document)
        return r_document
    # @comment
    # comment of post and order
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
        
    def brief_comment(self, document, type = 'brief'):
        if type == 'brief':
            brief_document = {
                '_id':'',
                'commenter':'',
                'commentType':'',
                'postId':'',
                'commentTime':'',
                'content':'',
                'multiMedia':[],
                'replyList':[],
                'likeUserList':[],
                'state':'',
                'star':[5.0,5.0,5.0],
                'orderId':'',
            }
            r_document = self.dict_match(document, brief_document)
        return r_document
        

    # @code
    # to phone check
    def get_code_default(self):
        code = {
            'mobile':mobile,
            'code_str':code_str,
            'time':time,
            'state':'on'
        }
        return code
    # @other
    def get_label_default(self):
        label = {
            'title':'',
            'userList':[],
            'state':'',
            'entryDate':'',
        }
        return label
    def get_reply_default(self):
        reply={
            'replyerId':'',
            'replyerName':'',
            'content':'',
            'replyTime':'',
        }
        return reply
    # @iconfig
    # config    
    def get_iconfig_default(self):
        iconfig={
            'title':'',
            'content':''
        }
        return iconfig
        
    # @task
    # ????
    def get_task_default(self):
        task={
            '_id':'',
            'master_id':'',
            'self_info':'undo',
            'achievement':'undo',
            'brief_introduction':'undo',
            'display_photo':'undo',
        }
        return task
