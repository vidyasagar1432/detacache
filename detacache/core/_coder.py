
import json
import pickle
from typing import Any
from fastapi.encoders import jsonable_encoder

from ._constants import JSON_CONVERTERS,FASTAPI_CONVERTERS


class Coder:
    @classmethod
    def encode(cls, value: Any):
        raise NotImplementedError

    @classmethod
    def decode(cls, value: Any):
        raise NotImplementedError


class JsonCoder(Coder):
    @classmethod
    def encode(cls, value: Any):
        return json.dumps(value)

    @classmethod
    def decode(cls, value: Any):
        return json.loads(value)


class PickleCoder(Coder):
    @classmethod
    def encode(cls, value: Any):
        return pickle.dumps(value)

    @classmethod
    def decode(cls, value: Any):
        return pickle.loads(value)


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


class FastAPICoder(Coder):
    @classmethod
    def encode(cls, value: Any):
        return jsonable_encoder(value)

    @classmethod
    def decode(cls, value: Any):
        return objDecode(value,FASTAPI_CONVERTERS)


