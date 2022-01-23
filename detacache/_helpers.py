
import hashlib
import datetime
import logging
import sys


logger = logging.getLogger('detacache')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stderr)
handler.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(levelname)s:%(module)s:%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


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



