
import deta
import logging
from starlette.templating import _TemplateResponse
from starlette.responses import HTMLResponse,PlainTextResponse,Response
from fastapi.encoders import jsonable_encoder


from ._base import BaseCache

logger = logging.getLogger(__name__)

class detaCache(BaseCache):
    def __init__(self, db: deta._Base,key:str, expire: int, function, *args, **kwargs):
        super().__init__(db,key, expire, function, *args, **kwargs)


class starletteCache(BaseCache):
    def __init__(self, db: deta._Base,key:str, expire: int, function, *args, **kwargs):
        super().__init__(db,key, expire, function, *args, **kwargs)
    
    def deserialize(self):
        # logger.info('`{}` function response is of type `{}`'.format(self.function.__name__,self.cached.get('type')))
        if self.cached.get('response') != 'json':
            return Response(self.cached.get('value'))
        return self.cached.get('value')
    
    def serialize(self,):
        self.response = 'json'
        # return jsonable_encoder(self.fucResponse)
        if isinstance(self.fucResponse,(dict, list,tuple, str, int, bool)):
            return self.fucResponse
        elif isinstance(self.fucResponse,(_TemplateResponse,HTMLResponse,PlainTextResponse,Response)):
            self.response = 'fastapi/starlette'
            return str(self.fucResponse.body,'utf-8')
        else:
            raise Exception("function response must be a json serializable or instance of [_TemplateResponse,HTMLResponse,PlainTextResponse,Response]")


# class fastapiCache(starletteCache):
#     def __init__(self, db: deta._Base, key: str, expire: int, function, *args, **kwargs):
#         super().__init__(db, key, expire, function, *args, **kwargs)


