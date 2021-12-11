
from deta import Deta
import aiohttp
import requests

from ._helpers import getCurrentTimestamp,checkExpiredTimestamp


class CacheApi(object):
    def __init__(self, projectKey: str = None,projectId: str = None,baseName:str='cache'):
        self.dbCache = Deta(project_key=projectKey,project_id=projectId).Base(baseName)

    def syncGetJson(self,url:str,headers:dict=None,ttl:int=0,log:bool=False):
        return self.__syncCheckCached(url=url,response='json',headers=headers,expire=ttl,log=log)

    def syncGetText(self,url:str,headers:dict=None,ttl:int=0,log:bool=False):
        return self.__syncCheckCached(url=url,response='text',headers=headers,expire=ttl,log=log)

    async def asyncGetJson(self,url:str,headers:dict=None,ttl:int=0,log:bool=False):
        return await self.__asyncCheckCached(url=url,response='json',headers=headers,expire=ttl,log=log)

    async def asyncGetText(self,url:str,headers:dict=None,ttl:int=0,log:bool=False):
        return await self.__asyncCheckCached(url=url,response='text',headers=headers,expire=ttl,log=log)

    async def __aiohttpFetchJson(self,url:str,headers:dict=None):
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url=url) as response:
                return await response.json()

    async def __aiohttpFetchText(self,url:str,headers:dict=None):
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url=url) as response:
                return await response.json()

    def __requestsFetchJson(self,url:str,headers:dict=None):
        return requests.get(url=url,headers=headers).json()

    def __requestsFetchText(self,url:str,headers:dict=None):
        return requests.get(url=url,headers=headers).text
    
    async def __asyncCheckCached(self,url:str,response:str,headers:dict,expire:int,log:bool):
        cached = self.dbCache.get(key=url)
        if not cached:
            return self.__dbCacheMISS(
                await self.__aiohttpFetchText(url,headers) if response == 'text' else await self.__aiohttpFetchJson(url,headers) ,
                url,expire,log)
        if not cached['expire'] == expire:
            return self.__dbUpdateExpireTime(
                await self.__aiohttpFetchText(url,headers) if response == 'text' else await self.__aiohttpFetchJson(url,headers) ,
                url,expire,log)
        if expire and checkExpiredTimestamp(cached['expire'],cached['timestamp'],getCurrentTimestamp()):
            return self.__dbUpdateCached(
                await self.__aiohttpFetchText(url,headers) if response == 'text' else await self.__aiohttpFetchJson(url,headers) ,
                url,log)
        if log:print('cached HIT')
        return cached['value']

    def __syncCheckCached(self,url:str,response:str,headers:dict,expire:int,log:bool):
        cached = self.dbCache.get(key=url)
        if not cached:
            return self.__dbCacheMISS(
                self.__requestsFetchText(url,headers) if response == 'text' else self.__requestsFetchJson(url,headers) ,
                url,expire,log)
        if not cached['expire'] == expire:
            return self.__dbUpdateExpireTime(
                self.__requestsFetchText(url,headers) if response == 'text' else self.__requestsFetchJson(url,headers) ,
                url,expire,log)
        if expire and checkExpiredTimestamp(cached['expire'],cached['timestamp'],getCurrentTimestamp()):
            return self.__dbUpdateCached(
                self.__requestsFetchText(url,headers) if response == 'text' else self.__requestsFetchJson(url,headers) ,
                url,log)
        if log:print('cached HIT')
        return cached['value']
    
    def __dbCacheMISS(self,data,key:str,expire:int,log:bool):
        if log:print('cache MISS')
        self.dbCache.put(data={
            'value':data,
            'expire':expire,
            'timestamp':getCurrentTimestamp()
            },key=key)
        if log:print('cached..')
        return data

    def __dbUpdateExpireTime(self,data,key:str,expire:int,log:bool):
        if log:print('updating.... expire time')
        self.dbCache.update(updates={
            'value':data,
            'expire':expire,
            'timestamp':getCurrentTimestamp(),
            },key=key)
        if log:print('cached.. and updated expire time')
        return data

    def __dbUpdateCached(self,data,key:str,log:bool):
        if log:print('cache expired, updating....')
        self.dbCache.update(updates={
            'value':data,
            'timestamp':getCurrentTimestamp(),
            },key=key)
        if log:print('cached..')
        return data