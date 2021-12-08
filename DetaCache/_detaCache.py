
from functools import wraps
from deta import Deta

from ._helpers import getDecoratorArgs,createStringHashKey,getCurrentTimestamp,checkExpiredTimestamp



class detaCache(object):
    def __init__(self, projectKey: str = None,projectId: str = None,baseName:str='cache'):
        self.dbCache = Deta(project_key=projectKey,project_id=projectId).Base(baseName)

    def cacheAsyncFunction(self,expire:int=None,count:bool=False) -> None:
        def wrapped(function):
            @wraps(function)
            async def wrappedFunction(*args, **kwargs):
                functionArgs = getDecoratorArgs(function,args,kwargs)
                key = createStringHashKey(f'{function.__name__}{functionArgs}')
                cached = self.dbCache.get(key=key)
                if not cached:
                    _data = await function(*args, **kwargs)
                    self.dbCache.put(data={
                        'value':_data,
                        'function':function.__name__,
                        'Arg':functionArgs,
                        'expire':expire,
                        'timestamp':getCurrentTimestamp()
                        },
                        key=key)
                    return _data
                if cached['expire'] and checkExpiredTimestamp(cached['expire'],cached['timestamp'],getCurrentTimestamp()):
                    print('cache expired, updating....')
                    _data = await function(*args, **kwargs)
                    self.dbCache.update(updates={
                        'value':_data,
                        'timestamp':getCurrentTimestamp()
                        },
                        key=key)
                if count:
                    self.dbCache.update(updates={'called':self.dbCache.util.increment(1)},key=key)
                return cached['value']
            return wrappedFunction
        return wrapped

    def cacheSyncFunction(self,expire:int=None,count:bool=False)-> None:
        def wrapped(function):
            @wraps(function)
            def wrappedFunction(*args, **kwargs):
                functionArgs = getDecoratorArgs(function,args,kwargs)
                key = createStringHashKey(f'{function.__name__}{functionArgs}')
                cached = self.dbCache.get(key=key)
                if not cached:
                    _data = function(*args, **kwargs)
                    self.dbCache.put(data={
                        'value':_data,
                        'function':function.__name__,
                        'Arg':functionArgs,
                        'expire':expire,
                        'timestamp':getCurrentTimestamp()
                        },
                        key=key)
                    return _data
                if cached['expire'] and checkExpiredTimestamp(cached['expire'],cached['timestamp'],getCurrentTimestamp()):
                    print('cache expired, updating....')
                    _data = function(*args, **kwargs)
                    self.dbCache.update(updates={
                        'value':_data,
                        'timestamp':getCurrentTimestamp()
                        },
                        key=key)
                if count:
                    self.dbCache.update(updates={'called':self.dbCache.util.increment(1)},key=key)
                return cached['value']
            return wrappedFunction
        return wrapped

