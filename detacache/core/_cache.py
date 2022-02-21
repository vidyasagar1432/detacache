

from typing import Any, Type
import logging

from ._coder import Coder
from ._key import KeyGen
from ._detaBase import DetaBase,SyncBase,AsyncBase
from ._helpers import getCurrentTimestamp,checkExpiredTimestamp


logger = logging.getLogger(__name__)

class Cache:
    def __init__(self,
        db: DetaBase,
        expire: int,
        function: Any,
        args: tuple,
        kwargs: dict,
        keyGen: Type[KeyGen],
        coder: Type[Coder],
    ):
        self.db = db
        self.expire = expire
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.key = keyGen.get(self.function, self.args, self.kwargs)
        self.coder = coder
    
    def getCached(self):
        '''create `cached` variable'''
        raise NotImplementedError
    
    def putCache(self):
        '''put `cached`'''
        raise NotImplementedError
    
    def functionCall(self):
        '''create `fucResponse` variable'''
        raise NotImplementedError
    
    def checkCached(self):
        raise NotImplementedError
    
    def putValue(self,data: Any) -> dict:
        return {
                'value': self.coder.encode(data),
                'type': type(data).__name__,
                'expire': self.expire,
                'timestamp': getCurrentTimestamp()
            }
    
    def checkIfCachedOrExpired(self,cached:dict):
        if not cached:
            logger.info(f'{self.function.__name__} function has no cache..')
            return True
        if cached.get('expire') != self.expire:
                logger.info(f'{self.function.__name__} function updating.... expire time ')
                return True
        if self.expire and checkExpiredTimestamp(
                cached.get('expire'), cached.get('timestamp'), getCurrentTimestamp()):
                logger.info(f'{self.function.__name__} function cache expire..')
                return True

class SyncCache(Cache):
    def __init__(self, db: SyncBase, expire: int, function: Any, args: tuple, kwargs: dict, keyGen: Type[KeyGen], coder: Type[Coder]):
        super().__init__(db, expire, function, args, kwargs, keyGen, coder)
    
    def getCache(self):
        self.cached = self.db.get(key=self.key)
        return self.cached
    
    def putCache(self,data: Any):
        self.db.put(data=self.putValue(data), key=self.key)
        logger.info(f'{self.function.__name__} function cached..')
        return data
        
    def functionCall(self):
        return self.function(*self.args, **self.kwargs)
    
    def checkCached(self):
        if self.checkIfCachedOrExpired(self.getCache()):
            return self.putCache(self.functionCall())
        logger.info(f'{self.function.__name__} function cached HIT')
        return self.coder.decode(self.cached)


class AsyncCache(Cache):
    def __init__(self, db: AsyncBase, expire: int, function: Any, args: tuple, kwargs: dict, keyGen: Type[KeyGen], coder: Type[Coder]):
        super().__init__(db, expire, function, args, kwargs, keyGen, coder)
    
    async def getCache(self):
        self.cached = await self.db.get(key=self.key)
        return self.cached
    
    async def putCache(self,data: Any):
        await self.db.put(data=self.putValue(data), key=self.key)
        logger.info(f'{self.function.__name__} function cached..')
        return data
    
    async def functionCall(self):
        return await self.function(*self.args, **self.kwargs)
    
    async def checkCached(self):
        if self.checkIfCachedOrExpired(await self.getCache()):
            return await self.putCache(await self.functionCall())
        logger.info(f'{self.function.__name__} function cached HIT')
        return self.coder.decode(self.cached)


