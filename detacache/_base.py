
import deta
import asyncio
from functools import wraps
from deta import Deta
import logging

from ._helpers import *

logger = logging.getLogger(__name__)


class BaseCache:
    def __init__(self, db: deta._Base, key: str, expire: int, function, *args, **kwargs):
        self.db = db
        self.key = key
        self.expire = expire
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.cached = self.db.get(key=self.key)

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
        self.db.put(data={
            'value': self.serialize(),
            'type': type(self.fucResponse).__name__,
            'response': self.response,
            'expire': self.expire,
            'timestamp': getCurrentTimestamp()
        }, key=self.key)
        logger.info(f'{self.function.__name__} function cached..')
        return self.fucResponse

    def deserialize(self):
        return self.cached.get('value')

    def serialize(self):
        if isinstance(self.fucResponse, (dict, list, tuple, set, str, int, bool)):
            self.response = 'json'
            return self.fucResponse
        else:
            raise Exception("function response must be a json serializable")

    async def asyncCheckCached(self):
        if not self.cached or self._checkIfExpired():
            return await self._asyncFunctionCallAndPutResponseInDetaCache()
        logger.info(f'{self.function.__name__} function cached HIT')
        return self.deserialize()

    def syncCheckCached(self):
        if not self.cached or self._checkIfExpired():
            return self._syncFunctionCallAndPutResponseInDetaCache()
        logger.info(f'{self.function.__name__} function cached HIT')
        return self.deserialize()


class BaseDecorator:

    def __init__(self, projectKey: str = None, projectId: str = None, baseName: str = 'cache'):
        self._dbCache = Deta(projectKey, project_id=projectId).Base(baseName)
        self.cacheClass = None
        self.key = None

    def cache(self, expire: int = 0) -> None:

        def wrapped(function):
            @wraps(function)
            async def asyncWrappedFunction(*args, **kwargs):
                return await self.cacheClass(
                    self._dbCache,
                    self.key(function, args, kwargs),
                    expire,
                    function,
                    *args,
                    **kwargs
                ).asyncCheckCached()

            @wraps(function)
            def syncWrappedFunction(*args, **kwargs):
                return self.cacheClass(
                    self._dbCache,
                    self.key(function, args, kwargs),
                    expire,
                    function,
                    *args,
                    **kwargs
                ).syncCheckCached()

            if asyncio.iscoroutinefunction(function):
                return asyncWrappedFunction
            else:
                return syncWrappedFunction
        return wrapped
