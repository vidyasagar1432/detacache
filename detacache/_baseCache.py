import deta
from ._helpers import *

class BaseCache:
    def __init__(self, db: deta._Base,key:str, expire: int, function, *args, **kwargs):
        self.db = db
        self.key = key
        self.expire = expire
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.cached = self.db.get(key=self.key)


    def _deserialize(self):
        return self.cached.get('value')
    
    def _serialize(self):
        if isinstance(self.fucResponse,(dict, list,tuple,set, str, int, bool)):
            return self.fucResponse

    def _checkIfExpired(self):
        return self.cached.get('expire') != self.expire or (
            self.expire and checkExpiredTimestamp(
                self.cached.get('expire'), self.cached.get('timestamp'), getCurrentTimestamp()))

    async def _asyncPutDataInDetaCache(self):
        self.fucResponse = await self.function(*self.args, **self.kwargs)
        return self._putDataInDetaCache()

    def _syncPutDataInDetaCache(self):
        self.fucResponse = self.function(*self.args, **self.kwargs)
        return self._putDataInDetaCache()
    
    def _putDataInDetaCache(self):
        self.db.put(data={
            'value': self._serialize(),
            'type':type(self.fucResponse).__name__,
            'expire': self.expire, 
            'timestamp': getCurrentTimestamp()
            }, 
            key=self.key)
        print('cached')
        return self.fucResponse

    async def _asyncCheckCached(self):
        if not self.cached or self._checkIfExpired():
            return await self._asyncPutDataInDetaCache()
        print('cache hit')
        return self._deserialize()

    def _syncCheckCached(self):
        if not self.cached or self._checkIfExpired():
            return self._syncPutDataInDetaCache()
        print('cache hit')
        return self._deserialize()
