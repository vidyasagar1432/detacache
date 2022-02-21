
from starlette.responses import HTMLResponse, PlainTextResponse, Response

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


_FASTAPIHTML= lambda x: HTMLResponse(str(x['body']), headers=dict(x['raw_headers']), status_code=x['status_code'])


FASTAPI_CONVERTERS = {
    "_TemplateResponse": _FASTAPIHTML,
    "HTMLResponse": _FASTAPIHTML,
    "PlainTextResponse": lambda x: PlainTextResponse(str(x['body']), headers=dict(x['raw_headers']), status_code=x['status_code']),
    "Response": lambda x: Response(str(x['body']), headers=dict(x['raw_headers']), status_code=x['status_code']),
}

FASTAPI_CONVERTERS.update(JSON_CONVERTERS)
