import inspect
import hashlib
from datetime import datetime


def getDecoratorArgs(func, args, kwargs):
    '''Returns Args of function as `dict`'''
    argspec = inspect.getfullargspec(func)
    data = dict()
    if argspec.args and type(argspec.args is list):
        for index,arg in enumerate(args) :
            data.update({str(argspec.args[index]):str(arg)})
    if kwargs:
        for k, v in kwargs.items():
            data.update({str(k):str(v)})
    return data


def createIntHashKey(string:str):
    '''Returns a md5 Hash of string as `int`'''
    return int(hashlib.md5(str(string).encode()).hexdigest(),16)

def createStringHashKey(string:str):
    '''Returns a md5 Hash of string as `string`'''
    return hashlib.md5(str(string).encode()).hexdigest()


def getCurrentTimestamp():
    '''Returns Current Timestamp as `int`'''
    return int(round(datetime.now().timestamp()))


def checkExpiredTimestamp(expire:int,initialTimestamp:int,currentTimestamp:int):
    '''Returns `True` if expired else `False`'''
    return initialTimestamp + expire < currentTimestamp

