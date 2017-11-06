from upload import *

#1. 创建category
print('www')
categoryId = list()  #4
categoryId.append(uploadCategory("绘画"))
print('www')

#2. 创建User
userId = list()  #8
for i in range(0,12):
    userId.append(registerUser(str(i+time.time())))

#3. 创建master
masterId = list() #8

for i in range(0,12):
    master = {"location" : "东南大学", 
    "coverPhoto" : "http://7xl53f.com1.z0.glb.clouddn.com/58a8f64690c4900ba468c03d",
    "masterLabel" : [ "5次获得LOFTER人像摄影加精", "第一届“视界东南”微视频大赛第一名获得者"],
    "phone" : "15943012334",
    "personalDetails" : "我是罗小林，电气学院大四学生。独立人像摄影师，摄影风格多变。15年6月买了人生第一台单反，依靠摄影赚来人生第二部单反。自学摄影一年零5个月，摄影作为副业，已经能够满足基本的生活支出。人称“美女收割机”，拥有无数的美女回头客，拯救了无数被男朋友的摄影技术黑到绝望的“失足少女”。LOFTER主页：http://doudou-seu.lofter.com", 
    "avatar" : "http://7xl53f.com1.z0.glb.clouddn.com/58a8ff6f90c4900ba468c049", 
    "category" : categoryId[0], 
    "masterPhoto" : ["http://7xl53f.com1.z0.glb.clouddn.com/58a8f5f090c4900ba468c034"
    ,"http://7xl53f.com1.z0.glb.clouddn.com/58a8f5f090c4900ba468c035"
    ,"http://7xl53f.com1.z0.glb.clouddn.com/58a8f5f090c4900ba468c036"
    ,"http://7xl53f.com1.z0.glb.clouddn.com/58a8f5f090c4900ba468c037"
    ,"http://7xl53f.com1.z0.glb.clouddn.com/58a8f5f190c4900ba468c038"
    ,"http://7xl53f.com1.z0.glb.clouddn.com/58a8f5f190c4900ba468c039"
    ,"http://7xl53f.com1.z0.glb.clouddn.com/58a8f5f190c4900ba468c03a"
    ,"http://7xl53f.com1.z0.glb.clouddn.com/58a8f5f190c4900ba468c03b"
    ,"http://7xl53f.com1.z0.glb.clouddn.com/58a8f5f190c4900ba468c03c"], 
    "state" : "on",
    "realName" : "罗小林", 
    "realTitle" : "独立人像摄影师"}
    registerMaster(master, userId[i])
    masterId.append(userId[i])

exit()
#4.创建event
eventId = list()

for i in range(len(categoryId)):
    # 4次迭代
    event= {
            'state':'on',       #事件状态  'new'/'on'/'off'  新创建/上架/下架
            'location':'东南大学九龙湖校区',
            'slogan':'不会PS？手机App也能修出人像大片！',       #事件一句话介绍
            'title':'如何拍好女朋友：A类',        #事件名称
            'eventLead':'课程主要针对没有单反的手机用户开设，课程采用“前期理论-外拍实践-后期处理”模式，力求在课程中通过理论与实践让学员学会如何拍摄优质的图片素材，学习手机修图的基本套路，能用App对照片进行修饰。',  #服务介绍
             
            'goalsText':'【课程安排】. \n课程一：2课时\n理论课：\n女朋友的内心戏：她想要你把她拍成什么样？\n那些肤白腿长有意境的照片时怎么拍的？\n什么样的照片才好看：人像摄影构图和用光其实很简单。\n拍出来总是游客照？几个小技巧让你的照片别具一格。\n不会PS？手机App也能修出人像大片！\n\n课程二：2课时\n实战教学\n提供“女朋友”，带你实实在在拍一次。\n\n课程三：2课时\n后期课，要求安装好Snapseed、VSCO以及美图秀秀上课。\n调色之前你要了解的色彩理论；\n手机修图除了套滤镜之外的其他打开方式；\n个人手机摄影作品前后期思路分享。',  
            'importantinfo':'【开课时间】\n上课时间暂定每周六的下午5人一个班，报满即开课；\n\n【注意事项】\n付款之后及时联系客服添加我微信',
            'photosDisplay':["http://7xl53f.com1.z0.glb.clouddn.com/58a8f73e90c4900ba468c040",
"http://7xl53f.com1.z0.glb.clouddn.com/58a8f73f90c4900ba468c041",
"http://7xl53f.com1.z0.glb.clouddn.com/58a8f74090c4900ba468c042"],#顶部图片
            'extendedPhotosTitle':'【作品展示】',
            'extendedPhotos':["http://7xl53f.com1.z0.glb.clouddn.com/58a8f74090c4900ba468c043",
"http://7xl53f.com1.z0.glb.clouddn.com/58a8f74090c4900ba468c044",
"http://7xl53f.com1.z0.glb.clouddn.com/58a8f74090c4900ba468c045",
"http://7xl53f.com1.z0.glb.clouddn.com/58a8f74090c4900ba468c046",
"http://7xl53f.com1.z0.glb.clouddn.com/58a8f74190c4900ba468c047",
"http://7xl53f.com1.z0.glb.clouddn.com/58a8f74190c4900ba468c048"],#学员展示图片
            'price':'0.1',        #事件价格
            'hour':'6',
        }
    event['category'] = categoryId[i]
    for master in [masterId[i], masterId[i+4]]:
        for eve in ['course', 'service','activity']:
            event['belongedMaster'] = master
            event['type'] = eve
            eventId.append(uploadEvent(event))

print(eventId)

#. 创建banner和index
for i in range(2):
    banner = {
        'type':'master',          #轮播图指向类型
        'contentId':masterId[i],     #轮播图指向ID
        'content':'content',       #轮播图说明
        'image':'http://7xl53f.com1.z0.glb.clouddn.com/58a8ff6f90c4900ba468c049'        #轮播图图片
        }
    uploadBanner(banner)
    banner['type']="event"
    banner['contentId']=eventId[i]
    uploadBanner(banner)

for i in range(6):
    index = {
        'type':'master',
        'contentId':masterId[i],
        'position':'1'
    }
    uploadIndex(index)
    index['type']='event'
    index['contentId']=eventId[i]
    uploadIndex(index)
