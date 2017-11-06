'''
0.上传图片获取图片url
1.创建category,保存categoryid
2.创建user，保存userid
3.创建达人，需要category id，保存达人的userid，6遍
4.创建课程，服务，活动，保存对应的id
4.创建index，创建banner
'''

import requests
import json
import time
#from uploadInfo3 import unitlist


managerToken = None
domain = 'https://api.idarenhui.com/wx'

managerName = 'manager'
managerPassword = 'seudaren'

def preLogin():
    if managerToken == None:
        managerLogin()


def uploadCategory(cate):
    preLogin()
    data = {'category':{'title':cate,'father':''}}
    headers = {'Content-Type':'application/json','Access_token':managerToken}
    r = requests.post(domain + "/v1.0/manager/category", data=json.dumps(data), headers=headers)
    print(r.text)
    return json.loads(r.text)['result']

def managerLogin():
    data = {"realName":managerName,"password":managerPassword}
    headers = {'Content-Type':'application/json'}
    r = requests.post(domain + "/v1.0/user/manager/login", data=json.dumps(data), headers=headers)
    print(r)
    res = json.loads(r.text)
    if(res['code'] == '0'):
        global managerToken
        managerToken = res['result']['utoken']['accessToken']
        return True
    else:
        print('login failed')
        return False


def getApplication():
    preLogin()
    headers = {'Content-Type':'application/json','Access_token':managerToken}
    r = requests.get(domain + "/v1.0/manager/application/all", headers=headers)
    print(r.text)

def approveApplication(applicationId):
    preLogin()
    headers = {'Content-Type':'application/json','Access_token':managerToken}
    data = {'application_id':applicationId,  'application':{'state':'approved'}}
    r = requests.put(domain + "/v1.0/manager/masterapplication", data=json.dumps(data), headers=headers)
    print('finish')
    print(r)

def getMasterInfo(userId):
    preLogin()
    headers = {'Content-Type':'application/json','Access_token':managerToken}
    data = {'user_id':userId}
    r = requests.get(domain + "/v1.0/manager/master", params=data,headers = headers)
    print(r)
    print(r.text)

def editMasterInfo(masterUserId, master):
    preLogin()
    headers = {'Content-Type':'application/json','Access_token':managerToken}
    data = {'user_id':masterUserId, 'master':master}
    r = requests.put(domain + "/v1.0/manager/master", data=json.dumps(data), headers=headers)
    print('finish')
    print(r)

def uploadEvent(event):
    preLogin()
    headers = {'Content-Type':'application/json','Access_token':managerToken}
    data = {
        'event':event
    }
    r = requests.post(domain + "/v1.0/manager/event", data=json.dumps(data), headers=headers)
    print(r.text)
    return json.loads(r.text)['result']

def getEventInfo(event_id):
    preLogin()
    headers = {'Content-Type':'application/json','Access_token':managerToken}
    data = {'event_id':event_id}
    r = requests.get(domain + "/v1.0/event", params=data,headers = headers)
    print(r)
    print(r.text)

def uploadIndex(index):
    preLogin()
    headers = {'Content-Type':'application/json','Access_token':managerToken}
    data = {'index':index}
    r = requests.post(domain + "/v1.0//manager/index", data=json.dumps(data),headers = headers)
    print(r)
    print(r.text)

def getIndex():
    preLogin()
    headers = {'Content-Type':'application/json','Access_token':managerToken}
    r = requests.get(domain + "/v1.0/index",headers = headers)
    print(r)
    print(r.text)

def uploadBanner(banner):
    preLogin()
    headers = {'Content-Type':'application/json','Access_token':managerToken}
    data = {    'banner':banner    }
    r = requests.post(domain + "/v1.0/manager/banner", data=json.dumps(data),headers = headers)
    print(r)
    print(r.text)

def getBanner():
    preLogin()
    headers = {'Content-Type':'application/json','Access_token':managerToken}
    r = requests.get(domain + "/v1.0/banner",headers = headers)
    print(r)
    print(r.text)

def registerUser(phone):

    headers = {'Content-Type':'application/json'}
    data = {'phone':phone,'code':'1','password':'12'}
    r = requests.post(domain+"/v1.0/user/register", data=json.dumps(data),headers = headers)
    print(r)
    print(r.text)
    return json.loads(r.text)['result']['userId']

def registerMaster(master, userId):
    preLogin()
    headers = {'Content-Type':'application/json','Access_token':managerToken}
    data = {'user_id':userId, 'master':master}
    r = requests.post(domain + "/v1.0/manager/user/toMaster", data=json.dumps(data), headers=headers)
    print(r)
    print(r.text)
    editMasterInfo(userId, master)
