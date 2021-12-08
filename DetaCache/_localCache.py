from functools import wraps
from tinydb import TinyDB,Query
from tinydb.table import Document
from tinydb.operations import increment

from ._helpers import inspectDecorator,intHashKey



class localCache(object):
    def __init__(self,filePath:str='cache.json', tableName: str = 'cache'):
        db = TinyDB(filePath)
        self.dbCache = db.table(tableName)
        self.q = Query()

    def cacheAsyncFunction(self,count:bool=False) -> None:
        def wrapped(function):
            @wraps(function)
            async def wrappedFunction(*args, **kwargs):
                arg = inspectDecorator(function,args,kwargs)
                if not arg:
                    raise
                key = intHashKey(f'{function.__name__}{arg}')
                data = self.dbCache.get(doc_id=key)
                if not data:
                    _data = await function(*args, **kwargs)
                    self.dbCache.insert(Document({
                        'value':_data,
                        'function':function.__name__,
                        'Arg':arg,
                        'called':0,
                        },
                        doc_id=key))
                    return _data
                if count:
                    self.dbCache.update(increment('called'),doc_ids=[key])
                return data.get('value')
            return wrappedFunction
        return wrapped
    
    def cacheSyncFunction(self,count:bool=False)-> None:
        def wrapped(function):
            @wraps(function)
            def wrappedFunction(*args, **kwargs):
                arg = inspectDecorator(function,args,kwargs)
                if not arg:
                    raise
                key = intHashKey(f'{function.__name__}{arg}')
                data = self.dbCache.get(doc_id=key)
                if not data:
                    _data = function(*args, **kwargs)
                    self.dbCache.insert(Document({
                        'value':_data,
                        'function':function.__name__,
                        'Arg':arg,
                        'called':0,
                        },
                        doc_id=key))
                    return _data
                if count:
                    self.dbCache.update(increment('called'),doc_ids=[key])
                return data.get('value')
            return wrappedFunction
        return wrapped
    
