from sdk.tor_top.base import TOPClient


class TOPPushCilent(TOPClient):
    async def andtoid_notice(self,title,tagget,target_value=''):
        if isinstance(target_value,list):
            target_value = ','.join(target_value)
        if tagget=='all':
            res = await self._fetch(
                method='taobao.cloudpush.notice.android',
                target=tagget,
                title=title
            )
            body = res
            print(body)