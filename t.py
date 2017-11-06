import urllib
import urllib2
import json
import time
url="https://api.idarenhui.com/wx_test"



#urlp=url+'/v1.0/event/index?type=appointment'
#urlp = url+'/v1.0/master?user_id=58b1ae9490c4902261436339'
#urlp = url+'/v1.0/new_banner'
#urlp = url+'/v1.0/vcoin/signup'
#urlp = url+'/v1.0/vcoin/getnumber'
#urlp = url+'/v1.0/vcoin/task '
urlp = url+'/v1.0/vcoin/signup'


#master_id: 58b1ae9490c490226143632d
#user_id: ObjectId("58b1ae9490c4902261436335")
#"accessToken" : 1de11a97-00f5-4fca-a68b-18933a44dfd3
#urlp = url + '/v1.0/order/master?event_id=58c1029890c4904799de14bc'
'''
print urlp
req=urllib2.Request(urlp)
req.add_header('Access_token','1de11a97-00f5-4fca-a68b-18933a44dfd3')#58b1ae9490c4902261436321
req.add_data(json.dumps({'typ':'appointment'}))
req.get_method = lambda: 'GET'
response=urllib2.urlopen(req)
jsonobj=json.loads(response.read())
print jsonobj
'''

user_id = '58b19a4090c49022614362d0'
user_token = '2d8a8357-fe03-42ed-b4c3-d987bfb94def'

#-----
master_id = '58b1ae9690c4902261436347' 
master_user_id = '58b1ae9490c4902261436339'
master_token = '0f415e3c-a6e4-4afa-b2e9-0f1e559bed70'
event_id = '58bbe6b690c4901ce496b679'




'''
#------
master_id = '58d13f9890c4904644f31689'
master_user_id = '58cfc11290c4904644f315e4'
master_token = '4a10f2e4-08b1-474e-a858-a9112212f80c'
event_id = '591d56f190c4907475732993'
'''

oneday_seconds = 60*60*24
present_time = time.time()
signup_list = []
for i in [1,2,3,4,5,6,7]:
    signup_list.append((present_time-i*oneday_seconds))
print signup_list


req=urllib2.Request(urlp)
req.add_header('Access_token',user_token)
req.get_method = lambda: 'GET'
response=urllib2.urlopen(req)
jsonobj=json.loads(response.read())
print jsonobj

def get_order_information(token):
    url="https://api.idarenhui.com/wx_test"
    urlp = url + '/v1.0/order/user'
    print urlp
    req=urllib2.Request(urlp)
    req.add_header('Access_token',token)
    req.get_method = lambda: 'GET'
    response=urllib2.urlopen(req)
    jsonobj=json.loads(response.read())
    print jsonobj

def get_my_vcoin(token):
    url="https://api.idarenhui.com/wx_test"
    urlp = url+'/v1.0/vcoin/getnumber'
    print urlp
    req=urllib2.Request(urlp)
    req.add_header('Access_token',token)
    req.get_method = lambda: 'GET'
    
    response=urllib2.urlopen(req)
    jsonobj=json.loads(response.read())
    print jsonobj


#------------------------------------------appointment
def user_appointment(token,event_id):
    url="https://api.idarenhui.com/wx_test"
    urlp = url + '/v1.0/appointment/user'
    print urlp
    req=urllib2.Request(urlp)
    req.add_header('Access_token',token)
    req.add_data(json.dumps({'event_id':event_id,'remarkInfo':'haha','realName':'keke','realPhone':'nana'}))
    req.get_method = lambda: 'POST'
    response=urllib2.urlopen(req)
    jsonobj=json.loads(response.read())
    print jsonobj

def master_confirm_appiontment(token,order_id):
    url="https://api.idarenhui.com/wx_test"
    urlp = url + '/v1.0/appointment/master'
    print urlp
    req=urllib2.Request(urlp)
    req.add_header('Access_token',token)
    req.add_data(json.dumps({'order_id':order_id}))
    req.get_method = lambda: 'POST'
    response=urllib2.urlopen(req)
    jsonobj=json.loads(response.read())
    print jsonobj

