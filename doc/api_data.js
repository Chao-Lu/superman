define({ "api": [
  {
    "type": "get",
    "url": "/v1.0/banner",
    "title": "获取首页轮播图",
    "group": "banner",
    "version": "1.0.0",
    "description": "<p>获取首页轮播图</p>",
    "permission": [
      {
        "name": "user"
      }
    ],
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "list",
            "optional": false,
            "field": "bannerlist",
            "description": "<p>轮播图</p>"
          }
        ]
      }
    },
    "filename": "handler/index.py",
    "groupTitle": "banner",
    "name": "GetV10Banner",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/banner"
      }
    ]
  },
  {
    "type": "DELETE",
    "url": "/v1.0/card/comment",
    "title": "删除卡片评论",
    "group": "card",
    "version": "1.0.0",
    "description": "<p>删除卡片评论</p>",
    "permission": [
      {
        "name": "user"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "comment_id",
            "description": "<p>评论ID</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "string",
            "optional": false,
            "field": "result",
            "description": "<p>&quot;OK&quot;</p>"
          }
        ]
      }
    },
    "filename": "handler/card.py",
    "groupTitle": "card",
    "name": "DeleteV10CardComment",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/card/comment"
      }
    ]
  },
  {
    "type": "DELETE",
    "url": "/v1.0/card/comment/like",
    "title": "评论取赞",
    "group": "card",
    "version": "1.0.0",
    "description": "<p>评论取赞</p>",
    "permission": [
      {
        "name": "user"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "comment_id",
            "description": "<p>评论ID</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "string",
            "optional": false,
            "field": "result",
            "description": "<p>&quot;OK&quot;</p>"
          }
        ]
      }
    },
    "filename": "handler/card.py",
    "groupTitle": "card",
    "name": "DeleteV10CardCommentLike",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/card/comment/like"
      }
    ]
  },
  {
    "type": "DELETE",
    "url": "/v1.0/card/reply",
    "title": "删除二级评论",
    "group": "card",
    "version": "1.0.0",
    "description": "<p>删除卡片评论</p>",
    "permission": [
      {
        "name": "user"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "object",
            "optional": false,
            "field": "reply",
            "description": "<p>二级评论</p>"
          },
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "comment_id",
            "description": "<p>所属评论ID</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "string",
            "optional": false,
            "field": "result",
            "description": "<p>&quot;OK&quot;</p>"
          }
        ]
      }
    },
    "filename": "handler/card.py",
    "groupTitle": "card",
    "name": "DeleteV10CardReply",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/card/reply"
      }
    ]
  },
  {
    "type": "get",
    "url": "/v1.0/card",
    "title": "获取卡片信息",
    "group": "card",
    "version": "1.0.0",
    "description": "<p>获取卡片信息</p>",
    "permission": [
      {
        "name": "all"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "card_id",
            "description": "<p>卡片id</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "card",
            "description": "<p>卡片信息</p>"
          }
        ]
      }
    },
    "filename": "handler/card.py",
    "groupTitle": "card",
    "name": "GetV10Card",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/card"
      }
    ]
  },
  {
    "type": "GET",
    "url": "/v1.0/card/comment",
    "title": "获取卡片评论",
    "group": "card",
    "version": "1.0.0",
    "description": "<p>获取卡片评论</p>",
    "permission": [
      {
        "name": "all"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "card_id",
            "description": "<p>卡片ID</p>"
          },
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "page",
            "description": "<p>页码</p>"
          },
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "pagesize",
            "description": "<p>页大小</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "list",
            "optional": false,
            "field": "commentlist",
            "description": "<p>卡片评论列表</p>"
          }
        ]
      }
    },
    "filename": "handler/card.py",
    "groupTitle": "card",
    "name": "GetV10CardComment",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/card/comment"
      }
    ]
  },
  {
    "type": "GET",
    "url": "/v1.0/card/comment/in",
    "title": "获取评论详情",
    "group": "card",
    "version": "1.0.0",
    "description": "<p>获取评论详情</p>",
    "permission": [
      {
        "name": "all"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "comment_id",
            "description": "<p>评论ID</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "list",
            "optional": false,
            "field": "comment",
            "description": "<p>评论详情</p>"
          }
        ]
      }
    },
    "filename": "handler/card.py",
    "groupTitle": "card",
    "name": "GetV10CardCommentIn",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/card/comment/in"
      }
    ]
  },
  {
    "type": "POST",
    "url": "/v1.0/card",
    "title": "上传卡片",
    "group": "card",
    "version": "1.0.0",
    "description": "<p>上传卡片</p>",
    "permission": [
      {
        "name": "master"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "object",
            "optional": false,
            "field": "card",
            "description": "<p>卡片信息</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "string",
            "optional": false,
            "field": "card_id",
            "description": ""
          }
        ]
      }
    },
    "filename": "handler/card.py",
    "groupTitle": "card",
    "name": "PostV10Card",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/card"
      }
    ]
  },
  {
    "type": "POST",
    "url": "/v1.0/card/comment",
    "title": "上传卡片评论",
    "group": "card",
    "version": "1.0.0",
    "description": "<p>上传卡片评论</p>",
    "permission": [
      {
        "name": "user"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "object",
            "optional": false,
            "field": "comment",
            "description": "<p>卡片评论</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "string",
            "optional": false,
            "field": "comment_id",
            "description": "<p>评论ID</p>"
          }
        ]
      }
    },
    "filename": "handler/card.py",
    "groupTitle": "card",
    "name": "PostV10CardComment",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/card/comment"
      }
    ]
  },
  {
    "type": "POST",
    "url": "/v1.0/card/comment/like",
    "title": "评论点赞",
    "group": "card",
    "version": "1.0.0",
    "description": "<p>评论点赞</p>",
    "permission": [
      {
        "name": "user"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "comment_id",
            "description": "<p>评论ID</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "string",
            "optional": false,
            "field": "result",
            "description": "<p>&quot;OK&quot;</p>"
          }
        ]
      }
    },
    "filename": "handler/card.py",
    "groupTitle": "card",
    "name": "PostV10CardCommentLike",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/card/comment/like"
      }
    ]
  },
  {
    "type": "POST",
    "url": "/v1.0/card/favormaster",
    "title": "获取关注达人的卡片",
    "group": "card",
    "version": "1.0.0",
    "description": "<p>获取关注达人的卡片</p>",
    "permission": [
      {
        "name": "user"
      }
    ],
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "list",
            "optional": false,
            "field": "cardlist",
            "description": "<p>卡片列表</p>"
          }
        ]
      }
    },
    "filename": "handler/card.py",
    "groupTitle": "card",
    "name": "PostV10CardFavormaster",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/card/favormaster"
      }
    ]
  },
  {
    "type": "POST",
    "url": "/v1.0/card/recommend",
    "title": "获取推荐卡片",
    "group": "card",
    "version": "1.0.0",
    "description": "<p>获取推荐卡片</p>",
    "permission": [
      {
        "name": "user"
      }
    ],
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "list",
            "optional": false,
            "field": "cardlist",
            "description": "<p>卡片列表</p>"
          }
        ]
      }
    },
    "filename": "handler/card.py",
    "groupTitle": "card",
    "name": "PostV10CardRecommend",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/card/recommend"
      }
    ]
  },
  {
    "type": "POST",
    "url": "/v1.0/card/reply",
    "title": "上传二级评论",
    "group": "card",
    "version": "1.0.0",
    "description": "<p>上传二级评论</p>",
    "permission": [
      {
        "name": "user"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "object",
            "optional": false,
            "field": "reply",
            "description": "<p>二级评论</p>"
          },
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "comment_id",
            "description": "<p>所属评论ID</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "string",
            "optional": false,
            "field": "result",
            "description": "<p>&quot;OK&quot;</p>"
          }
        ]
      }
    },
    "filename": "handler/card.py",
    "groupTitle": "card",
    "name": "PostV10CardReply",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/card/reply"
      }
    ]
  },
  {
    "type": "delete",
    "url": "/v1.0/cardholder",
    "title": "卡包信息删除",
    "group": "cardholder",
    "version": "1.0.0",
    "description": "<p>卡包信息删除</p>",
    "permission": [
      {
        "name": "user"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "card_id",
            "description": "<p>卡片id</p>"
          },
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "like",
            "description": "<p>Y/N:喜欢/不喜欢</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "string",
            "optional": false,
            "field": "result",
            "description": "<p>&quot;OK&quot;</p>"
          }
        ]
      }
    },
    "filename": "handler/cardholder.py",
    "groupTitle": "cardholder",
    "name": "DeleteV10Cardholder",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/cardholder"
      }
    ]
  },
  {
    "type": "get",
    "url": "/v1.0/cardholder",
    "title": "获取卡包(喜欢,不喜欢)",
    "group": "cardholder",
    "version": "1.0.0",
    "description": "<p>获取卡包(喜欢的卡片,不喜欢的卡片)</p>",
    "permission": [
      {
        "name": "user"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "like",
            "description": "<p>Y/N:喜欢/不喜欢</p>"
          },
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "page",
            "description": "<p>页码</p>"
          },
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "pagesize",
            "description": "<p>页大小</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "list",
            "optional": false,
            "field": "cardlist",
            "description": "<p>卡片列表</p>"
          }
        ]
      }
    },
    "filename": "handler/cardholder.py",
    "groupTitle": "cardholder",
    "name": "GetV10Cardholder",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/cardholder"
      }
    ]
  },
  {
    "type": "post",
    "url": "/v1.0/cardholder",
    "title": "卡包信息添加",
    "group": "cardholder",
    "version": "1.0.0",
    "description": "<p>卡包信息添加</p>",
    "permission": [
      {
        "name": "user"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "card_id",
            "description": "<p>卡片id</p>"
          },
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "like",
            "description": "<p>Y/N:喜欢/不喜欢</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "string",
            "optional": false,
            "field": "result",
            "description": "<p>&quot;OK&quot;</p>"
          }
        ]
      }
    },
    "filename": "handler/cardholder.py",
    "groupTitle": "cardholder",
    "name": "PostV10Cardholder",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/cardholder"
      }
    ]
  },
  {
    "type": "delete",
    "url": "/v1.0/event/favor",
    "title": "去除喜欢的事件",
    "group": "event",
    "version": "1.0.0",
    "description": "<p>去除喜欢的事件</p>",
    "permission": [
      {
        "name": "user"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "event_id",
            "description": "<p>事件ID</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "string",
            "optional": false,
            "field": "result",
            "description": "<p>'OK'</p>"
          }
        ]
      }
    },
    "filename": "handler/event.py",
    "groupTitle": "event",
    "name": "DeleteV10EventFavor",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/event/favor"
      }
    ]
  },
  {
    "type": "get",
    "url": "/v1.0/event",
    "title": "获取事件详情(用户)",
    "group": "event",
    "version": "1.0.0",
    "description": "<p>获取事件详情(用户)</p>",
    "permission": [
      {
        "name": "user"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "event_id",
            "description": "<p>事件ID</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "object",
            "optional": false,
            "field": "event",
            "description": "<p>事件详情</p>"
          }
        ]
      }
    },
    "filename": "handler/event.py",
    "groupTitle": "event",
    "name": "GetV10Event",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/event"
      }
    ]
  },
  {
    "type": "get",
    "url": "/v1.0/event/favor",
    "title": "获取喜欢的事件",
    "group": "event",
    "version": "1.0.0",
    "description": "<p>获取喜欢的事件</p>",
    "permission": [
      {
        "name": "user"
      }
    ],
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "list",
            "optional": false,
            "field": "eventlist",
            "description": ""
          }
        ]
      }
    },
    "filename": "handler/event.py",
    "groupTitle": "event",
    "name": "GetV10EventFavor",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/event/favor"
      }
    ]
  },
  {
    "type": "get",
    "url": "/v1.0/event/master",
    "title": "获取事件详情(达人)",
    "group": "event",
    "version": "1.0.0",
    "description": "<p>获取事件详情(达人)</p>",
    "permission": [
      {
        "name": "user"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "event_id",
            "description": "<p>事件ID</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "object",
            "optional": false,
            "field": "event",
            "description": "<p>事件详情</p>"
          }
        ]
      }
    },
    "filename": "handler/event.py",
    "groupTitle": "event",
    "name": "GetV10EventMaster",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/event/master"
      }
    ]
  },
  {
    "type": "post",
    "url": "/v1.0/event/favor",
    "title": "添加喜欢的事件",
    "group": "event",
    "version": "1.0.0",
    "description": "<p>添加喜欢的事件</p>",
    "permission": [
      {
        "name": "user"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "event_id",
            "description": "<p>事件ID</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "string",
            "optional": false,
            "field": "result",
            "description": "<p>'OK'</p>"
          }
        ]
      }
    },
    "filename": "handler/event.py",
    "groupTitle": "event",
    "name": "PostV10EventFavor",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/event/favor"
      }
    ]
  },
  {
    "type": "post",
    "url": "/v1.0/event/master",
    "title": "达人处理事件",
    "group": "event",
    "version": "1.0.0",
    "description": "<p>达人处理事件</p>",
    "permission": [
      {
        "name": "user"
      }
    ],
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "string",
            "optional": false,
            "field": "result",
            "description": "<p>&quot;OK&quot;</p>"
          }
        ]
      }
    },
    "filename": "handler/event.py",
    "groupTitle": "event",
    "name": "PostV10EventMaster",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/event/master"
      }
    ]
  },
  {
    "type": "get",
    "url": "/v1.0/index",
    "title": "获取首页推荐列表",
    "group": "index",
    "version": "1.0.0",
    "description": "<p>获取首页推荐列表</p>",
    "permission": [
      {
        "name": "user"
      }
    ],
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "list",
            "optional": false,
            "field": "indexlist",
            "description": "<p>首页推荐列表</p>"
          }
        ]
      }
    },
    "filename": "handler/index.py",
    "groupTitle": "index",
    "name": "GetV10Index",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/index"
      }
    ]
  },
  {
    "type": "delete",
    "url": "/v1.0/manager/card",
    "title": "删除卡片",
    "group": "manager",
    "version": "1.0.0",
    "description": "<p>删除卡片</p>",
    "permission": [
      {
        "name": "manager"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "card_id",
            "description": "<p>卡片ID</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "string",
            "optional": false,
            "field": "result",
            "description": "<p>&quot;OK&quot;</p>"
          }
        ]
      }
    },
    "filename": "handler/superside/card.py",
    "groupTitle": "manager",
    "name": "DeleteV10ManagerCard",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/manager/card"
      }
    ]
  },
  {
    "type": "delete",
    "url": "/v1.0/manager/category",
    "title": "删除类别",
    "group": "manager",
    "version": "1.0.0",
    "description": "<p>删除类别</p>",
    "permission": [
      {
        "name": "manager"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "category_id",
            "description": "<p>类别ID</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "string",
            "optional": false,
            "field": "result",
            "description": "<p>&quot;OK&quot;</p>"
          }
        ]
      }
    },
    "filename": "handler/superside/category.py",
    "groupTitle": "manager",
    "name": "DeleteV10ManagerCategory",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/manager/category"
      }
    ]
  },
  {
    "type": "delete",
    "url": "/v1.0/manager/event",
    "title": "删除事件",
    "group": "manager",
    "version": "1.0.0",
    "description": "<p>删除事件</p>",
    "permission": [
      {
        "name": "manager"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "event_id",
            "description": "<p>事件ID</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "string",
            "optional": false,
            "field": "result",
            "description": "<p>&quot;OK&quot;</p>"
          }
        ]
      }
    },
    "filename": "handler/superside/event.py",
    "groupTitle": "manager",
    "name": "DeleteV10ManagerEvent",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/manager/event"
      }
    ]
  },
  {
    "type": "delete",
    "url": "/v1.0/manager/index",
    "title": "删除首页推荐",
    "group": "manager",
    "version": "1.0.0",
    "description": "<p>删除首页推荐</p>",
    "permission": [
      {
        "name": "manager"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "index_id",
            "description": "<p>首页推荐ID</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "string",
            "optional": false,
            "field": "result",
            "description": "<p>&quot;OK&quot;</p>"
          }
        ]
      }
    },
    "filename": "handler/superside/index.py",
    "groupTitle": "manager",
    "name": "DeleteV10ManagerIndex",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/manager/index"
      }
    ]
  },
  {
    "type": "delete",
    "url": "/v1.0/manager/team",
    "title": "删除小组",
    "group": "manager",
    "version": "1.0.0",
    "description": "<p>删除小组</p>",
    "permission": [
      {
        "name": "manager"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "team_id",
            "description": "<p>小组ID</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "string",
            "optional": false,
            "field": "result",
            "description": "<p>&quot;OK&quot;</p>"
          }
        ]
      }
    },
    "filename": "handler/superside/team.py",
    "groupTitle": "manager",
    "name": "DeleteV10ManagerTeam",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/manager/team"
      }
    ]
  },
  {
    "type": "delete",
    "url": "/v1.0/manager/team/manager",
    "title": "删除小组管理员",
    "group": "manager",
    "version": "1.0.0",
    "description": "<p>删除小组管理员</p>",
    "permission": [
      {
        "name": "manager"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "team_id",
            "description": "<p>小组ID</p>"
          },
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "leaderId",
            "description": "<p>管理员ID</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "string",
            "optional": false,
            "field": "result",
            "description": "<p>&quot;OK&quot;</p>"
          }
        ]
      }
    },
    "filename": "handler/superside/team.py",
    "groupTitle": "manager",
    "name": "DeleteV10ManagerTeamManager",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/manager/team/manager"
      }
    ]
  },
  {
    "type": "get",
    "url": "/v1.0/event/all",
    "title": "获取事件列表",
    "group": "manager",
    "version": "1.0.0",
    "description": "<p>获取事件列表</p>",
    "permission": [
      {
        "name": "manager"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "condition",
            "description": ""
          },
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "sortby",
            "description": ""
          },
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "sort",
            "description": ""
          },
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "limit",
            "description": ""
          },
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "skip",
            "description": ""
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "eventlist",
            "description": "<p>事件列表</p>"
          }
        ]
      }
    },
    "filename": "handler/event.py",
    "groupTitle": "manager",
    "name": "GetV10EventAll",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/event/all"
      }
    ]
  },
  {
    "type": "get",
    "url": "/v1.0/event/index",
    "title": "获取所有事件列表",
    "group": "manager",
    "version": "1.0.0",
    "description": "<p>获取事件列表</p>",
    "permission": [
      {
        "name": "manager"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "type",
            "description": ""
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "eventlist",
            "description": "<p>事件列表</p>"
          }
        ]
      }
    },
    "filename": "handler/event.py",
    "groupTitle": "manager",
    "name": "GetV10EventIndex",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/event/index"
      }
    ]
  },
  {
    "type": "get",
    "url": "/v1.0/manager/application",
    "title": "获取申请信息",
    "group": "manager",
    "version": "1.0.0",
    "description": "<p>获取申请信息</p>",
    "permission": [
      {
        "name": "manager"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "application_id",
            "description": ""
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "application",
            "description": "<p>申请信息</p>"
          }
        ]
      }
    },
    "filename": "handler/superside/application.py",
    "groupTitle": "manager",
    "name": "GetV10ManagerApplication",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/manager/application"
      }
    ]
  },
  {
    "type": "get",
    "url": "/v1.0/manager/application/all",
    "title": "获取申请列表",
    "group": "manager",
    "version": "1.0.0",
    "description": "<p>获取申请列表</p>",
    "permission": [
      {
        "name": "manager"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "condition",
            "description": ""
          },
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "sortby",
            "description": ""
          },
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "sort",
            "description": ""
          },
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "limit",
            "description": ""
          },
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "skip",
            "description": ""
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "applicationlist",
            "description": "<p>申请信息</p>"
          }
        ]
      }
    },
    "filename": "handler/superside/application.py",
    "groupTitle": "manager",
    "name": "GetV10ManagerApplicationAll",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/manager/application/all"
      }
    ]
  },
  {
    "type": "get",
    "url": "/v1.0/manager/banner",
    "title": "获取轮播图列表",
    "group": "manager",
    "version": "1.0.0",
    "description": "<p>获取轮播图列表</p>",
    "permission": [
      {
        "name": "manager"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "condition",
            "description": ""
          },
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "sortby",
            "description": ""
          },
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "sort",
            "description": ""
          },
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "limit",
            "description": ""
          },
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "skip",
            "description": ""
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "bannerlist",
            "description": "<p>轮播图列表</p>"
          }
        ]
      }
    },
    "filename": "handler/superside/index.py",
    "groupTitle": "manager",
    "name": "GetV10ManagerBanner",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/manager/banner"
      }
    ]
  },
  {
    "type": "get",
    "url": "/v1.0/manager/card",
    "title": "获取卡片信息",
    "group": "manager",
    "version": "1.0.0",
    "description": "<p>获取卡片信息</p>",
    "permission": [
      {
        "name": "manager"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "card_id",
            "description": "<p>卡片ID</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "card",
            "description": "<p>卡片信息</p>"
          }
        ]
      }
    },
    "filename": "handler/superside/card.py",
    "groupTitle": "manager",
    "name": "GetV10ManagerCard",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/manager/card"
      }
    ]
  },
  {
    "type": "get",
    "url": "/v1.0/manager/card/all",
    "title": "获取卡片列表",
    "group": "manager",
    "version": "1.0.0",
    "description": "<p>获取卡片列表</p>",
    "permission": [
      {
        "name": "manager"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "condition",
            "description": ""
          },
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "sortby",
            "description": ""
          },
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "sort",
            "description": ""
          },
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "limit",
            "description": ""
          },
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "skip",
            "description": ""
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "cardlist",
            "description": "<p>卡片信息</p>"
          }
        ]
      }
    },
    "filename": "handler/superside/card.py",
    "groupTitle": "manager",
    "name": "GetV10ManagerCardAll",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/manager/card/all"
      }
    ]
  },
  {
    "type": "get",
    "url": "/v1.0/manager/category/all",
    "title": "获取类别列表",
    "group": "manager",
    "version": "1.0.0",
    "description": "<p>获取类别列表</p>",
    "permission": [
      {
        "name": "manager"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "condition",
            "description": ""
          },
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "sortby",
            "description": ""
          },
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "sort",
            "description": ""
          },
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "limit",
            "description": ""
          },
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "skip",
            "description": ""
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "list",
            "optional": false,
            "field": "categorylist",
            "description": "<p>类别信息</p>"
          }
        ]
      }
    },
    "filename": "handler/superside/category.py",
    "groupTitle": "manager",
    "name": "GetV10ManagerCategoryAll",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/manager/category/all"
      }
    ]
  },
  {
    "type": "get",
    "url": "/v1.0/manager/event",
    "title": "获取事件信息",
    "group": "manager",
    "version": "1.0.0",
    "description": "<p>获取事件信息</p>",
    "permission": [
      {
        "name": "manager"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "event_id",
            "description": "<p>事件ID</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "event",
            "description": "<p>事件信息</p>"
          }
        ]
      }
    },
    "filename": "handler/superside/event.py",
    "groupTitle": "manager",
    "name": "GetV10ManagerEvent",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/manager/event"
      }
    ]
  },
  {
    "type": "get",
    "url": "/v1.0/manager/event/all",
    "title": "获取事件列表",
    "group": "manager",
    "version": "1.0.0",
    "description": "<p>获取事件列表</p>",
    "permission": [
      {
        "name": "manager"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "condition",
            "description": ""
          },
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "sortby",
            "description": ""
          },
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "sort",
            "description": ""
          },
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "limit",
            "description": ""
          },
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "skip",
            "description": ""
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "eventlist",
            "description": "<p>事件信息</p>"
          }
        ]
      }
    },
    "filename": "handler/superside/event.py",
    "groupTitle": "manager",
    "name": "GetV10ManagerEventAll",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/manager/event/all"
      }
    ]
  },
  {
    "type": "get",
    "url": "/v1.0/manager/index",
    "title": "获取首页推荐信息",
    "group": "manager",
    "version": "1.0.0",
    "description": "<p>获取首页推荐信息</p>",
    "permission": [
      {
        "name": "manager"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "index_id",
            "description": "<p>首页推荐ID</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "index",
            "description": "<p>首页推荐信息</p>"
          }
        ]
      }
    },
    "filename": "handler/superside/index.py",
    "groupTitle": "manager",
    "name": "GetV10ManagerIndex",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/manager/index"
      }
    ]
  },
  {
    "type": "get",
    "url": "/v1.0/manager/index/all",
    "title": "获取首页推荐列表",
    "group": "manager",
    "version": "1.0.0",
    "description": "<p>获取首页推荐列表</p>",
    "permission": [
      {
        "name": "manager"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "condition",
            "description": ""
          },
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "sortby",
            "description": ""
          },
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "sort",
            "description": ""
          },
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "limit",
            "description": ""
          },
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "skip",
            "description": ""
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "indexlist",
            "description": "<p>首页推荐信息</p>"
          }
        ]
      }
    },
    "filename": "handler/superside/index.py",
    "groupTitle": "manager",
    "name": "GetV10ManagerIndexAll",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/manager/index/all"
      }
    ]
  },
  {
    "type": "get",
    "url": "/v1.0/manager/master",
    "title": "获取达人信息",
    "group": "manager",
    "version": "1.0.0",
    "description": "<p>获取达人信息</p>",
    "permission": [
      {
        "name": "manager"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "user_id",
            "description": "<p>用户ID</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "master",
            "description": "<p>达人信息</p>"
          }
        ]
      }
    },
    "filename": "handler/superside/master.py",
    "groupTitle": "manager",
    "name": "GetV10ManagerMaster",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/manager/master"
      }
    ]
  },
  {
    "type": "get",
    "url": "/v1.0/manager/master/all",
    "title": "获取达人列表",
    "group": "manager",
    "version": "1.0.0",
    "description": "<p>获取达人列表</p>",
    "permission": [
      {
        "name": "manager"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "condition",
            "description": ""
          },
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "sortby",
            "description": ""
          },
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "sort",
            "description": ""
          },
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "limit",
            "description": ""
          },
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "skip",
            "description": ""
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "masterlist",
            "description": "<p>达人信息</p>"
          }
        ]
      }
    },
    "filename": "handler/superside/master.py",
    "groupTitle": "manager",
    "name": "GetV10ManagerMasterAll",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/manager/master/all"
      }
    ]
  },
  {
    "type": "get",
    "url": "/v1.0/manager/order",
    "title": "获取订单信息",
    "group": "manager",
    "version": "1.0.0",
    "description": "<p>获取订单信息</p>",
    "permission": [
      {
        "name": "manager"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "order_id",
            "description": "<p>订单ID</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "order",
            "description": "<p>订单信息</p>"
          }
        ]
      }
    },
    "filename": "handler/superside/order.py",
    "groupTitle": "manager",
    "name": "GetV10ManagerOrder",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/manager/order"
      }
    ]
  },
  {
    "type": "get",
    "url": "/v1.0/manager/order/all",
    "title": "获取订单列表",
    "group": "manager",
    "version": "1.0.0",
    "description": "<p>获取订单列表</p>",
    "permission": [
      {
        "name": "manager"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "condition",
            "description": ""
          },
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "sortby",
            "description": ""
          },
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "sort",
            "description": ""
          },
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "limit",
            "description": ""
          },
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "skip",
            "description": ""
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "orderlist",
            "description": "<p>订单信息</p>"
          }
        ]
      }
    },
    "filename": "handler/superside/order.py",
    "groupTitle": "manager",
    "name": "GetV10ManagerOrderAll",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/manager/order/all"
      }
    ]
  },
  {
    "type": "get",
    "url": "/v1.0/manager/team",
    "title": "获取小组信息",
    "group": "manager",
    "version": "1.0.0",
    "description": "<p>获取小组信息</p>",
    "permission": [
      {
        "name": "manager"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "team_id",
            "description": "<p>小组ID</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "team",
            "description": "<p>小组信息</p>"
          }
        ]
      }
    },
    "filename": "handler/superside/team.py",
    "groupTitle": "manager",
    "name": "GetV10ManagerTeam",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/manager/team"
      }
    ]
  },
  {
    "type": "get",
    "url": "/v1.0/manager/team/all",
    "title": "获取小组列表",
    "group": "manager",
    "version": "1.0.0",
    "description": "<p>获取小组列表</p>",
    "permission": [
      {
        "name": "manager"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "condition",
            "description": ""
          },
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "sortby",
            "description": ""
          },
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "sort",
            "description": ""
          },
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "limit",
            "description": ""
          },
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "skip",
            "description": ""
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "cardlist",
            "description": "<p>小组信息</p>"
          }
        ]
      }
    },
    "filename": "handler/superside/team.py",
    "groupTitle": "manager",
    "name": "GetV10ManagerTeamAll",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/manager/team/all"
      }
    ]
  },
  {
    "type": "get",
    "url": "/v1.0/manager/user",
    "title": "获取用户信息",
    "group": "manager",
    "version": "1.0.0",
    "description": "<p>获取用户信息</p>",
    "permission": [
      {
        "name": "manager"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "user_id",
            "description": ""
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "user",
            "description": "<p>用户信息</p>"
          }
        ]
      }
    },
    "filename": "handler/superside/user.py",
    "groupTitle": "manager",
    "name": "GetV10ManagerUser",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/manager/user"
      }
    ]
  },
  {
    "type": "get",
    "url": "/v1.0/manager/user/all",
    "title": "获取用户列表",
    "group": "manager",
    "version": "1.0.0",
    "description": "<p>获取用户列表</p>",
    "permission": [
      {
        "name": "manager"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "condition",
            "description": ""
          },
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "sortby",
            "description": ""
          },
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "sort",
            "description": ""
          },
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "limit",
            "description": ""
          },
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "skip",
            "description": ""
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "userlist",
            "description": "<p>用户信息</p>"
          }
        ]
      }
    },
    "filename": "handler/superside/user.py",
    "groupTitle": "manager",
    "name": "GetV10ManagerUserAll",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/manager/user/all"
      }
    ]
  },
  {
    "type": "get",
    "url": "/v1.0/master/all",
    "title": "获取达人列表",
    "group": "manager",
    "version": "1.0.0",
    "description": "<p>获取达人列表</p>",
    "permission": [
      {
        "name": "manager"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "condition",
            "description": ""
          },
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "sortby",
            "description": ""
          },
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "sort",
            "description": ""
          },
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "limit",
            "description": ""
          },
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "skip",
            "description": ""
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "masterlist",
            "description": "<p>达人信息</p>"
          }
        ]
      }
    },
    "filename": "handler/master.py",
    "groupTitle": "manager",
    "name": "GetV10MasterAll",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/master/all"
      }
    ]
  },
  {
    "type": "get",
    "url": "/v1.0/master/index",
    "title": "获取所有达人列表",
    "group": "manager",
    "version": "1.0.0",
    "description": "<p>获取所有达人列表</p>",
    "permission": [
      {
        "name": "manager"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "type",
            "description": ""
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "masterlist",
            "description": "<p>达人列表</p>"
          }
        ]
      }
    },
    "filename": "handler/master.py",
    "groupTitle": "manager",
    "name": "GetV10MasterIndex",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/master/index"
      }
    ]
  },
  {
    "type": "post",
    "url": "/v1.0/manager/banner",
    "title": "上传轮播图",
    "group": "manager",
    "version": "1.0.0",
    "description": "<p>上传轮播图</p>",
    "permission": [
      {
        "name": "manager"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "Object",
            "optional": false,
            "field": "banner",
            "description": "<p>轮播图</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "string",
            "optional": false,
            "field": "banner_id",
            "description": "<p>轮播图ID</p>"
          }
        ]
      }
    },
    "filename": "handler/superside/index.py",
    "groupTitle": "manager",
    "name": "PostV10ManagerBanner",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/manager/banner"
      }
    ]
  },
  {
    "type": "post",
    "url": "/v1.0/manager/category",
    "title": "上传类别",
    "group": "manager",
    "version": "1.0.0",
    "description": "<p>上传类别</p>",
    "permission": [
      {
        "name": "manager"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "Object",
            "optional": false,
            "field": "category",
            "description": "<p>类别内容</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "string",
            "optional": false,
            "field": "category_id",
            "description": "<p>类别Id</p>"
          }
        ]
      }
    },
    "filename": "handler/superside/category.py",
    "groupTitle": "manager",
    "name": "PostV10ManagerCategory",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/manager/category"
      }
    ]
  },
  {
    "type": "post",
    "url": "/v1.0/manager/event",
    "title": "上传事件",
    "group": "manager",
    "version": "1.0.0",
    "description": "<p>上传事件</p>",
    "permission": [
      {
        "name": "manager"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "event",
            "description": "<p>事件</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "string",
            "optional": false,
            "field": "event_id",
            "description": "<p>事件ID</p>"
          }
        ]
      }
    },
    "filename": "handler/superside/event.py",
    "groupTitle": "manager",
    "name": "PostV10ManagerEvent",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/manager/event"
      }
    ]
  },
  {
    "type": "post",
    "url": "/v1.0/manager/index",
    "title": "上传首页推荐",
    "group": "manager",
    "version": "1.0.0",
    "description": "<p>上传首页推荐</p>",
    "permission": [
      {
        "name": "manager"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "Object",
            "optional": false,
            "field": "index",
            "description": "<p>首页推荐</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "string",
            "optional": false,
            "field": "index_id",
            "description": "<p>首页推荐ID</p>"
          }
        ]
      }
    },
    "filename": "handler/superside/index.py",
    "groupTitle": "manager",
    "name": "PostV10ManagerIndex",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/manager/index"
      }
    ]
  },
  {
    "type": "post",
    "url": "/v1.0/manager/order",
    "title": "完成订单",
    "group": "manager",
    "version": "1.0.0",
    "description": "<p>完成订单</p>",
    "permission": [
      {
        "name": "manager"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "order_id",
            "description": "<p>订单ID</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "result",
            "description": "<p>'OK'</p>"
          }
        ]
      }
    },
    "filename": "handler/superside/order.py",
    "groupTitle": "manager",
    "name": "PostV10ManagerOrder",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/manager/order"
      }
    ]
  },
  {
    "type": "post",
    "url": "/v1.0/manager/order/refund",
    "title": "订单退款",
    "group": "manager",
    "version": "1.0.0",
    "description": "<p>订单退款</p>",
    "permission": [
      {
        "name": "manager"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "order_id",
            "description": "<p>订单ID</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "string",
            "optional": false,
            "field": "result",
            "description": "<p>&quot;OK&quot;</p>"
          }
        ]
      }
    },
    "filename": "handler/superside/order.py",
    "groupTitle": "manager",
    "name": "PostV10ManagerOrderRefund",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/manager/order/refund"
      }
    ]
  },
  {
    "type": "post",
    "url": "/v1.0/manager/team",
    "title": "创建小组",
    "group": "manager",
    "version": "1.0.0",
    "description": "<p>创建小组</p>",
    "permission": [
      {
        "name": "manager"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "Object",
            "optional": false,
            "field": "team",
            "description": "<p>小组内容</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "string",
            "optional": false,
            "field": "team_id",
            "description": "<p>小组Id</p>"
          }
        ]
      }
    },
    "filename": "handler/superside/team.py",
    "groupTitle": "manager",
    "name": "PostV10ManagerTeam",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/manager/team"
      }
    ]
  },
  {
    "type": "post",
    "url": "/v1.0/manager/team/manager",
    "title": "添加小组管理员",
    "group": "manager",
    "version": "1.0.0",
    "description": "<p>添加小组管理员</p>",
    "permission": [
      {
        "name": "manager"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "team_id",
            "description": "<p>小组ID</p>"
          },
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "leaderId",
            "description": "<p>管理员ID</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "string",
            "optional": false,
            "field": "result",
            "description": "<p>&quot;OK&quot;</p>"
          }
        ]
      }
    },
    "filename": "handler/superside/team.py",
    "groupTitle": "manager",
    "name": "PostV10ManagerTeamManager",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/manager/team/manager"
      }
    ]
  },
  {
    "type": "post",
    "url": "/v1.0/manager/user/toMaster",
    "title": "用户升级为达人",
    "group": "manager",
    "version": "1.0.0",
    "description": "<p>用户升级为达人</p>",
    "permission": [
      {
        "name": "manager"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "Object",
            "optional": false,
            "field": "user_id",
            "description": "<p>用户id</p>"
          },
          {
            "group": "Parameter",
            "type": "Object",
            "optional": false,
            "field": "master",
            "description": "<p>达人信息</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "string",
            "optional": false,
            "field": "result",
            "description": "<p>&quot;OK&quot;</p>"
          }
        ]
      }
    },
    "filename": "handler/superside/user.py",
    "groupTitle": "manager",
    "name": "PostV10ManagerUserTomaster",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/manager/user/toMaster"
      }
    ]
  },
  {
    "type": "put",
    "url": "/v1.0/manager/application",
    "title": "更改申请信息",
    "group": "manager",
    "version": "1.0.0",
    "description": "<p>更改申请信息</p>",
    "permission": [
      {
        "name": "manager"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "application_id",
            "description": ""
          },
          {
            "group": "Parameter",
            "type": "Object",
            "optional": false,
            "field": "application",
            "description": ""
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "string",
            "optional": false,
            "field": "result",
            "description": "<p>&quot;OK&quot;</p>"
          }
        ]
      }
    },
    "filename": "handler/superside/application.py",
    "groupTitle": "manager",
    "name": "PutV10ManagerApplication",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/manager/application"
      }
    ]
  },
  {
    "type": "put",
    "url": "/v1.0/manager/banner",
    "title": "更改轮播图信息",
    "group": "manager",
    "version": "1.0.0",
    "description": "<p>更改轮播图信息</p>",
    "permission": [
      {
        "name": "manager"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "banner_id",
            "description": "<p>轮播图ID</p>"
          },
          {
            "group": "Parameter",
            "type": "Object",
            "optional": false,
            "field": "banner",
            "description": "<p>更改内容</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "string",
            "optional": false,
            "field": "result",
            "description": "<p>&quot;OK&quot;</p>"
          }
        ]
      }
    },
    "filename": "handler/superside/index.py",
    "groupTitle": "manager",
    "name": "PutV10ManagerBanner",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/manager/banner"
      }
    ]
  },
  {
    "type": "put",
    "url": "/v1.0/manager/card",
    "title": "更改卡片信息",
    "group": "manager",
    "version": "1.0.0",
    "description": "<p>更改卡片信息</p>",
    "permission": [
      {
        "name": "manager"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "card_id",
            "description": "<p>卡片ID</p>"
          },
          {
            "group": "Parameter",
            "type": "Object",
            "optional": false,
            "field": "card",
            "description": "<p>更改内容</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "string",
            "optional": false,
            "field": "result",
            "description": "<p>&quot;OK&quot;</p>"
          }
        ]
      }
    },
    "filename": "handler/superside/card.py",
    "groupTitle": "manager",
    "name": "PutV10ManagerCard",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/manager/card"
      }
    ]
  },
  {
    "type": "put",
    "url": "/v1.0/manager/category",
    "title": "更改类别信息",
    "group": "manager",
    "version": "1.0.0",
    "description": "<p>更改类别信息</p>",
    "permission": [
      {
        "name": "manager"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "category_id",
            "description": "<p>类别ID</p>"
          },
          {
            "group": "Parameter",
            "type": "Object",
            "optional": false,
            "field": "category",
            "description": "<p>更改内容</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "string",
            "optional": false,
            "field": "result",
            "description": "<p>&quot;OK&quot;</p>"
          }
        ]
      }
    },
    "filename": "handler/superside/category.py",
    "groupTitle": "manager",
    "name": "PutV10ManagerCategory",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/manager/category"
      }
    ]
  },
  {
    "type": "put",
    "url": "/v1.0/manager/event",
    "title": "更改事件信息",
    "group": "manager",
    "version": "1.0.0",
    "description": "<p>更改事件信息</p>",
    "permission": [
      {
        "name": "manager"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "event_id",
            "description": "<p>事件ID</p>"
          },
          {
            "group": "Parameter",
            "type": "Object",
            "optional": false,
            "field": "event",
            "description": "<p>更改内容</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "string",
            "optional": false,
            "field": "result",
            "description": "<p>&quot;OK&quot;</p>"
          }
        ]
      }
    },
    "filename": "handler/superside/event.py",
    "groupTitle": "manager",
    "name": "PutV10ManagerEvent",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/manager/event"
      }
    ]
  },
  {
    "type": "put",
    "url": "/v1.0/manager/index",
    "title": "更改首页推荐信息",
    "group": "manager",
    "version": "1.0.0",
    "description": "<p>更改首页推荐信息</p>",
    "permission": [
      {
        "name": "manager"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "index_id",
            "description": "<p>首页推荐ID</p>"
          },
          {
            "group": "Parameter",
            "type": "Object",
            "optional": false,
            "field": "index",
            "description": "<p>更改内容</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "string",
            "optional": false,
            "field": "result",
            "description": "<p>&quot;OK&quot;</p>"
          }
        ]
      }
    },
    "filename": "handler/superside/index.py",
    "groupTitle": "manager",
    "name": "PutV10ManagerIndex",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/manager/index"
      }
    ]
  },
  {
    "type": "put",
    "url": "/v1.0/manager/master",
    "title": "更改达人信息",
    "group": "manager",
    "version": "1.0.0",
    "description": "<p>更改达人信息</p>",
    "permission": [
      {
        "name": "manager"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "user_id",
            "description": "<p>用户ID</p>"
          },
          {
            "group": "Parameter",
            "type": "Object",
            "optional": false,
            "field": "master",
            "description": "<p>更改内容</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "string",
            "optional": false,
            "field": "result",
            "description": "<p>&quot;OK&quot;</p>"
          }
        ]
      }
    },
    "filename": "handler/superside/master.py",
    "groupTitle": "manager",
    "name": "PutV10ManagerMaster",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/manager/master"
      }
    ]
  },
  {
    "type": "put",
    "url": "/v1.0/manager/order",
    "title": "支付订单(临时)",
    "group": "manager",
    "version": "1.0.0",
    "description": "<p>支付订单</p>",
    "permission": [
      {
        "name": "manager"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "order_id",
            "description": "<p>订单ID</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "result",
            "description": "<p>'OK'</p>"
          }
        ]
      }
    },
    "filename": "handler/superside/order.py",
    "groupTitle": "manager",
    "name": "PutV10ManagerOrder",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/manager/order"
      }
    ]
  },
  {
    "type": "put",
    "url": "/v1.0/manager/team",
    "title": "更改小组信息",
    "group": "manager",
    "version": "1.0.0",
    "description": "<p>更改小组信息</p>",
    "permission": [
      {
        "name": "manager"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "team_id",
            "description": "<p>小组ID</p>"
          },
          {
            "group": "Parameter",
            "type": "Object",
            "optional": false,
            "field": "team",
            "description": "<p>更改内容</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "string",
            "optional": false,
            "field": "result",
            "description": "<p>&quot;OK&quot;</p>"
          }
        ]
      }
    },
    "filename": "handler/superside/team.py",
    "groupTitle": "manager",
    "name": "PutV10ManagerTeam",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/manager/team"
      }
    ]
  },
  {
    "type": "put",
    "url": "/v1.0/manager/user",
    "title": "更改用户信息",
    "group": "manager",
    "version": "1.0.0",
    "description": "<p>更改用户信息</p>",
    "permission": [
      {
        "name": "manager"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "user_id",
            "description": ""
          },
          {
            "group": "Parameter",
            "type": "Object",
            "optional": false,
            "field": "user",
            "description": ""
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "string",
            "optional": false,
            "field": "result",
            "description": "<p>&quot;OK&quot;</p>"
          }
        ]
      }
    },
    "filename": "handler/superside/user.py",
    "groupTitle": "manager",
    "name": "PutV10ManagerUser",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/manager/user"
      }
    ]
  },
  {
    "type": "get",
    "url": "/v1.0/master",
    "title": "获取达人详情",
    "group": "master",
    "version": "1.0.0",
    "description": "<p>获取达人详情</p>",
    "permission": [
      {
        "name": "user"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "user_id",
            "description": "<p>达人ID</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "master",
            "description": "<p>达人信息</p>"
          }
        ]
      }
    },
    "filename": "handler/master.py",
    "groupTitle": "master",
    "name": "GetV10Master",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/master"
      }
    ]
  },
  {
    "type": "get",
    "url": "/v1.0/master/card",
    "title": "获取达人卡片信息",
    "group": "master",
    "version": "1.0.0",
    "description": "<p>获取达人卡片信息</p>",
    "permission": [
      {
        "name": "user"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "user_id",
            "description": ""
          },
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "sortby",
            "description": ""
          },
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "sort",
            "description": ""
          },
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "limit",
            "description": ""
          },
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "skip",
            "description": ""
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "list",
            "optional": false,
            "field": "cardlist",
            "description": "<p>卡片信息列表</p>"
          }
        ]
      }
    },
    "filename": "handler/master.py",
    "groupTitle": "master",
    "name": "GetV10MasterCard",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/master/card"
      }
    ]
  },
  {
    "type": "get",
    "url": "/v1.0/notice",
    "title": "获取通知详情",
    "group": "notice",
    "version": "1.0.0",
    "description": "<p>获取通知详情</p>",
    "permission": [
      {
        "name": "user"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "notice_id",
            "description": ""
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "object",
            "optional": false,
            "field": "notice",
            "description": "<p>通知</p>"
          }
        ]
      }
    },
    "filename": "handler/notice.py",
    "groupTitle": "notice",
    "name": "GetV10Notice",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/notice"
      }
    ]
  },
  {
    "type": "get",
    "url": "/v1.0/noticeholder",
    "title": "获取通知列表(未处理/所有)",
    "group": "notice",
    "version": "1.0.0",
    "description": "<p>获取通知列表(未处理/所有)</p>",
    "permission": [
      {
        "name": "user"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "unhandle",
            "description": "<p>Y/N:未处理/所有</p>"
          },
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "page",
            "description": "<p>页码</p>"
          },
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "pagesize",
            "description": "<p>页大小</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "list",
            "optional": false,
            "field": "cardlist",
            "description": "<p>卡片列表</p>"
          }
        ]
      }
    },
    "filename": "handler/notice.py",
    "groupTitle": "notice",
    "name": "GetV10Noticeholder",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/noticeholder"
      }
    ]
  },
  {
    "type": "post",
    "url": "/v1.0/noticeholder",
    "title": "处理通知",
    "group": "notice",
    "version": "1.0.0",
    "description": "<p>处理通知</p>",
    "permission": [
      {
        "name": "user"
      }
    ],
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "string",
            "optional": false,
            "field": "result",
            "description": "<p>&quot;OK&quot;</p>"
          }
        ]
      }
    },
    "filename": "handler/notice.py",
    "groupTitle": "notice",
    "name": "PostV10Noticeholder",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/noticeholder"
      }
    ]
  },
  {
    "type": "delete",
    "url": "/v1.0/order/user",
    "title": "取消订单",
    "group": "order",
    "version": "1.0.0",
    "description": "<p>取消订单</p>",
    "permission": [
      {
        "name": "user"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "order_id",
            "description": "<p>订单id</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "string",
            "optional": false,
            "field": "result",
            "description": "<p>'OK'</p>"
          }
        ]
      }
    },
    "filename": "handler/order.py",
    "groupTitle": "order",
    "name": "DeleteV10OrderUser",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/order/user"
      }
    ]
  },
  {
    "type": "get",
    "url": "/v1.0/order",
    "title": "获取订单详情",
    "group": "order",
    "version": "1.0.0",
    "description": "<p>获取订单详情</p>",
    "permission": [
      {
        "name": "user"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "order_id",
            "description": "<p>订单ID</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "object",
            "optional": false,
            "field": "order",
            "description": "<p>订单</p>"
          }
        ]
      }
    },
    "filename": "handler/order.py",
    "groupTitle": "order",
    "name": "GetV10Order",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/order"
      }
    ]
  },
  {
    "type": "get",
    "url": "/v1.0/order/pay",
    "title": "获取订单支付代码(支付订单)",
    "group": "order",
    "version": "1.0.0",
    "description": "<p>获取订单支付代码</p>",
    "permission": [
      {
        "name": "user"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "order_id",
            "description": "<p>订单id</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "string",
            "optional": false,
            "field": "ch_id",
            "description": "<p>支付代码</p>"
          }
        ]
      }
    },
    "filename": "handler/order.py",
    "groupTitle": "order",
    "name": "GetV10OrderPay",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/order/pay"
      }
    ]
  },
  {
    "type": "get",
    "url": "/v1.0/order/user",
    "title": "获取订单列表(用户)",
    "group": "order",
    "version": "1.0.0",
    "description": "<p>获取订单列表(用户)</p>",
    "permission": [
      {
        "name": "user"
      }
    ],
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "object",
            "optional": false,
            "field": "orderlist",
            "description": "<p>获取订单列表</p>"
          }
        ]
      }
    },
    "filename": "handler/order.py",
    "groupTitle": "order",
    "name": "GetV10OrderUser",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/order/user"
      }
    ]
  },
  {
    "type": "post",
    "url": "/v1.0/order",
    "title": "完成订单相关操作",
    "group": "order",
    "version": "1.0.0",
    "description": "<p>完成订单相关操作</p>",
    "permission": [
      {
        "name": "user"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "order_id",
            "description": "<p>订单ID</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "object",
            "optional": false,
            "field": "orderlist",
            "description": "<p>获取订单列表</p>"
          }
        ]
      }
    },
    "filename": "handler/order.py",
    "groupTitle": "order",
    "name": "PostV10Order",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/order"
      }
    ]
  },
  {
    "type": "post",
    "url": "/v1.0/order/order_callback",
    "title": "ping++回调函数",
    "group": "order",
    "version": "1.0.0",
    "description": "<p>完成订单</p>",
    "permission": [
      {
        "name": "user"
      }
    ],
    "filename": "handler/order.py",
    "groupTitle": "order",
    "name": "PostV10OrderOrder_callback",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/order/order_callback"
      }
    ]
  },
  {
    "type": "post",
    "url": "/v1.0/order/user",
    "title": "创建订单",
    "group": "order",
    "version": "1.0.0",
    "description": "<p>创建订单</p>",
    "permission": [
      {
        "name": "user"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "event_id",
            "description": "<p>事件Id</p>"
          },
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "remarkInfo",
            "description": "<p>备注</p>"
          },
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "realName",
            "description": "<p>真实姓名</p>"
          },
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "realPhone",
            "description": "<p>联系电话</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "string",
            "optional": false,
            "field": "order_id",
            "description": "<p>订单ID</p>"
          }
        ]
      }
    },
    "filename": "handler/order.py",
    "groupTitle": "order",
    "name": "PostV10OrderUser",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/order/user"
      }
    ]
  },
  {
    "type": "post",
    "url": "/v1.0/order/wx_lite_callback",
    "title": "微信支付回调函数",
    "group": "order",
    "version": "1.0.0",
    "description": "<p>完成订单</p>",
    "permission": [
      {
        "name": "user"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "order_id",
            "description": "<p>订单编号</p>"
          },
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "ch_id",
            "description": "<p>支付代码</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "string",
            "optional": false,
            "field": "result",
            "description": "<p>&quot;OK&quot;/&quot;NO&quot;</p>"
          }
        ]
      }
    },
    "filename": "handler/order.py",
    "groupTitle": "order",
    "name": "PostV10OrderWx_lite_callback",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/order/wx_lite_callback"
      }
    ]
  },
  {
    "type": "post",
    "url": "/v1.0/order/wxpay",
    "title": "微信支付下单",
    "group": "order",
    "version": "1.0.0",
    "description": "<p>微信支付下单</p>",
    "permission": [
      {
        "name": "user"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "order_id",
            "description": "<p>订单编号</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "string",
            "optional": false,
            "field": "prepay_id",
            "description": "<p>支付代码</p>"
          }
        ]
      }
    },
    "filename": "handler/wxpay.py",
    "groupTitle": "order",
    "name": "PostV10OrderWxpay",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/order/wxpay"
      }
    ]
  },
  {
    "type": "post",
    "url": "/v1.0/order/wxpay/return",
    "title": "微信支付前端回调",
    "group": "order",
    "version": "1.0.0",
    "description": "<p>微信支付前端回调</p>",
    "permission": [
      {
        "name": "user"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "order_id",
            "description": "<p>订单编号</p>"
          },
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "result",
            "description": "<p>'success'/'fail'</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "string",
            "optional": false,
            "field": "result",
            "description": "<p>'OK'</p>"
          }
        ]
      }
    },
    "filename": "handler/wxpay.py",
    "groupTitle": "order",
    "name": "PostV10OrderWxpayReturn",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/order/wxpay/return"
      }
    ]
  },
  {
    "type": "post",
    "url": "/v1.0/order/wxpay/wx_callback",
    "title": "微信支付腾讯回调",
    "group": "order",
    "version": "1.0.0",
    "description": "<p>微信支付回调</p>",
    "permission": [
      {
        "name": "user"
      }
    ],
    "filename": "handler/wxpay.py",
    "groupTitle": "order",
    "name": "PostV10OrderWxpayWx_callback",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/order/wxpay/wx_callback"
      }
    ]
  },
  {
    "type": "get",
    "url": "/v1.0/static/token",
    "title": "七牛上传token",
    "name": "upload_token",
    "group": "other",
    "version": "1.0.0",
    "description": "<p>获取七牛用的上传token</p>",
    "permission": [
      {
        "name": "all"
      }
    ],
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "key",
            "description": "<p>分配的文件名</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "token",
            "description": "<p>上传使用的token</p>"
          }
        ]
      }
    },
    "filename": "handler/qiniu.py",
    "groupTitle": "other",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/static/token"
      }
    ]
  },
  {
    "type": "delete",
    "url": "/v1.0/team/manger",
    "title": "删帖",
    "group": "team",
    "version": "1.0.0",
    "description": "<p>删帖</p>",
    "permission": [
      {
        "name": "user"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "card_id",
            "description": "<p>卡片id</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "string",
            "optional": false,
            "field": "result",
            "description": "<p>&quot;OK&quot;</p>"
          }
        ]
      }
    },
    "filename": "handler/team.py",
    "groupTitle": "team",
    "name": "DeleteV10TeamManger",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/team/manger"
      }
    ]
  },
  {
    "type": "get",
    "url": "/v1.0/team",
    "title": "获取小组详情",
    "group": "team",
    "version": "1.0.0",
    "description": "<p>获取小组详情</p>",
    "permission": [
      {
        "name": "user"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "team_id",
            "description": "<p>小组ID</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "object",
            "optional": false,
            "field": "team",
            "description": "<p>小组详情</p>"
          }
        ]
      }
    },
    "filename": "handler/team.py",
    "groupTitle": "team",
    "name": "GetV10Team",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/team"
      }
    ]
  },
  {
    "type": "post",
    "url": "/v1.0/team",
    "title": "加入小组",
    "group": "team",
    "version": "1.0.0",
    "description": "<p>加入小组</p>",
    "permission": [
      {
        "name": "user"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "team_id",
            "description": "<p>小组ID</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "string",
            "optional": false,
            "field": "result",
            "description": "<p>&quot;OK&quot;</p>"
          }
        ]
      }
    },
    "filename": "handler/team.py",
    "groupTitle": "team",
    "name": "PostV10Team",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/team"
      }
    ]
  },
  {
    "type": "put",
    "url": "/v1.0/team",
    "title": "退出小组",
    "group": "team",
    "version": "1.0.0",
    "description": "<p>退出小组</p>",
    "permission": [
      {
        "name": "user"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "team_id",
            "description": "<p>小组id</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "string",
            "optional": false,
            "field": "result",
            "description": "<p>&quot;OK&quot;</p>"
          }
        ]
      }
    },
    "filename": "handler/team.py",
    "groupTitle": "team",
    "name": "PutV10Team",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/team"
      }
    ]
  },
  {
    "type": "delete",
    "url": "/v1.0/token/access",
    "title": "注销access token",
    "group": "token",
    "version": "1.0.0",
    "description": "<p>注销access token</p>",
    "permission": [
      {
        "name": "user"
      }
    ],
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "string",
            "optional": false,
            "field": "result",
            "description": "<p>&quot;OK&quot;</p>"
          }
        ]
      }
    },
    "filename": "handler/token.py",
    "groupTitle": "token",
    "name": "DeleteV10TokenAccess",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/token/access"
      }
    ]
  },
  {
    "type": "post",
    "url": "/v1.0/token/access",
    "title": "获取access token",
    "group": "token",
    "version": "1.0.0",
    "description": "<p>获取access token</p>",
    "permission": [
      {
        "name": "all"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "phone",
            "description": "<p>手机号</p>"
          },
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "password",
            "description": "<p>密码</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "token",
            "description": ""
          }
        ],
        "token": [
          {
            "group": "token",
            "type": "string",
            "optional": false,
            "field": "userId",
            "description": ""
          },
          {
            "group": "token",
            "type": "string",
            "optional": false,
            "field": "accessToken",
            "description": ""
          },
          {
            "group": "token",
            "type": "string",
            "optional": false,
            "field": "accessTime",
            "description": ""
          }
        ]
      }
    },
    "filename": "handler/token.py",
    "groupTitle": "token",
    "name": "PostV10TokenAccess",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/token/access"
      }
    ]
  },
  {
    "type": "post",
    "url": "/v1.0/token/smscode",
    "title": "发送短信验证码",
    "group": "token",
    "version": "1.0.0",
    "description": "<p>发送短信验证码</p>",
    "permission": [
      {
        "name": "all"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "phone",
            "description": "<p>手机号</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "string",
            "optional": false,
            "field": "result",
            "description": "<p>&quot;OK&quot;</p>"
          }
        ]
      }
    },
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "type": "string",
            "optional": false,
            "field": "message",
            "description": ""
          }
        ]
      }
    },
    "filename": "handler/token.py",
    "groupTitle": "token",
    "name": "PostV10TokenSmscode",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/token/smscode"
      }
    ]
  },
  {
    "type": "delete",
    "url": "/v1.0/user/favor",
    "title": "删除用户收藏",
    "group": "user",
    "version": "1.0.0",
    "permission": [
      {
        "name": "user"
      }
    ],
    "description": "<p>删除用户收藏</p>",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "type",
            "description": "<p>(1:master)\t收藏类型</p>"
          },
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "id",
            "description": "<p>收藏对象ID</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "string",
            "optional": false,
            "field": "result",
            "description": "<p>&quot;OK&quot;</p>"
          }
        ]
      }
    },
    "filename": "handler/user.py",
    "groupTitle": "user",
    "name": "DeleteV10UserFavor",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/user/favor"
      }
    ]
  },
  {
    "type": "get",
    "url": "/v1.0/user",
    "title": "获取用户信息",
    "group": "user",
    "version": "1.0.0",
    "description": "<p>获取用户信息</p>",
    "permission": [
      {
        "name": "user"
      }
    ],
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "user",
            "description": "<p>用户信息</p>"
          }
        ]
      }
    },
    "filename": "handler/user.py",
    "groupTitle": "user",
    "name": "GetV10User",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/user"
      }
    ]
  },
  {
    "type": "get",
    "url": "/v1.0/user/application",
    "title": "查询用户申请",
    "group": "user",
    "version": "1.0.0",
    "description": "<p>查询用户申请</p>",
    "permission": [
      {
        "name": "user"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "page",
            "description": "<p>页数</p>"
          },
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "pagesize",
            "description": "<p>页大小</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "list",
            "optional": false,
            "field": "applicationlist",
            "description": "<p>用户申请列表</p>"
          }
        ]
      }
    },
    "filename": "handler/user.py",
    "groupTitle": "user",
    "name": "GetV10UserApplication",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/user/application"
      }
    ]
  },
  {
    "type": "get",
    "url": "/v1.0/user/favor",
    "title": "查询用户收藏",
    "group": "user",
    "version": "1.0.0",
    "description": "<p>查询用户收藏</p>",
    "permission": [
      {
        "name": "user"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "type",
            "description": "<p>(1:master)\t收藏类型</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "list",
            "optional": false,
            "field": "favorlist",
            "description": "<p>收藏内容列表</p>"
          }
        ]
      }
    },
    "filename": "handler/user.py",
    "groupTitle": "user",
    "name": "GetV10UserFavor",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/user/favor"
      }
    ]
  },
  {
    "type": "post",
    "url": "/v1.0/user/application",
    "title": "用户提出申请",
    "group": "user",
    "version": "1.0.0",
    "description": "<p>用户提出申请</p>",
    "permission": [
      {
        "name": "user"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "application",
            "description": "<p>用户申请</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "string",
            "optional": false,
            "field": "result",
            "description": "<p>&quot;OK&quot;</p>"
          }
        ]
      }
    },
    "filename": "handler/user.py",
    "groupTitle": "user",
    "name": "PostV10UserApplication",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/user/application"
      }
    ]
  },
  {
    "type": "POST",
    "url": "/v1.0/user/favor",
    "title": "添加用户收藏",
    "group": "user",
    "version": "1.0.0",
    "description": "<p>添加用户收藏</p>",
    "permission": [
      {
        "name": "user"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "type",
            "description": "<p>(1:master)\t收藏类型</p>"
          },
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "id",
            "description": "<p>收藏对象ID</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "string",
            "optional": false,
            "field": "result",
            "description": "<p>&quot;OK&quot;</p>"
          }
        ]
      }
    },
    "filename": "handler/user.py",
    "groupTitle": "user",
    "name": "PostV10UserFavor",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/user/favor"
      }
    ]
  },
  {
    "type": "post",
    "url": "/v1.0/user/login",
    "title": "微信登陆",
    "group": "user",
    "version": "1.0.0",
    "description": "<p>微信登陆</p>",
    "permission": [
      {
        "name": "all"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "code",
            "description": "<p>手机号</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "object",
            "optional": false,
            "field": "utoken",
            "description": "<p>用户登陆token</p>"
          },
          {
            "group": "Success 200",
            "type": "string",
            "optional": false,
            "field": "new",
            "description": "<p>是否新用户</p>"
          }
        ],
        "token": [
          {
            "group": "token",
            "type": "string",
            "optional": false,
            "field": "userId",
            "description": ""
          },
          {
            "group": "token",
            "type": "string",
            "optional": false,
            "field": "accessToken",
            "description": ""
          },
          {
            "group": "token",
            "type": "string",
            "optional": false,
            "field": "accessTime",
            "description": ""
          }
        ]
      }
    },
    "filename": "handler/user.py",
    "groupTitle": "user",
    "name": "PostV10UserLogin",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/user/login"
      }
    ]
  },
  {
    "type": "post",
    "url": "/v1.0/user/register",
    "title": "用户注册",
    "group": "user",
    "version": "1.0.0",
    "description": "<p>用户注册</p>",
    "permission": [
      {
        "name": "all"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "phone",
            "description": "<p>手机号</p>"
          },
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "password",
            "description": "<p>密码</p>"
          },
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "code",
            "description": "<p>验证码</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "object",
            "optional": false,
            "field": "utoken",
            "description": "<p>用户登陆token</p>"
          }
        ],
        "token": [
          {
            "group": "token",
            "type": "string",
            "optional": false,
            "field": "userId",
            "description": ""
          },
          {
            "group": "token",
            "type": "string",
            "optional": false,
            "field": "accessToken",
            "description": ""
          },
          {
            "group": "token",
            "type": "string",
            "optional": false,
            "field": "accessTime",
            "description": ""
          }
        ]
      }
    },
    "filename": "handler/user.py",
    "groupTitle": "user",
    "name": "PostV10UserRegister",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/user/register"
      }
    ]
  },
  {
    "type": "put",
    "url": "/v1.0/user/password",
    "title": "更新password",
    "group": "user",
    "version": "1.0.0",
    "description": "<p>更新password</p>",
    "permission": [
      {
        "name": "user"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "Opassword",
            "description": "<p>旧password</p>"
          },
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "Npassword",
            "description": "<p>新password</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "string",
            "optional": false,
            "field": "result",
            "description": "<p>&quot;OK&quot;</p>"
          }
        ]
      }
    },
    "filename": "handler/user.py",
    "groupTitle": "user",
    "name": "PutV10UserPassword",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/user/password"
      }
    ]
  },
  {
    "type": "put",
    "url": "/v1.0/user/userinfo",
    "title": "更新个人信息",
    "group": "user",
    "version": "1.0.0",
    "description": "<p>更新用户信息</p>",
    "permission": [
      {
        "name": "user"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "Object",
            "optional": false,
            "field": "user",
            "description": "<p>用户信息</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "string",
            "optional": false,
            "field": "result",
            "description": "<p>&quot;OK&quot;</p>"
          }
        ]
      }
    },
    "filename": "handler/user.py",
    "groupTitle": "user",
    "name": "PutV10UserUserinfo",
    "sampleRequest": [
      {
        "url": "http://testapi.idarenhui.com/v1.0/user/userinfo"
      }
    ]
  }
] });
