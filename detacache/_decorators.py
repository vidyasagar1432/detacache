
from ._cache import starletteCache, detaCache
from ._helpers import jsonKeyGen, starletteKeyGen
from ._base import BaseDecorator


class DetaCache(BaseDecorator):
    def __init__(self, projectKey: str = None, projectId: str = None, baseName: str = 'cache'):
        super().__init__(projectKey, projectId, baseName)
        self.cacheClass = detaCache
        self.key = jsonKeyGen


class StarletteCache(BaseDecorator):
    def __init__(self, projectKey: str = None, projectId: str = None, baseName: str = 'cache'):
        super().__init__(projectKey, projectId, baseName)
        self.cacheClass = starletteCache
        self.key = starletteKeyGen


class FastAPICache(StarletteCache):
    def __init__(self, projectKey: str = None, projectId: str = None, baseName: str = 'cache'):
        super().__init__(projectKey, projectId, baseName)