def master_finish_appointment(token,order_id):
    url = "https://api.idarenhui.com/wx_test"
    urlp = url + '/v1.0/appointment/master'
    print urlp
    req=urllib2.Request(urlp)
    req.add_header('Access_token',token)
    req.add_data(json.dumps({'order_id':order_id}))
    req.get_method = lambda: 'PUT'
    response=urllib2.urlopen(req)
    jsonobj=json.loads(response.read())
    print jsonobj

def user_comment_order(token):
    url="https://api.idarenhui.com/wx_test"
    urlp = url + '/v1.0/appointment/user'
    print urlp
    req=urllib2.Request(urlp)
    req.add_header('Access_token',token)
    req.add_data(json.dumps({'order_id':order_id}))
    req.get_method = lambda: 'GET'
    response=urllib2.urlopen(req)
    jsonobj=json.loads(response.read())
    print jsonobj

def user_appointment_refund(token,order_id):
    url="https://api.idarenhui.com/wx_test"
    urlp = url + '/v1.0/appointment/user'
    print urlp
    req=urllib2.Request(urlp)
    req.add_header('Access_token',token)
    req.add_data(json.dumps({'order_id':order_id}))
    req.get_method = lambda: 'DELETE'
    response=urllib2.urlopen(req)

def user_comment_order(token,event_id,order_id):
    url="https://api.idarenhui.com/wx_test"
    urlp = url + '/v1.0/comment'
    req=urllib2.Request(urlp)
    req.add_header('Access_token',token)
    comment = {
        'content':'caoishojd',
        'star':[4,3,5],
        'multiMedia':'',
        }
    req.add_data(json.dumps({'comment_type':'appointment','post_id':event_id,'order_id':order_id,'comment':comment,}))
    req.get_method = lambda: 'POST'
    response=urllib2.urlopen(req)


    urlp = url + '/v1.0/appointment/user' 
    req=urllib2.Request(urlp)
    req.add_header('Access_token',token)
    req.add_data(json.dumps({'order_id':order_id}))
    req.get_method = lambda: 'PUT'
    response=urllib2.urlopen(req)


def get_one_order(token,order_id):
    url="https://api.idarenhui.com/wx_test"
    urlp = url + '/v1.0/order?order_id=' + order_id
    print urlp
    req=urllib2.Request(urlp)
    req.add_header('Access_token',token)
    req.add_data(json.dumps({'order_id':order_id}))
    req.get_method = lambda: 'GET'
    response=urllib2.urlopen(req)
    jsonobj=json.loads(response.read())
    print jsonobj

def get_comment(token,order_id):
    url="https://api.idarenhui.com/wx_test"
    urlp = url + '/v1.0/order?order_id=' + order_id
    print urlp
    req=urllib2.Request(urlp)
    req.add_header('Access_token',token)
    req.add_data(json.dumps({'order_id':order_id}))
    req.get_method = lambda: 'GET'
    response=urllib2.urlopen(req)
    jsonobj=json.loads(response.read())
    print jsonobj

    comment_id = jsonobj['result']['comment_id']
    url="https://api.idarenhui.com/wx_test"
    urlp = url + '/v1.0/comment?comment_id=' + comment_id
    print urlp
    req=urllib2.Request(urlp)
    req.add_header('Access_token',token)
    req.add_data(json.dumps({'comment_id':comment_id}))
    req.get_method = lambda: 'GET'
    response=urllib2.urlopen(req)
    jsonobj=json.loads(response.read())
    print jsonobj

#---------------------------------------------order
def get_master_info(token,master_user_id):
    url="https://api.idarenhui.com/wx_test"
    urlp = url + '/v1.0/master?user_id='+master_user_id
    print urlp
    req=urllib2.Request(urlp)
    req.add_header('Access_token',token)
    req.get_method = lambda: 'GET'
    response=urllib2.urlopen(req)
    jsonobj=json.loads(response.read())
    print jsonobj['result']['total_money']

