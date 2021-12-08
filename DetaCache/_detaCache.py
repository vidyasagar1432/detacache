from functools import wraps
from deta import Deta

from ._helpers import inspectDecorator,stringHashKey


class detaCache(object):
    def __init__(self, projectKey: str = None,projectId: str = None,baseName:str='cache'):
        self.dbCache = Deta(project_key=projectKey,project_id=projectId).Base(baseName)

    def cacheAsyncFunction(self,count:bool=False) -> None:
        def wrapped(function):
            @wraps(function)
            async def wrappedFunction(*args, **kwargs):
                arg = inspectDecorator(function,args,kwargs)
                if not arg:
                    arg = None
                key=stringHashKey(f'{function.__name__}{arg}')
                data = self.dbCache.get(key=key)
                if not data:
                    _data = await function(*args, **kwargs)
                    self.dbCache.put(data={'value':_data,'function':function.__name__,'Arg':arg},key=key)
                    return _data
                if count:
                    self.dbCache.update(updates={'called':self.dbCache.util.increment(1)},key=key)
                return data['value']
            return wrappedFunction
        return wrapped
    
    def cacheSyncFunction(self,count:bool=False)-> None:
        def wrapped(function):
            @wraps(function)
            def wrappedFunction(*args, **kwargs):
                arg = inspectDecorator(function,args,kwargs)
                if not arg:
                    arg = None
                key = stringHashKey(f'{function.__name__}{arg}')
                data = self.dbCache.get(key=key)
                if not data:
                    _data = function(*args, **kwargs)
                    self.dbCache.put(data={'value':_data,'function':function.__name__,'Arg':arg},key=key)
                    return _data
                if count:
                    self.dbCache.update(updates={'called':self.dbCache.util.increment(1)},key=key)
                return data['value']
            return wrappedFunction
        return wrapped
    
    
    