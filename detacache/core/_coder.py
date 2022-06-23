
from typing import Any

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


class Coder:
    @classmethod
    def encode(cls, value: Any):
        raise NotImplementedError

    @classmethod
    def decode(cls, value: Any):
        raise NotImplementedError


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



