
from typing import Any

class Coder:
    @classmethod
    def encode(cls, value: Any):
        raise NotImplementedError

    @classmethod
    def decode(cls, value: Any):
        raise NotImplementedError


JSON_CONVERTERS = {
    "dict": lambda x: dict(x),
    "list": lambda x: list(x),
    "tuple": lambda x: tuple(x),
    "float": lambda x: float(x),
    "set": lambda x: set(x),
    "str": lambda x: str(x),
    "int": lambda x: int(x),
    "bool": lambda x: bool(x),
}

def objDecode(value,con):
    _type = value.get("type")
    if not _type:
        return value

    if _type in con:
        return con[_type](value["value"])
    else:
        raise TypeError("Unknown {}".format(_type))


class DetaCoder(Coder):
    '''(dict, list, tuple, set, float, str, int, bool)'''
    
    @classmethod
    def encode(cls, value: Any):
        if isinstance(value, (dict, list, float, str, int, bool)):
            return value
        elif isinstance(value, (tuple, set)):
            return list(value)
        else:
            raise Exception(
                "function response must be (dict, list, tuple, set, float, str, int, bool)")

    @classmethod
    def decode(cls, value: Any):
        return objDecode(value,JSON_CONVERTERS)

try:
    import fastapi
    from fastapi.encoders import jsonable_encoder
    from fastapi.responses import HTMLResponse, PlainTextResponse, JSONResponse, Response
except ImportError: 
    fastapi = None 



def fastAPIdecode():
    _FASTAPIHTML = lambda x: HTMLResponse(str(x['body']), headers=dict(x['raw_headers']), status_code=x['status_code'])
    FASTAPI_CONVERTERS = {
        "_TemplateResponse":_FASTAPIHTML,
        "HTMLResponse": _FASTAPIHTML,
        "JSONResponse":lambda x: JSONResponse(str(x['body']), headers=dict(x['raw_headers']), status_code=x['status_code']),
        "PlainTextResponse": lambda x: PlainTextResponse(str(x['body']), headers=dict(x['raw_headers']), status_code=x['status_code']),
        "Response": lambda x: Response(str(x['body']), headers=dict(x['raw_headers']), status_code=x['status_code']),
    }
    FASTAPI_CONVERTERS.update(JSON_CONVERTERS)
    return FASTAPI_CONVERTERS




class FastAPICoder(Coder):
    
    @classmethod
    def encode(cls, value: Any):
        assert fastapi is not None, "fastapi must be installed to use FastAPICoder.encode"
        return jsonable_encoder(value)

    @classmethod
    def decode(cls, value: Any):
        assert fastapi is not None, "fastapi must be installed to use FastAPICoder.decode"
        return objDecode(value,fastAPIdecode())

class StarletteCoder(FastAPICoder):
    pass
