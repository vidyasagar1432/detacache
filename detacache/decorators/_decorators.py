
import asyncio
from deta import Deta
from functools import wraps
from typing import Type

from detacache.cache import BaseCache, fastAPICache, detaCache
from detacache.coder import BaseCoder,JsonCoder,FastAPICoder
from detacache.key import BaseKeyGen,JsonKeyGen,FastAPIKeyGen


class BaseDecorator:

    def __init__(self, 
                projectKey: str = None, 
                projectId: str = None, 
                baseName: str = 'cache',
                keyGen:Type[BaseKeyGen]=None,
                coder:Type[BaseCoder]=None,
                cacheClass:Type[BaseCache]=None
                ):
        self._dbCache = Deta(projectKey, project_id=projectId).Base(baseName)
        self.cacheClass = cacheClass
        self.keyGen = keyGen
        self.coder=coder

    def cache(self, 
            expire: int = 0,
            keyGen:Type[BaseKeyGen]=None,
            coder:Type[BaseCoder]=None,
            cacheClass:Type[BaseCache]=None
            ) -> None:
        _cache = self.cacheClass if not cacheClass else cacheClass

        def wrapped(function):
            @wraps(function)
            async def asyncWrappedFunction(*args, **kwargs):
                return await _cache(
                    self._dbCache,
                    expire,
                    function,
                    args,
                    kwargs,
                    self.keyGen if not keyGen else keyGen,
                    self.coder if not coder else coder,
                ).asyncCheckCached()

            @wraps(function)
            def syncWrappedFunction(*args, **kwargs):
                return _cache(
                    self._dbCache,
                    expire,
                    function,
                    args,
                    kwargs,
                    self.keyGen if not keyGen else keyGen,
                    self.coder if not coder else coder,
                ).syncCheckCached()

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
                keyGen:Type[BaseKeyGen]=JsonKeyGen,
                coder:Type[BaseCoder]=JsonCoder,
                cacheClass:Type[BaseCache]=detaCache
            ):
        super().__init__(projectKey, projectId, baseName,keyGen,coder,cacheClass)


class FastAPICache(BaseDecorator):
    def __init__(self, 
                projectKey: str = None,
                projectId: str = None, 
                baseName: str = 'cache',
                keyGen:Type[BaseKeyGen]=FastAPIKeyGen,
                coder:Type[BaseCoder]=FastAPICoder,
                cacheClass:Type[BaseCache]=fastAPICache
            ):
        super().__init__(projectKey, projectId, baseName,keyGen,coder,cacheClass)

