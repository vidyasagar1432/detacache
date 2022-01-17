import inspect
import hashlib
from datetime import datetime
from deta import _Base
from typing import Union
from starlette.templating import _TemplateResponse
from starlette.responses import HTMLResponse
from fastapi import Request


def getDecoratorArgs(func, args, kwargs):
    '''Returns Args and Kwargs of function as `dict`'''
    argspec = inspect.getfullargspec(func)

    data = {str(argspec.args[index]): str(arg) if isinstance(arg,
            (dict, list, str, int, bool)) else str(arg.url) if isinstance(arg, Request) else None
            for index, arg in enumerate(args) if argspec.args and type(argspec.args is list)}

    data.update({str(k): str(v) if isinstance(v, (dict, list, str, int, bool))
                else str(v.url) if isinstance(v, Request) else None
                for k, v in kwargs.items() if kwargs})

    return data


def createIntHashKey(string: str):
    '''Returns a md5 Hash of string as `int`'''
    return int(hashlib.md5(str(string).encode()).hexdigest(), 16)


def createStringHashKey(string: str):
    '''Returns a md5 Hash of string as `string`'''
    return hashlib.md5(str(string).encode()).hexdigest()


def getCurrentTimestamp():
    '''Returns Current Timestamp as `int`'''
    return int(round(datetime.now().timestamp()))


def checkExpiredTimestamp(expire: int, initialTimestamp: int, currentTimestamp: int):
    '''Returns `True` if expired else `False`'''
    return initialTimestamp + expire < currentTimestamp


async def asyncCheckCached(db: _Base, key: str, expire: int, function, *args, **kwargs):
    cached = db.get(key=key)

    if not cached:
        print('cached')
        return putDataIntoDetaCache(await function(*args, **kwargs), db, key, expire)

    if cached.get('expire') != expire or (expire and checkExpiredTimestamp(cached['expire'], cached['timestamp'], getCurrentTimestamp())):
        print('cache expired')
        return updateDataIntoDetaCache(await function(*args, **kwargs), db, key, expire)
    print('cache hit')
    return cached['value'] if not cached['html'] else HTMLResponse(content=cached['value'])


def syncCheckCached(db: _Base, key: str, expire: int, function, *args, **kwargs):
    cached = db.get(key=key)

    if not cached:
        print('cached')
        return putDataIntoDetaCache(function(*args, **kwargs), db, key, expire)

    if cached.get('expire') != expire or (expire and checkExpiredTimestamp(cached['expire'], cached['timestamp'], getCurrentTimestamp())):
        print('cache expired')
        return updateDataIntoDetaCache(function(*args, **kwargs), db, key, expire)
    print('cache hit')
    return cached['value'] if not cached['html'] else HTMLResponse(content=cached['value'])


def inDbValue(data: Union[dict, list, str, int, bool, _TemplateResponse], expire: int):
    inDb = {'value': data, 'expire': expire,
            'html': False, 'timestamp': getCurrentTimestamp()}

    if isinstance(data, _TemplateResponse):
        inDb['value'] = str(data.body, 'utf-8')
        inDb['html'] = True

    return inDb


def putDataIntoDetaCache(data: Union[dict, list, str, int, bool, _TemplateResponse], db: _Base, key: str, expire: int):
    inDb = inDbValue(data=data, expire=expire)

    db.put(data=inDb, key=key)
    print('putDataIntoDetaCache')
    return data if not inDb['html'] else HTMLResponse(content=inDb['value'])


def updateDataIntoDetaCache(data: Union[dict, list, str, int, bool, _TemplateResponse], db: _Base, key: str, expire: int):
    inDb = inDbValue(data=data, expire=expire)

    db.update(updates=inDbValue(data=data, expire=expire), key=key)
    print('updateDataIntoDetaCache')
    return data if not inDb['html'] else HTMLResponse(content=inDb['value'])
