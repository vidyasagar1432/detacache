
import deta
import logging
import deta
from typing import Any, Type

from detacache.coder import BaseCoder, JsonCoder, FastAPICoder
from detacache.key import BaseKeyGen, JsonKeyGen, FastAPIKeyGen
from detacache._helpers import getCurrentTimestamp, checkExpiredTimestamp

logger = logging.getLogger(__name__)


class BaseCache:
    def __init__(self,
        db: deta._Base,
        expire: int,
        function: Any,
        args: tuple,
        kwargs: dict,
        keyGen: Type[BaseKeyGen],
        coder: Type[BaseCoder],
        ):
        self.db = db
        self.expire = expire
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.key = keyGen.get(self.function, self.args, self.kwargs)
        self.cached = self.db.get(key=self.key)
        self.coder = coder

    async def asyncCheckCached(self):
        if not self.cached or self._checkIfExpired():
                return await self._asyncFunctionCallAndPutResponseInDetaCache()
        logger.info(f'{self.function.__name__} function cached HIT')
        return self.decode()

    def syncCheckCached(self):
        if not self.cached or self._checkIfExpired():
                return self._syncFunctionCallAndPutResponseInDetaCache()
        logger.info(f'{self.function.__name__} function cached HIT')
        return self.decode()

    def _checkIfExpired(self):
        if _expired := self.cached.get('expire') != self.expire:
                logger.info(f'{self.function.__name__} function cache expire..')
        if _newExpire := self.expire and checkExpiredTimestamp(
                self.cached.get('expire'), self.cached.get('timestamp'), getCurrentTimestamp()):
                logger.info(
                f'{self.function.__name__} function updating.... expire time')
        return _newExpire or _expired

    async def _asyncFunctionCallAndPutResponseInDetaCache(self):
        self.fucResponse = await self.function(*self.args, **self.kwargs)
        return self._putDataInDetaCache()

    def _syncFunctionCallAndPutResponseInDetaCache(self):
        self.fucResponse = self.function(*self.args, **self.kwargs)
        return self._putDataInDetaCache()

    def _putDataInDetaCache(self):
        self.db.put(data=self.put(), key=self.key)
        logger.info(f'{self.function.__name__} function cached..')
        return self.fucResponse

    def put(self) -> dict:
        return {
                'value': self.encode(),
                'type': type(self.fucResponse).__name__,
                'expire': self.expire,
                'timestamp': getCurrentTimestamp()
        }

    def decode(self):
        return self.coder.decode(self.cached)

    def encode(self):
        return self.coder.encode(self.fucResponse)


class detaCache(BaseCache):
    def __init__(self,
                db: deta._Base,
                expire: int,
                function,
                args,
                kwargs,
                keyGen: Type[BaseKeyGen] = JsonKeyGen,
                coder: Type[BaseCoder] = JsonCoder
                ):
        super().__init__(db, expire, function, args, kwargs, keyGen, coder)


class fastAPICache(BaseCache):
    def __init__(self,
                db: deta._Base,
                expire: int,
                function,
                args,
                kwargs,
                keyGen: Type[BaseKeyGen] = FastAPIKeyGen,
                coder: Type[BaseCoder] = FastAPICoder
                ):
        super().__init__(db, expire, function, args, kwargs, keyGen, coder)
