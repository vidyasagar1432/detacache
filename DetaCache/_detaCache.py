
from functools import wraps
from deta import Deta

from ._helpers import getDecoratorArgs,createStringHashKey,getCurrentTimestamp,checkExpiredTimestamp


class detaCache(object):
    '''## Create an instance of detaCache.
    
    Args:
        projectKey (str): Sets the projectKey of Deta .
        projectId (str, optional): Sets the projectId of Deta.
        baseName (str,optional): Sets the name of DetaBase. Defaults to `cache`.
    
    Example:
        Calling `detaCache` gives an instance of detaCache.
    ```
        import aiohttp
        import requests
        from DetaCache import detaCache

        app = detaCache('projectKey')

        @app.cacheAsyncFunction()
        async def asyncgetjSON(url:str):
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    return await response.json()

        @app.cacheSyncFunction()
        def syncgetjSON(url:str):
            return requests.get(url).json()
    ```
    '''
    def __init__(self, projectKey: str = None,projectId: str = None,baseName:str='cache'):
        self.dbCache = Deta(project_key=projectKey,project_id=projectId).Base(baseName)

    def cacheAsyncFunction(self,expire:int=None,log:bool=False,count:bool=False) -> None:
        '''## Decorator for Async Function to cache in Deta Base.

        Args:
            expire (int, optional): Sets the expire time to expire in sec . Defaults to `None`.
            log (bool, optional): Sets whether to log. Defaults to `False`.
            count (bool, optional): counts how many times function is called. Defaults to `False`.
            
        Note:
            count will make function slow by 50-150 ms if `True`
            
        Example:
        ```
            from DetaCache import detaCache

            app = detaCache('cache.json')

            @app.cacheAsyncFunction()
            async def someAsyncFunction(url:str):
                pass
        ```
        '''
        def wrapped(function):
            
            @wraps(function)
            async def wrappedFunction(*args, **kwargs):
                functionArgs = getDecoratorArgs(function,args,kwargs)
                key = createStringHashKey(f'{function.__name__}{functionArgs}')
                cached = self.dbCache.get(key=key)
                
                if not cached:
                    if log:print(f'{function.__name__} with {functionArgs} cache MISS')
                    _data = await function(*args, **kwargs)
                    self.dbCache.put(data={
                        'value':_data,
                        'function':function.__name__,
                        'Arg':functionArgs,
                        'expire':expire,
                        'called':0,
                        'timestamp':getCurrentTimestamp()
                        },
                        key=key)
                    if log:print(f'{function.__name__} with {functionArgs} cached..')
                    return _data
                
                if not cached['expire'] == expire:
                    if log:print(f'{function.__name__} with {functionArgs} updating.... expire time')
                    _data = await function(*args, **kwargs)
                    self.dbCache.update(updates={
                        'value':_data,
                        'expire':expire,
                        'timestamp':getCurrentTimestamp(),
                        'called':self.dbCache.util.increment(1) if count else cached['called']
                        },key=key)
                    if log:print(f'{function.__name__} with {functionArgs} cached.. and updated expire time')
                    return _data
                
                if cached['expire'] and checkExpiredTimestamp(cached['expire'],cached['timestamp'],getCurrentTimestamp()):
                    if log:print(f'{function.__name__} with {functionArgs} cache expired, updating....')
                    _data = await function(*args, **kwargs)
                    self.dbCache.update(updates={
                        'value':_data,
                        'timestamp':getCurrentTimestamp(),
                        'called':self.dbCache.util.increment(1) if count else cached['called']
                        },key=key)
                    if log:print(f'{function.__name__} with {functionArgs} cached..')
                    return _data
                if count:
                    self.dbCache.update(updates={'called':self.dbCache.util.increment(1)},key=key)
                if log:print(f'{function.__name__} with {functionArgs} cached HIT')
                return cached['value']
            
            return wrappedFunction
        return wrapped

    def cacheSyncFunction(self,expire:int=None,log:bool=False,count:bool=False)-> None:
        '''## Decorator for Sync Function to cache in Deta Base.

        Args:
            expire (int, optional): Sets the expire time to expire in sec . Defaults to `None`.
            log (bool, optional): Sets whether to log. Defaults to `False`.
            count (bool, optional): counts how many times function is called. Defaults to `False`.
            
        Note:
            count will make function slow by 50-150 ms if `True`
            
        Example:
        ```
            from DetaCache import detaCache

            app = detaCache('cache.json')

            @app.cacheSyncFunction()
            async def someSyncFunction(url:str):
                pass
        ```
        '''
        def wrapped(function):
            
            @wraps(function)
            def wrappedFunction(*args, **kwargs):
                functionArgs = getDecoratorArgs(function,args,kwargs)
                key = createStringHashKey(f'{function.__name__}{functionArgs}')
                cached = self.dbCache.get(key=key)
                
                if not cached:
                    if log:print(f'{function.__name__} with {functionArgs} cache MISS')
                    _data = function(*args, **kwargs)
                    self.dbCache.put(data={
                        'value':_data,
                        'function':function.__name__,
                        'Arg':functionArgs,
                        'expire':expire,
                        'called':0,
                        'timestamp':getCurrentTimestamp()
                        },
                        key=key)
                    if log:print(f'{function.__name__} with {functionArgs} cached..')
                    return _data
                
                if not cached['expire'] == expire:
                    if log:print(f'{function.__name__} with {functionArgs} updating.... expire time')
                    _data = function(*args, **kwargs)
                    self.dbCache.update(updates={
                        'value':_data,
                        'expire':expire,
                        'timestamp':getCurrentTimestamp(),
                        'called':self.dbCache.util.increment(1) if count else cached['called']
                        },key=key)
                    if log:print(f'{function.__name__} with {functionArgs} cached.. and updated expire time')
                    return _data
                
                if cached['expire'] and checkExpiredTimestamp(cached['expire'],cached['timestamp'],getCurrentTimestamp()):
                    if log:print(f'{function.__name__} with {functionArgs} cache expired, updating....')
                    _data = function(*args, **kwargs)
                    self.dbCache.update(updates={
                        'value':_data,
                        'timestamp':getCurrentTimestamp(),
                        'called':self.dbCache.util.increment(1) if count else cached['called']
                        },key=key)
                    if log:print(f'{function.__name__} with {functionArgs} cached..')
                    return _data
                if count:
                    self.dbCache.update(updates={'called':self.dbCache.util.increment(1)},key=key)
                if log:print(f'{function.__name__} with {functionArgs} cached HIT')
                return cached['value']
            
            return wrappedFunction
        return wrapped