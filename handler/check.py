from handler.base import BaseHandler
import routes
import random
import config
from handler.exceptions import ResourceNotExistError,PermissionDeniedError,ArgsError,StateError,RelateResError
    
class CheckHandler(BaseHandler):

    async def get(self):
        userlist = await self.db.user.get_user_free({},'_id','+',10000000,0)
        #print(userlist)
        for user in userlist:
            noticeholder = await self.db.noticeholder.get_by_user(str(user['_id']))
            if noticeholder is None:
                print('www')
                noticeholder=self.db.base.get_noticeholder_default()
                noticeholder['userId']=str(user['_id'])
                print(user['_id'])
                await self.db.noticeholder.insert(noticeholder)
        pass

routes.handlers += [
    (r'/v1.0/check', CheckHandler),

]
