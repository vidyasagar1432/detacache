
import asyncio
from functools import wraps
from deta import Deta

from ._detaCache import fastapiCache ,jsonCache
from ._helpers import *


class JsonCache:

    def __init__(self, projectKey: str = None, projectId: str = None, baseName: str = 'cache'):
        self._dbCache = Deta(project_key=projectKey,project_id=projectId).Base(baseName)

    def cache(self, expire: int = 0) -> None:

        def wrapped(function):
            @wraps(function)
            async def asyncWrappedFunction(*args, **kwargs):
                return await jsonCache(
                    self._dbCache,
                    createStringHashKey(
                        f'{function.__name__}{jsonSerializableArgs(function,args,kwargs)}'),
                    expire,
                    function,
                    *args,
                    **kwargs
                )._asyncCheckCached()

            @wraps(function)
            def syncWrappedFunction(*args, **kwargs):
                return jsonCache(
                    self._dbCache,
                    createStringHashKey(
                        f'{function.__name__}{jsonSerializableArgs(function,args,kwargs)}'),
                    expire,
                    function,
                    *args,
                    **kwargs
                )._syncCheckCached()

            if asyncio.iscoroutinefunction(function):
                return asyncWrappedFunction
            else:
                return syncWrappedFunction
        return wrapped


class FastAPICache:

    def __init__(self, projectKey: str = None, projectId: str = None, baseName: str = 'cache'):
        self._dbCache = Deta(project_key=projectKey,project_id=projectId).Base(baseName)

    def cache(self, expire: int = 0) -> None:

        def wrapped(function):
            @wraps(function)
            async def asyncWrappedFunction(*args, **kwargs):
                return await fastapiCache(
                    self._dbCache,
                    fastapiKeyGen(function,args,kwargs),
                    expire,
                    function,
                    *args,
                    **kwargs
                )._asyncCheckCached()

            @wraps(function)
            def syncWrappedFunction(*args, **kwargs):
                return fastapiCache(
                    self._dbCache,
                    fastapiKeyGen(function,args,kwargs),
                    expire,
                    function,
                    *args,
                    **kwargs
                )._syncCheckCached()

            if asyncio.iscoroutinefunction(function):
                return asyncWrappedFunction
            else:
                return syncWrappedFunction
        return wrapped
