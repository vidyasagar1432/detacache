
import inspect
import hashlib
import datetime
from fastapi import Request


class getDecoratorArgs:
    def __init__(self, func, args, kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.argspec = inspect.getfullargspec(self.func)

    def jsonSerializableArgs(self):
        '''Returns Args and Kwargs of function as `dict`'''

        data = {str(self.argspec.args[index]): str(arg) if isinstance(arg,
                (dict, list, str, int, bool)) else None for index, arg in
                enumerate(self.args) if self.argspec.args and type(self.argspec.args is list)}

        data.update({str(k): str(v) if isinstance(v, (dict, list, str, int, bool))
                    else None for k, v in self.kwargs.items() if self.kwargs})

        return data

    def fastapiArgs(self):
        '''Returns Args and Kwargs of function as `dict`'''

        data = {str(self.argspec.args[index]): str(arg) if isinstance(arg,
                (dict, list, str, int, bool)) else str(arg.url) if isinstance(
                    arg, Request) else None for index, arg in enumerate(self.args)
                if self.argspec.args and type(self.argspec.args is list)}

        data.update({str(k): str(v) if isinstance(v, (dict, list, str, int, bool))
                     else str(v.url) if isinstance(v, Request) else None
                     for k, v in self.kwargs.items() if self.kwargs})

        return data


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
