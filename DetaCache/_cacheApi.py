
import aiohttp
import requests
from typing import Any

from ._detaCache import DetaCache


class Aiohttp:
    def __init__(self, projectKey: str = None,projectId: str = None,baseName:str='cache'):
        self.app = DetaCache(projectKey=projectKey,projectId=projectId,baseName=baseName)

    async def getJson(self,url:str,params:dict=None,ttl:int=0,log:bool=False,headers:dict=None,allow_redirects: bool = True, **kwargs: Any):
        @self.app.cache(expire=ttl,log=log)
        async def __aiohttpGetJson(url:str,params:dict=None,headers:dict=None,allow_redirects: bool = True, **kwargs: Any):
            return await self.__aiohttpFetch(url=url,response='json',params=params,allow_redirects=allow_redirects,headers=headers,**kwargs)
        return await __aiohttpGetJson(url=url,params=params,allow_redirects=allow_redirects,headers=headers,**kwargs)
    
    async def getText(self,url:str,params:dict=None,ttl:int=0,log:bool=False,headers:dict=None,allow_redirects: bool = True, **kwargs: Any):
        @self.app.cache(expire=ttl,log=log)
        async def __aiohttpGetText(url:str,params:dict=None,headers:dict=None,allow_redirects: bool = True, **kwargs: Any):
            return await self.__aiohttpFetch(url=url,response='test',params=params,allow_redirects=allow_redirects,headers=headers,**kwargs)
        return await __aiohttpGetText(url=url,params=params,allow_redirects=allow_redirects,headers=headers,**kwargs)

    async def __aiohttpFetch(self,response:str,url:str,params:dict=None,headers:dict=None,allow_redirects: bool = True, **kwargs: Any):
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url,data=params,allow_redirects=allow_redirects, **kwargs) as res:
                if response == 'json':
                    return await res.json()
                return await res.text()


class Requests:
    def __init__(self, projectKey: str = None,projectId: str = None,baseName:str='cache'):
        self.app = DetaCache(projectKey=projectKey,projectId=projectId,baseName=baseName)

    def getJson(self,url:str,params:dict=None,ttl:int=0,log:bool=False,headers:dict=None,allow_redirects: bool = True, **kwargs: Any):
        @self.app.cache(expire=ttl,log=log)
        def __requestsGetJson(url:str,params:dict=None,headers:dict=None,allow_redirects: bool = True, **kwargs: Any):
            return self.__requestsFetch(url=url,response='json',params=params,allow_redirects=allow_redirects,headers=headers,**kwargs)
        return __requestsGetJson(url=url,params=params,allow_redirects=allow_redirects,headers=headers,**kwargs)
    
    def getText(self,url:str,params:dict=None,ttl:int=0,log:bool=False,headers:dict=None,allow_redirects: bool = True, **kwargs: Any):
        @self.app.cache(expire=ttl,log=log)
        def __requestsGetText(url:str,params:dict=None,headers:dict=None,allow_redirects: bool = True, **kwargs: Any):
            return self.__requestsFetch(url=url,response='test',params=params,allow_redirects=allow_redirects,headers=headers,**kwargs)
        return __requestsGetText(url=url,params=params,allow_redirects=allow_redirects,headers=headers,**kwargs)

    def __requestsFetch(self,response:str,url:str,params:dict=None,headers:dict=None,allow_redirects: bool = True, **kwargs: Any):
        res = requests.get(url=url,params=params,headers=headers,allow_redirects=allow_redirects,**kwargs)
        if response == 'json':
            return res.json()
        return res.text