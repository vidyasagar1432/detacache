
import inspect
from starlette.requests import Request

from .._helpers import createStringHashKey


class BaseKeyGen:
    @classmethod
    def get(cls, function, args: tuple, kwargs: dict) -> str:
        raise NotImplementedError


class JsonKeyGen(BaseKeyGen):
    @classmethod
    def get(cls,function, args: tuple, kwargs: dict):
        '''Returns a deta cache key'''

        argspec = inspect.getfullargspec(function)

        data = {str(argspec.args[index]): str(arg) if isinstance(arg,
                (dict, list, tuple, set, str, int, bool)) else None for index, arg in enumerate(args)
                if argspec.args and type(argspec.args is list)}

        data.update({str(k): str(v) if isinstance(v, (dict, list, tuple, set, str, int, bool))
                    else None for k, v in kwargs.items() if kwargs})
        
        return createStringHashKey(f'{function.__name__}{data}')

class FastAPIKeyGen(BaseKeyGen):
    @classmethod
    def get(cls,function, args: tuple, kwargs: dict,):
        '''Returns a deta cache key'''

        request = kwargs.get('request')

        assert request, f"function {function.__name__} needs a `request` argument"

        if not isinstance(request, Request):
            raise Exception(
                "`request` must be an instance of `starlette.request.Request`")

        return createStringHashKey(f'{function.__name__}{request.url}')
