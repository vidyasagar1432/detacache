
import inspect
import hashlib
import datetime
from starlette.requests import Request
from starlette.responses import Response

def jsonSerializableArgs(function,args:tuple,kwargs:dict):
    '''Returns Args and Kwargs of function as `dict`'''

    argspec = inspect.getfullargspec(function)
    
    data = {str(argspec.args[index]): str(arg) if isinstance(arg,
            (dict, list,tuple,set, str, int, bool)) else None for index, arg in enumerate(args)
            if argspec.args and type(argspec.args is list)}

    data.update({str(k): str(v) if isinstance(v, (dict, list,tuple,set, str, int, bool))
                    else None for k, v in kwargs.items() if kwargs})

    return data

def fastapiKeyGen(function,args:tuple,kwargs:dict,):
    '''Returns Args and Kwargs of function as `dict`'''

    request = kwargs.get('request')

    assert request, f"function {function.__name__} needs a `request` argument"

    if not isinstance(request,Request):
        raise Exception("`request` must be an instance of  starlette.request.Request")
    
    return createStringHashKey(f'{function.__name__}{request.url}')


def createIntHashKey(string: str):
    '''Returns a md5 Hash of string as `int`'''
    return int(hashlib.md5(str(string).encode()).hexdigest(), 16)


def createStringHashKey(string: str):
    '''Returns a md5 Hash of string as `string`'''
    return hashlib.md5(str(string).encode()).hexdigest()


def getCurrentTimestamp():
    '''Returns Current Timestamp as `int`'''
    return int(round(datetime.datetime.now().timestamp()))


def checkExpiredTimestamp(expire: int, initialTimestamp: int, currentTimestamp: int):
    '''Returns `True` if expired else `False`'''
    return initialTimestamp + expire < currentTimestamp