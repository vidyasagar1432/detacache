
import deta
from starlette.templating import _TemplateResponse
from starlette.responses import HTMLResponse,PlainTextResponse

from ._baseCache import BaseCache


class jsonCache(BaseCache):
    def __init__(self, db: deta._Base,key:str, expire: int, function, *args, **kwargs):
        super().__init__(db,key, expire, function, *args, **kwargs)


class fastapiCache(BaseCache):
    def __init__(self, db: deta._Base,key:str, expire: int, function, *args, **kwargs):
        super().__init__(db,key, expire, function, *args, **kwargs)

    def _deserialize(self):
        if self.cached.get('type') in ['_TemplateResponse','HTMLResponse']:
            return HTMLResponse(content=self.cached.get('value'),headers={'cache-hit',True})
        if self.cached.get('type') == 'PlainTextResponse':
            return PlainTextResponse(content=self.cached.get('value'),headers={'cache-hit',True})
        return self.cached.get('value')
    
    def _serialize(self,):
        if isinstance(self.fucResponse,(dict, list,tuple,set, str, int, bool)):
            return self.fucResponse
        if isinstance(self.fucResponse,(_TemplateResponse,HTMLResponse,PlainTextResponse)):
            return str(self.fucResponse.body,'utf-8')


# class fastapiCache(starletteCache):
#     def __init__(self, db: deta._Base, key: str, expire: int, function, *args, **kwargs):
#         super().__init__(db, key, expire, function, *args, **kwargs)