def user_create_order(token,event_id):
    url="https://api.idarenhui.com/wx_test"
    urlp = url + '/v1.0/order/user'
    print urlp
    req=urllib2.Request(urlp)
    req.add_header('Access_token',token)
    req.add_data(json.dumps({'event_id':event_id,'remarkInfo':'haha','realName':'keke','realPhone':'nana'}))
    req.get_method = lambda: 'POST'
    response=urllib2.urlopen(req)
    jsonobj=json.loads(response.read())
    print jsonobj

def master_confirm_order(token,order_id):
    url="https://api.idarenhui.com/wx_test"
    urlp = url + '/v1.0/order/master'
    print urlp
    req=urllib2.Request(urlp)
    req.add_header('Access_token',token)
    req.add_data(json.dumps({'order_id':order_id}))
    req.get_method = lambda: 'POST'
    response=urllib2.urlopen(req)
    jsonobj=json.loads(response.read())
    print jsonobj

def master_finish_order(token,order_id):
    url = "https://api.idarenhui.com/wx_test"
    urlp = url + '/v1.0/order/master'
    print urlp
    req=urllib2.Request(urlp)
    req.add_header('Access_token',token)
    req.add_data(json.dumps({'order_id':order_id}))
    req.get_method = lambda: 'PUT'
    response=urllib2.urlopen(req)
    jsonobj=json.loads(response.read())
    print jsonobj

def user_comment_order(token,event_id,order_id):
    url="https://api.idarenhui.com/wx_test"
    urlp = url + '/v1.0/comment'
    req=urllib2.Request(urlp)
    req.add_header('Access_token',token)
    comment = {
        'content':'caoishojd',
        'star':[4,3,5],
        'multiMedia':'',
        }
    req.add_data(json.dumps({'comment_type':'appointment','post_id':event_id,'order_id':order_id,'comment':comment,}))
    req.get_method = lambda: 'POST'
    response=urllib2.urlopen(req)


    urlp = url + '/v1.0/order/user' 
    req=urllib2.Request(urlp)
    req.add_header('Access_token',token)
    req.add_data(json.dumps({'order_id':order_id}))
    req.get_method = lambda: 'PUT'
    response=urllib2.urlopen(req)

#------------------------------------------favor
def user_favor(token,event_id):
    url="https://api.idarenhui.com/wx_test"
    urlp = url + '/v1.0/event/favor'
    req=urllib2.Request(urlp)
    req.add_header('Access_token',token)
    req.add_data(json.dumps({'event_id':event_id}))
    req.get_method = lambda: 'POST' 
    response=urllib2.urlopen(req)


#user_favor(user_token,event_id)



'''
get_my_vcoin(user_token)
get_order_information(user_token)
get_my_vcoin(user_token)
get_my_vcoin(master_token)
user_appointment(user_token,event_id)
get_my_vcoin(user_token)
get_my_vcoin(master_token)
get_order_information(user_token)
order_id_r = '591f50ec90c4903e7d7ff71d'
order_id = '591f50c790c4903e7d7ff71c'
master_confirm_appiontment(master_token,order_id)
get_my_vcoin(user_token)
get_my_vcoin(master_token)
get_order_information(user_token)
master_finish_appointment(master_token,order_id)
user_appointment_refund(user_token,order_id_r)
user_appointment_refund(user_token,order_id)
user_comment_order(user_token,event_id,order_id)
get_order_information(user_token)
get_my_vcoin(user_token)
get_my_vcoin(master_token)
user_comment_order(user_token)

get_one_order(user_token,order_id)
comment_id = '591f5d2290c4904865adbb9f'
get_comment(user_token,order_id)
'''
#get_master_info(master_token,master_user_id)
#user_create_order(user_token,event_id)
#get_order_information(user_token)
#get_master_info(master_token,master_user_id)
#order_id = '591f68f390c4904b00cc34c2'
#master_confirm_order(master_token,order_id)
#get_master_info(master_token,master_user_id)
#master_finish_order(master_token,order_id)
#get_master_info(master_token,master_user_id)
#user_comment_order(user_token,event_id,order_id)
#get_master_info(master_token,master_user_id)
#get_one_order(user_token,order_id)
#get_comment(user_token,order_id)





