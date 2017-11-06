from handler.base import BaseHandler
import routes
from handler.exceptions import ResourceNotExistError,PermissionDeniedError,ArgsError,StateError,RelateResError


class TeamHandler(BaseHandler):
    """
        @api {get} /v1.0/team 获取小组详情

        @apiGroup team
        @apiVersion  1.0.0
        @apiDescription 获取小组详情

        @apiPermission user
        
        @apiParam    {string}    team_id    小组ID
        
        @apiSuccess    {object}    team    小组详情
    """
    async def get(self):
        user_info=await self.user_info
        
        team_id    =self.get_argument('like',default=None)
        
        team = await self.db.team.get_by_id(team_id)
        if team is None:
            raise ResourceNotExistError("小组不存在{0}".format(team_id))
        self.finish_success(result=team)
        pass
        
    """
        @api {post} /v1.0/team  加入小组
        @apiGroup team
        @apiVersion  1.0.0
        @apiDescription 加入小组
        @apiPermission user
        
        @apiParam    {string}    team_id    小组ID
        
        @apiSuccess    {string}    result "OK"
    """
    async def post(self):
        user_info=await self.user_info
        json=self.json_body
        team_id=json['team_id']
        team = await self.db.team.get_by_id(team_id)
        if team is None:
            raise ResourceNotExistError("小组不存在{0}".format(team_id))
        await self.db.user.insert_favor_team((str)user_info['_id'],team_id)
        await self.db.team.insert_member(team_id,(str)user_info['_id'])
        self.finish_success(result='OK')

    """
        @api {put} /v1.0/team 退出小组
        @apiGroup team
        @apiVersion  1.0.0
        @apiDescription 退出小组
        @apiPermission user
        
        @apiParam {string} team_id       小组id

        
        @apiSuccess    {string}    result "OK"
    """
    async def put(self):
        user_info=await self.user_info
        json=self.json_body
        team_id=json['team_id']
        team = await self.db.team.get_by_id(team_id)
        if team is None:
            raise ResourceNotExistError("小组不存在{0}".format(team_id))
        await self.db.user.remove_favor_team((str)user_info['_id'],team_id)
        await self.db.team.remove_member(team_id,(str)user_info['_id'])
        self.finish_success(result='OK')
        return

class TeamManagerHandler(BaseHandler):
    """
        @api {delete} /v1.0/team/manger 删帖
        @apiGroup team
        @apiVersion  1.0.0
        @apiDescription 删帖
        @apiPermission user
        
        @apiParam {string} card_id       卡片id

        
        @apiSuccess    {string}    result "OK"
    """
    async def delete(self):
        user_info=await self.user_info
        json=self.json_body
        card_id=json['card_id']
        card = await self.db.card.get_by_id(card_id)
        if card is None:
            raise ResourceNotExistError("卡片不存在{0}".format(card_id))
        team_id = card['belongTeam']
        team = await self.db.team.get_by_id(team_id)
        if team is None:
            raise RelateResError("小组不存在")
        if (str)user_info['_id'] not in team['leaderlist']:
            raise PermissionDeniedError("需要有本小组的管理员权限")
        await self.remove_card(card_id)
        
        
        
routes.handlers += [
    (r'/v1.0/team', TeamHandler),
    (r'/v1.0/team/manger', TeamManagerHandler),
]
