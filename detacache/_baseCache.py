
import deta
from ._helpers import *
from starlette.templating import _TemplateResponse
from starlette.responses import HTMLResponse


class jsonSerializableCache:
    def __init__(self, db: deta._Base, key: str, expire: int, function, *args, **kwargs):
        self.db = db
        self.key = key
        self.expire = expire
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self._getCached()

    def _getCached(self):
        self.cached = self.db.get(key=self.key)

    async def _asyncFuc(self):
        self.fucResponse = await self.function(*self.args, **self.kwargs)

    def _syncFuc(self):
        self.fucResponse = self.function(*self.args, **self.kwargs)

    def _checkIfExpired(self):
        return self.cached['expire'] != self.expire or (
            self.expire and checkExpiredTimestamp(
                self.cached['expire'], self.cached['timestamp'], getCurrentTimestamp()))

    def _inDbValue(self):
        return {'value': self.fucResponse, 'expire': self.expire, 'timestamp': getCurrentTimestamp()}

    def _putDataInDetaCache(self):
        self.db.put(data=self._inDbValue(), key=self.key)
        print('cached')
        return self.fucResponse

    def _updateDataInDetaCache(self):
        self.db.update(updates=self._inDbValue(), key=self.key)
        print('cache expired')
        return self.fucResponse

    async def _asyncCheckCached(self):
        if not self.cached:
            await self._asyncFuc()
            return self._putDataInDetaCache()
        if self._checkIfExpired():
            await self._asyncFuc()
            return self._updateDataInDetaCache()
        print('cache hit')
        return self.cached['value']

    def _syncCheckCached(self):
        if not self.cached:
            self._syncFuc()
            return self._putDataInDetaCache()
        if self._checkIfExpired():
            self._syncFuc()
            return self._updateDataInDetaCache()
        print('cache hit')
        return self.cached['value']

    async def asyncCheckCached(self):
        return await self._asyncCheckCached()

    def syncCheckCached(self):
        return self._syncCheckCached()


class fastapiCache(jsonSerializableCache):

    def __init__(self, db: deta._Base, key: str, expire: int, function, *args, **kwargs):
        super().__init__(db, key, expire, function, *args, **kwargs)

    def _inDbValue(self):
        inDb = {'value': self.fucResponse, 'expire': self.expire,
                'html': False, 'timestamp': getCurrentTimestamp()}
        self.html = False
        if isinstance(self.fucResponse, _TemplateResponse):
            inDb['value'] = str(self.fucResponse.body, 'utf-8')
            inDb['html'] = True
            self.html = True
        return inDb

    async def asyncCached(self):
        f = await self._asyncCheckCached()
        return f if not (self.cached and self.cached['html']) else HTMLResponse(content=self.cached['value'])

    def syncCached(self):
        f = self._syncCheckCached()
        return f if not (self.cached and self.cached['html']) else HTMLResponse(content=self.cached['value'])
