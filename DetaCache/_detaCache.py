
import asyncio
from functools import wraps
from deta import Deta

from ._helpers import getDecoratorArgs,createStringHashKey,getCurrentTimestamp,checkExpiredTimestamp


class DetaCache(object):
    '''## Create an instance of DetaCache.
    
    Args:
        projectKey (str): Sets the projectKey of Deta .
        projectId (str, optional): Sets the projectId of Deta.
        baseName (str,optional): Sets the name of DetaBase. Defaults to `cache`.
    
    Example:
        Calling `DetaCache` gives an instance of DetaCache.
    ```
        import aiohttp
        import requests
        from detacache import DetaCache

        app = DetaCache('projectKey')

        @app.cache()
        async def asyncgetjSON(url:str):
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    return await response.json()

        @app.cache()
        def syncgetjSON(url:str):
            return requests.get(url).json()
    ```
    '''
    def __init__(self, projectKey: str = None,projectId: str = None,baseName:str='cache'):
        self._dbCache = Deta(project_key=projectKey,project_id=projectId).Base(baseName)


    def cache(self,expire:int=0,log:bool=False) -> None:
        '''### Decorator for both Async and Sync Functions to cache in Deta Base.
        Args:
            expire (int, optional): Sets the expire time to expire in sec . Defaults to `0`.
            log (bool, optional): Sets whether to log. Defaults to `False`.
        '''
        def wrapped(function):
            @wraps(function)
            async def asyncWrappedFunction(*args, **kwargs):
                functionArgs = getDecoratorArgs(function,args,kwargs)
                return await asyncCheckCached(
                    self._dbCache,
                    createStringHashKey(f'{function.__name__}{functionArgs}'),
                    function,
                    functionArgs,
                    expire,
                    log,
                    *args,
                    **kwargs,)
            @wraps(function)
            def syncWrappedFunction(*args, **kwargs):
                functionArgs = getDecoratorArgs(function,args,kwargs)
                return syncCheckCached(
                    self._dbCache,
                    createStringHashKey(f'{function.__name__}{functionArgs}'),
                    function,
                    functionArgs,
                    expire,
                    log,
                    *args,
                    **kwargs,)
            if asyncio.iscoroutinefunction(function):
                return asyncWrappedFunction
            else:
                return syncWrappedFunction
        return wrapped

async def asyncCheckCached(db,key,function,functionArgs,expire,log,*args, **kwargs):
    cached = db.get(key=key)
    if not cached:
        return dbCacheMISS(await function(*args, **kwargs),db,key,function.__name__,functionArgs,expire,log)
    if not cached['expire'] == expire:
        return dbUpdateExpireTime(await function(*args, **kwargs),db,key,function.__name__,functionArgs,expire,log)
    if expire and checkExpiredTimestamp(cached['expire'],cached['timestamp'],getCurrentTimestamp()):
        return dbUpdateCached(await function(*args, **kwargs),db,key,function.__name__,functionArgs,log)
    if log:print(f'{function.__name__} with {functionArgs} cached HIT')
    return cached['value']

def syncCheckCached(db,key,function,functionArgs,expire,log,*args, **kwargs):
    cached = db.get(key=key)
    if not cached:
        return dbCacheMISS(function(*args, **kwargs),db,key,function.__name__,functionArgs,expire,log)
    if not cached['expire'] == expire:
        return dbUpdateExpireTime(function(*args, **kwargs),db,key,function.__name__,functionArgs,expire,log)
    if expire and checkExpiredTimestamp(cached['expire'],cached['timestamp'],getCurrentTimestamp()):
        return dbUpdateCached(function(*args, **kwargs),db,key,function.__name__,functionArgs,log)
    if log:print(f'{function.__name__} with {functionArgs} cached HIT')
    return cached['value']

def dbCacheMISS(data,db,key,functionName,functionArgs,expire,log):
    if log:print(f'{functionName} with {functionArgs} cache MISS')
    db.put(data={
        'value':data,
        'function':functionName,
        'Arg':functionArgs,
        'expire':expire,
        'timestamp':getCurrentTimestamp()
        },key=key)
    if log:print(f'{functionName} with {functionArgs} cached..')
    return data

def dbUpdateExpireTime(data,db,key,functionName,functionArgs,expire,log):
    if log:print(f'{functionName} with {functionArgs} updating.... expire time')
    db.update(updates={
        'value':data,
        'expire':expire,
        'timestamp':getCurrentTimestamp(),
        },key=key)
    if log:print(f'{functionName} with {functionArgs} cached.. and updated expire time')
    return data

def dbUpdateCached(data,db,key,functionName,functionArgs,log):
    if log:print(f'{functionName} with {functionArgs} cache expired, updating....')
    db.update(updates={
        'value':data,
        'timestamp':getCurrentTimestamp(),
        },key=key)
    if log:print(f'{functionName} with {functionArgs} cached..')
    return data

