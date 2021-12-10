import asyncio
from functools import wraps
from tinydb import TinyDB
from tinydb.table import Document
from tinydb.operations import increment

from ._helpers import getDecoratorArgs,createIntHashKey,getCurrentTimestamp,checkExpiredTimestamp


class localCache(object):
    '''## Create an instance of localCache.
    
    Args:
        filePath (str,optional): Sets the Path of file . Defaults to `cache.json`.
        tableName (int, optional): Sets the name of table. Defaults to `cache`.
        
    Example:
        Calling `localCache` gives an instance of localCache.
    ```
        import aiohttp
        import requests
        from DetaCache import localCache

        app = localCache('cache.json')

        @app.cacheasync()
        async def asyncgetjSON(url:str):
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    return await response.json()

        @app.cache()
        def syncgetjSON(url:str):
            return requests.get(url).json()
    ```
    '''
    def __init__(self,filePath:str='cache.json', tableName: str = 'cache'):
        db = TinyDB(filePath)
        self.dbCache = db.table(tableName)

    def cache(self,expire:int=None,log:bool=False,count:bool=False) -> None:
        '''## Decorator to cache locally.

        Args:
            expire (int, optional): Sets the expire time to expire in sec . Defaults to `None`.
            log (bool, optional): Sets whether to log. Defaults to `False`.
            count (bool, optional): counts how many times function is called. Defaults to `False`.
            
        Note:
            count will make function slow by 50-150 ms if `True`
            
        Example:
        ```
            from DetaCache import localCache

            app = localCache('cache.json')

            @app.cacheasync()
            async def function():
                pass
        ```
        '''
        def wrapped(function):
            
            @wraps(function)
            async def asyncWrappedFunction(*args, **kwargs):
                functionArgs = getDecoratorArgs(function,args,kwargs)
                key = createIntHashKey(f'{function.__name__}{functionArgs}')
                cached = self.dbCache.get(doc_id=key)
                
                if not cached:
                    if log:print(f'{function.__name__} with {functionArgs} cache MISS')
                    _data = await function(*args, **kwargs)
                    self.dbCache.insert(Document({
                        'value':_data,
                        'function':function.__name__,
                        'Arg':functionArgs,
                        'called':0,
                        'expire':expire,
                        'timestamp':getCurrentTimestamp()
                        },
                        doc_id=key))
                    if log:print(f'{function.__name__} with {functionArgs} cached..')
                    return _data
                
                if not cached.get('expire') == expire:
                    if log:print(f'{function.__name__} with {functionArgs} updating.... expire time')
                    _data = await function(*args, **kwargs)
                    self.dbCache.update(Document({
                        'value':_data,
                        'expire':expire,
                        'timestamp':getCurrentTimestamp(),
                        'called':increment('called') if count else cached.get('called')
                        },
                        doc_id=key))
                    if log:print(f'{function.__name__} with {functionArgs} cached.. and updated expire time')
                    return _data
                
                if cached.get('expire') and checkExpiredTimestamp(cached.get('expire'),cached.get('timestamp'),getCurrentTimestamp()):
                    if log:print(f'{function.__name__} with {functionArgs} cache expired, updating....')
                    _data = await function(*args, **kwargs)
                    self.dbCache.update(Document({
                        'value':_data,
                        'timestamp':getCurrentTimestamp(),
                        'called':increment('called') if count else cached.get('called')
                        },
                        doc_id=key))
                    if log:print(f'{function.__name__} with {functionArgs} cached..')
                    return _data
                if count:
                    self.dbCache.update(increment('called'),doc_ids=[key])
                if log:print(f'{function.__name__} with {functionArgs} cached HIT')
                return cached.get('value')
            
            @wraps(function)
            def syncWrappedFunction(*args, **kwargs):
                functionArgs = getDecoratorArgs(function,args,kwargs)
                key = createIntHashKey(f'{function.__name__}{functionArgs}')
                cached = self.dbCache.get(doc_id=key)
                
                if not cached:
                    if log:print(f'{function.__name__} with {functionArgs} cache MISS')
                    _data = function(*args, **kwargs)
                    self.dbCache.insert(Document({
                        'value':_data,
                        'function':function.__name__,
                        'Arg':functionArgs,
                        'called':0,
                        'expire':expire,
                        'timestamp':getCurrentTimestamp()
                        },
                        doc_id=key))
                    if log:print(f'{function.__name__} with {functionArgs} cached..')
                    return _data
                
                if not cached.get('expire') == expire:
                    if log:print(f'{function.__name__} with {functionArgs} updating.... expire time')
                    _data = function(*args, **kwargs)
                    self.dbCache.update(Document({
                        'value':_data,
                        'expire':expire,
                        'timestamp':getCurrentTimestamp(),
                        'called':increment('called') if count else cached.get('called')
                        },
                        doc_id=key))
                    if log:print(f'{function.__name__} with {functionArgs} cached.. and updated expire time')
                    return _data
                
                if cached.get('expire') and checkExpiredTimestamp(cached.get('expire'),cached.get('timestamp'),getCurrentTimestamp()):
                    if log:print(f'{function.__name__} with {functionArgs} cache expired, updating....')
                    _data = function(*args, **kwargs)
                    self.dbCache.update(Document({
                        'value':_data,
                        'timestamp':getCurrentTimestamp(),
                        'called':increment('called') if count else cached['called']
                        },
                        doc_id=key))
                    if log:print(f'{function.__name__} with {functionArgs} cached..')
                    return _data
                if count:
                    self.dbCache.update(increment('called'),doc_ids=[key])
                if log:print(f'{function.__name__} with {functionArgs} cached HIT')
                return cached.get('value')

            if asyncio.iscoroutinefunction(function):
                return asyncWrappedFunction
            else:
                return syncWrappedFunction
        return wrapped

