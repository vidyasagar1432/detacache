
import asyncio
from functools import wraps
from deta import Deta

from ._helpers import *


class DetaCache:
    ''' DetaCache.

    Args:
        projectKey (str): Sets the projectKey of Deta .
        projectId (str, optional): Sets the projectId of Deta.
        baseName (str,optional): Sets the name of DetaBase. Defaults to `cache`.

    Example:
        Calling `DetaCache` gives an instance of DetaCache.
    ```
        import aiohttp
        import requests
        from detacache import DetaCache

        app = DetaCache('projectKey')

        @app.cache()
        async def asyncgetjSON(url:str):
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    return await response.json()

        @app.cache()
        def syncgetjSON(url:str):
            return requests.get(url).json()
    ```
    <https://github.com/vidyasagar1432/detacache>
    '''

    def __init__(self, projectKey: str = None, projectId: str = None, baseName: str = 'cache'):
        self._dbCache = Deta(project_key=projectKey,
                            project_id=projectId).Base(baseName)

    def cache(self, expire: int = 0) -> None:
        '''
        Args:
            expire (int, optional): Sets the expire time to expire in sec . Defaults to `0`.
        <https://github.com/vidyasagar1432/detacache>
        '''
        def wrapped(function):
            @wraps(function)
            async def asyncWrappedFunction(*args, **kwargs):
                return await asyncCheckCached(
                    self._dbCache,
                    createStringHashKey(
                        f'{function.__name__}{getDecoratorArgs(function,args,kwargs)}'),
                    expire,
                    function,
                    *args,
                    **kwargs)

            @wraps(function)
            def syncWrappedFunction(*args, **kwargs):
                return syncCheckCached(
                    self._dbCache,
                    createStringHashKey(
                        f'{function.__name__}{getDecoratorArgs(function,args,kwargs)}'),
                    expire,
                    function,
                    *args,
                    **kwargs)
            if asyncio.iscoroutinefunction(function):
                return asyncWrappedFunction
            else:
                return syncWrappedFunction
        return wrapped
