import inspect
import hashlib
from datetime import datetime


def getDecoratorArgs(func, args, kwargs):
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
    return int(hashlib.md5(str(string).encode()).hexdigest(),16)

def createStringHashKey(string:str):
    return hashlib.md5(str(string).encode()).hexdigest()


def getCurrentTimestamp():
    return int(round(datetime.now().timestamp()))


def checkExpiredTimestamp(expire:int,initialTimestamp:int,currentTimestamp:int):
    return initialTimestamp + expire < currentTimestamp

