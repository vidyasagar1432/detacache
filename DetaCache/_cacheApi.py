
from deta import Deta
import aiohttp

class CacheApi(object):
    def __init__(self, projectKey: str = None,projectId: str = None,baseName:str='cache'):
        self.dbCache = Deta(project_key=projectKey,project_id=projectId).Base(baseName)

    async def __aiohttpFetchJson(self,url:str,headers:dict=None):
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url=url) as response:
                return await response.json()

    async def __aiohttpFetchText(self,url:str,headers:dict=None):
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url=url) as response:
                return await response.json()

    async def asyncGetJson(self,url:str,headers:dict=None):
        data = self.dbCache.get(key=url)
        if not data:
            _data = await self.__aiohttpFetchJson(url,headers)
            self.dbCache.put(data={'value':_data},key=url)
            return _data
        return data['value']

    async def asyncGetText(self,url:str,headers:dict=None):
        data = self.dbCache.get(key=url)
        if not data:
            _data = await self.__aiohttpFetchText(url,headers)
            self.dbCache.put(data={'value':_data},key=url)
            return _data
        return data['value']