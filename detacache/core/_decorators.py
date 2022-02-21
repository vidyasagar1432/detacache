
import asyncio
from functools import wraps
from typing import Type

from ._coder import Coder,JsonCoder,FastAPICoder,DetaCoder
from ._key import KeyGen,JsonKeyGen,FastAPIKeyGen,DetaKeyGen
from ._detaBase import SyncBase,AsyncBase
from ._cache import AsyncCache,SyncCache



class BaseDecorator:

    def __init__(self, 
                projectKey: str = None, 
                projectId: str = None, 
                baseName: str = 'cache',
                keyGen:Type[KeyGen] = None,
                coder:Type[Coder] = None,
                ):
        self._syncDb = SyncBase(projectKey, baseName,projectId)
        self._asyncDb = AsyncBase(projectKey, baseName,projectId)
        self.keyGen = keyGen
        self.coder=coder

    def cache(self, 
            expire: int = 0,
            keyGen:Type[KeyGen]=None,
            coder:Type[Coder]=None,
            ) -> None:

        def wrapped(function):
            @wraps(function)
            async def asyncWrappedFunction(*args, **kwargs):
                return await AsyncCache(
                    self._asyncDb,
                    expire,
                    function,
                    args,
                    kwargs,
                    keyGen if keyGen else self.keyGen,
                    coder if coder else self.coder,
                ).checkCached()

            @wraps(function)
            def syncWrappedFunction(*args, **kwargs):
                return SyncCache(
                    self._syncDb,
                    expire,
                    function,
                    args,
                    kwargs,
                    keyGen if keyGen else self.keyGen,
                    coder if coder else self.coder,
                ).checkCached()

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
                keyGen:Type[KeyGen]=DetaKeyGen,
                coder:Type[Coder]=DetaCoder,
            ):
        super().__init__(projectKey, projectId, baseName,keyGen,coder)

class JsonCache(BaseDecorator):
    def __init__(self, 
                projectKey: str = None,
                projectId: str = None, 
                baseName: str = 'cache',
                keyGen:Type[KeyGen]=JsonKeyGen,
                coder:Type[Coder]=JsonCoder,
            ):
        super().__init__(projectKey, projectId, baseName,keyGen,coder)


class FastAPICache(BaseDecorator):
    def __init__(self, 
                projectKey: str = None,
                projectId: str = None, 
                baseName: str = 'cache',
                keyGen:Type[KeyGen]=FastAPIKeyGen,
                coder:Type[Coder]=FastAPICoder,
            ):
        super().__init__(projectKey, projectId, baseName,keyGen,coder)

