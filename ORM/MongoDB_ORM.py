# coding=utf-8
from .MongoDB import base
from .MongoDB import iconfig
from .MongoDB import notice
from .MongoDB import comment
from .MongoDB import master
from .MongoDB import token
from .MongoDB import user
from .MongoDB import application
from .MongoDB import event
from .MongoDB import order
from .MongoDB import category
from .MongoDB import banner
from .MongoDB import index
from .MongoDB import post
from .MongoDB import code
from .MongoDB import userteam
from .MongoDB import circle
from .MongoDB import mode
from .MongoDB import label
from .MongoDB import tip
from .MongoDB import task

import config
class MongoDB_ORM(object):
    def __init__(self,mongodb):
        control = base.MongoDB_control(mongodb)
        self.db_control = control
        self.base = control

        self.iconfig = iconfig.Iconfig(control)
        self.comment = comment.Comment(control)
        self.master = master.Master(control)
        self.token = token.Token(control)
        self.user = user.User(control)
        self.application = application.Application(control)
        self.notice = notice.Notice(control)
        self.event = event.Event(control)
        self.order = order.Order(control)
        self.category = category.Category(control)
        self.banner = banner.Banner(control)
        self.index = index.Index(control)
        self.post = post.Post(control)
        self.code = code.Code(control)
        self.userteam = userteam.userTeam(control)
        self.circle = circle.Circle(control)
        self.mode = mode.Mode(control)
        self.label = label.Label(control)
        self.tip = tip.Tip(control)
        self.task = task.Task(control)
