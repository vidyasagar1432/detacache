from functools import wraps
from tinydb import TinyDB,Query
from tinydb.table import Document
from tinydb.operations import increment

from ._helpers import getDecoratorArgs,createIntHashKey,getCurrentTimestamp,checkExpiredTimestamp


class localCache(object):
    def __init__(self,filePath:str='cache.json', tableName: str = 'cache'):
        db = TinyDB(filePath)
        self.dbCache = db.table(tableName)
        self.q = Query()

    def cacheAsyncFunction(self,expire:int=None,count:bool=False) -> None:
        def wrapped(function):
            @wraps(function)
            async def wrappedFunction(*args, **kwargs):
                functionArgs = getDecoratorArgs(function,args,kwargs)
                key = createIntHashKey(f'{function.__name__}{functionArgs}')
                cached = self.dbCache.get(doc_id=key)
                if not cached:
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
                    return _data
                if cached.get('expire') and checkExpiredTimestamp(cached.get('expire'),cached.get('timestamp'),getCurrentTimestamp()):
                    print('cache expired, updating....')
                    _data = await function(*args, **kwargs)
                    self.dbCache.update(Document({
                        'value':_data,
                        'timestamp':getCurrentTimestamp()
                        },
                        doc_id=key))
                    return _data
                if count:
                    self.dbCache.update(increment('called'),doc_ids=[key])
                return cached.get('value')
            return wrappedFunction
        return wrapped
    
    def cacheSyncFunction(self,expire:int=None,count:bool=False)-> None:
        def wrapped(function):
            @wraps(function)
            def wrappedFunction(*args, **kwargs):
                functionArgs = getDecoratorArgs(function,args,kwargs)
                key = createIntHashKey(f'{function.__name__}{functionArgs}')
                cached = self.dbCache.get(doc_id=key)
                if not cached:
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
                    return _data
                if cached.get('expire') and checkExpiredTimestamp(cached.get('expire'),cached.get('timestamp'),getCurrentTimestamp()):
                    print('cache expired, updating....')
                    _data = function(*args, **kwargs)
                    self.dbCache.update(Document({
                        'value':_data,
                        'timestamp':getCurrentTimestamp()
                        },
                        doc_id=key))
                    return _data
                if count:
                    self.dbCache.update(increment('called'),doc_ids=[key])
                return cached.get('value')
            return wrappedFunction
        return wrapped
    
