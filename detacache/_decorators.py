
from ._cache import starletteCache ,jsonCache
from ._helpers import jsonKeyGen, starletteKeyGen
from ._base import BaseDecorator

class JsonCache(BaseDecorator):
    def __init__(self, projectKey: str = None, projectId: str = None, baseName: str = 'cache'):
        super().__init__(projectKey, projectId, baseName)
        self.cacheClass = jsonCache
        self.key = jsonKeyGen


class StarletteCache(BaseDecorator):
    def __init__(self, projectKey: str = None, projectId: str = None, baseName: str = 'cache'):
        super().__init__(projectKey, projectId, baseName)
        self.cacheClass = starletteCache
        self.key = starletteKeyGen


class FastAPICache(StarletteCache):
    def __init__(self, projectKey: str = None, projectId: str = None, baseName: str = 'cache'):
        super().__init__(projectKey, projectId, baseName)

