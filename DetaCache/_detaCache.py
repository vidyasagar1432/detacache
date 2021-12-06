from functools import wraps
from deta import Deta

from ._helpers import inspectDecorator

class detaCache(object):
    def __init__(self, projectKey: str = None,projectId: str = None,baseName:str='cache'):
        self.dbCache = Deta(project_key=projectKey,project_id=projectId).Base(baseName)

    def cacheAsyncFunction(self,count:bool=False) -> None:
        def wrapped(function):
            @wraps(function)
            async def wrappedFunction(*args, **kwargs):
                print(function.__name__)
                arg = inspectDecorator(function,args,kwargs)
                if not arg:
                    raise 
                data = self.dbCache.fetch(query={'function':function.__name__,'Arg':arg}).items
                if not data:
                    _data = await function(*args, **kwargs)
                    self.dbCache.put(data={'value':_data,'function':function.__name__,'Arg':arg})
                    return _data
                if count:
                    self.dbCache.update(updates={'called':self.dbCache.util.increment(1)},key=data[0]['key'])
                return data[0]['value']
            return wrappedFunction
        return wrapped
    
    def cacheSyncFunction(self,count:bool=False)-> None:
        def wrapped(function):
            @wraps(function)
            def wrappedFunction(*args, **kwargs):
                print(function.__name__)
                arg = inspectDecorator(function,args,kwargs)
                if not arg:
                    raise 
                data = self.dbCache.fetch(query={'function':function.__name__,'Arg':arg}).items
                if not data:
                    _data = function(*args, **kwargs)
                    self.dbCache.put(data={'value':_data,'function':function.__name__,'Arg':arg})
                    return _data
                if count:
                    self.dbCache.update(updates={'called':self.dbCache.util.increment(1)},key=data[0]['key'])
                return data[0]['value']
            return wrappedFunction
        return wrapped