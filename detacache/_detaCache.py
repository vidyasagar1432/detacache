
import asyncio
from functools import wraps
from deta import Deta

from ._baseCache import jsonSerializableCache, fastapiCache
from ._helpers import *


class JsonCache:

    def __init__(self, projectKey: str = None, projectId: str = None, baseName: str = 'cache'):
        self._dbCache = Deta(project_key=projectKey,
                             project_id=projectId).Base(baseName)

    def cache(self, expire: int = 0) -> None:

        def wrapped(function):
            @wraps(function)
            async def asyncWrappedFunction(*args, **kwargs):
                return await jsonSerializableCache(
                    self._dbCache,
                    createStringHashKey(
                        f'{function.__name__}{getDecoratorArgs(function,args,kwargs).jsonSerializableArgs()}'),
                    expire,
                    function,
                    *args,
                    **kwargs
                ).asyncCheckCached()

            @wraps(function)
            def syncWrappedFunction(*args, **kwargs):
                return jsonSerializableCache(
                    self._dbCache,
                    createStringHashKey(
                        f'{function.__name__}{getDecoratorArgs(function,args,kwargs).jsonSerializableArgs()}'),
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


class FastAPICache:

    def __init__(self, projectKey: str = None, projectId: str = None, baseName: str = 'cache'):
        self._dbCache = Deta(project_key=projectKey,
                             project_id=projectId).Base(baseName)

    def cache(self, expire: int = 0) -> None:

        def wrapped(function):
            @wraps(function)
            async def asyncWrappedFunction(*args, **kwargs):
                return await fastapiCache(
                    self._dbCache,
                    createStringHashKey(
                        f'{function.__name__}{getDecoratorArgs(function,args,kwargs).fastapiArgs()}'),
                    expire,
                    function,
                    *args,
                    **kwargs
                ).asyncCached()

            @wraps(function)
            def syncWrappedFunction(*args, **kwargs):
                return fastapiCache(
                    self._dbCache,
                    createStringHashKey(
                        f'{function.__name__}{getDecoratorArgs(function,args,kwargs).fastapiArgs()}'),
                    expire,
                    function,
                    *args,
                    **kwargs
                ).syncCached()

            if asyncio.iscoroutinefunction(function):
                return asyncWrappedFunction
            else:
                return syncWrappedFunction
        return wrapped
