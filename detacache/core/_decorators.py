
import asyncio

from functools import wraps
from typing import Any, Type, Callable

from ._coder import Coder, DetaCoder, FastAPICoder,StarletteCoder
from ._key import KeyGenerator, DetaKey, FastAPIKey,StarletteKey
from ._detaBase import SyncBase, AsyncBase
from ._helpers import getCurrentTimestamp


class BaseDecorator:

    def __init__(self,
                 projectKey: str = None,
                 projectId: str = None,
                 baseName: str = 'cache',
                 key: KeyGenerator = None,
                 coder: Coder = None,
                 expire: int = 0,
                 ):

        self._syncDb = SyncBase(projectKey, baseName, projectId)
        self._asyncDb = AsyncBase(projectKey, baseName, projectId)
        self.key = key
        self.coder = coder
        self.expire = expire

    def putDataInBase(self, response: Any, coder: Coder, expire: int) -> dict:
        return {
            'value': coder.encode(response),
            'type': type(response).__name__,
            '__expires': getCurrentTimestamp() + expire,
        }

    def cache(self,
              expire: int = 0,
              key: KeyGenerator = None,
              coder: Coder = None,
              ) -> None:

        key = key or self.key
        coder = coder or self.coder
        expire = expire or self.expire

        def wrapped(function):

            @wraps(function)
            async def asyncWrappedFunction(*args, **kwargs):
                _key = key.generate(function, args, kwargs)
                cached = await self._asyncDb.get(key.generate(function, args, kwargs))

                if not cached:
                    functionResponse = await function(*args, **kwargs)
                    await self._asyncDb.put(self.putDataInBase(functionResponse, coder, expire), _key)
                    return functionResponse

                return coder.decode(cached)

            @wraps(function)
            def syncWrappedFunction(*args, **kwargs):
                _key = key.generate(function, args, kwargs)
                cached = self._syncDb.get(_key)

                if not cached:
                    functionResponse = function(*args, **kwargs)
                    self._syncDb.put(self.putDataInBase(
                        functionResponse, coder, expire), _key)
                    return functionResponse

                return coder.decode(cached)

            if asyncio.iscoroutinefunction(function):
                return asyncWrappedFunction
            else:
                return syncWrappedFunction

        return wrapped


class DetaCache(BaseDecorator):
    def __init__(self,
                 projectKey: str = None,
                 projectId: str = None,
                 baseName: str = 'cache',
                 key: KeyGenerator = DetaKey,
                 coder: Coder = DetaCoder,
                 ):
        super().__init__(projectKey, projectId, baseName, key, coder)

class FastAPICache(BaseDecorator):
    def __init__(self,
                 projectKey: str = None,
                 projectId: str = None,
                 baseName: str = 'cache',
                 key: KeyGenerator = FastAPIKey,
                 coder: Coder = FastAPICoder,
                 ):
        super().__init__(projectKey, projectId, baseName, key, coder)

class StarletteCache(BaseDecorator):
    def __init__(self,
                 projectKey: str = None,
                 projectId: str = None,
                 baseName: str = 'cache',
                 key: KeyGenerator = StarletteKey,
                 coder: Coder = StarletteCoder,
                 ):
        super().__init__(projectKey, projectId, baseName, key, coder)