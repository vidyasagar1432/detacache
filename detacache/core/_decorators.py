
import asyncio

from functools import wraps
from typing import Any, Type, Callable

from ._coder import Coder,DetaCoder
from ._key import detaKeyGen
from ._detaBase import SyncBase,AsyncBase
from ._helpers import getCurrentTimestamp


class BaseDecorator:

    def __init__(self, 
                projectKey: str = None, 
                projectId: str = None, 
                baseName: str = 'cache',
                keyGen:Type[Callable] = None,
                coder:Type[Coder] = None,
                expire: int = 0,
                ):
        self._syncDb = SyncBase(projectKey, baseName,projectId)
        self._asyncDb = AsyncBase(projectKey, baseName,projectId)
        self.keyGen = keyGen
        self.coder=coder
        self.expire = expire

    def putDataInBase(self,data: Any,expire:int) -> dict:
        return {
                'value': self.coder.encode(data),
                'type': type(data).__name__,
                '__expires':getCurrentTimestamp() + expire,
            }
    
    def cache(self, 
            expire: int = 0,
            keyGen:Type[Callable]=None,
            coder:Type[Coder]=None,
            ) -> None:
        
        keyGen = keyGen or self.keyGen
        coder = coder or self.coder
        expire = expire or self.expire
        
        def wrapped(function):
            @wraps(function)
            async def asyncWrappedFunction(*args, **kwargs):
                key = keyGen(function, args, kwargs)        
                cached = await self._asyncDb.get(key=key)
                if not cached:
                    functionResponse = await function(*args, **kwargs)
                    await self._asyncDb.put(data=self.putDataInBase(functionResponse,expire=expire), key=key)
                    return functionResponse
                return self.coder.decode(cached)

            @wraps(function)
            def syncWrappedFunction(*args, **kwargs):
                key = keyGen(function, args, kwargs)        
                cached = self._syncDb.get(key=key)
                if not cached:
                    functionResponse = function(*args, **kwargs)
                    self._syncDb.put(data=self.putDataInBase(functionResponse,expire=expire), key=key)
                    return functionResponse
                return self.coder.decode(cached)
            
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
                keyGen:Callable=detaKeyGen,
                coder:Type[Coder]=DetaCoder,
            ):
        super().__init__(projectKey, projectId, baseName,keyGen,coder)


