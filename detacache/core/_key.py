
import inspect
import typing

from ._helpers import createStringHashKey

class KeyGenerator:
    
    @classmethod
    def generate(cls, function:typing.Callable, args: tuple, kwargs: dict) -> str:
        raise NotImplementedError



class DetaKey(KeyGenerator):
    @classmethod
    def generate(cls,function:typing.Callable, args: tuple, kwargs: dict):
        '''Returns a deta cache key'''

        argspec = inspect.getfullargspec(function)

        data = {str(argspec.args[index]): str(arg) if isinstance(arg,
                (dict, list, tuple, set, str, int, bool)) else None for index, arg in enumerate(args)
                if argspec.args and type(argspec.args is list)}

        data.update({str(k): str(v) if isinstance(v, (dict, list, tuple, set, str, int, bool))
                    else None for k, v in kwargs.items() if kwargs})

        return createStringHashKey(f'{function.__name__}{data}')

try:
    import fastapi
    from fastapi.requests import Request
except ImportError: 
    fastapi = None 

class FastAPIKey(KeyGenerator):

    @classmethod
    def generate(cls,function:typing.Callable, args: tuple, kwargs: dict,):
        '''Returns a deta cache key'''

        assert fastapi is not None, "fastapi must be installed to use FastAPIKey"

        request = kwargs.get('request')

        assert request, f"function {function.__name__} needs a `request` argument"

        if not isinstance(request, Request):
            raise Exception("`request` must be an instance of `fastapi.request.Request`")

        return createStringHashKey(f'{function.__name__}{request.url}')

try:
    import starlette
    from starlette.requests import Request
except ImportError: 
    starlette = None 


class StarletteKey(KeyGenerator):

    @classmethod
    def generate(cls,function:typing.Callable, args: tuple, kwargs: dict,):
        '''Returns a deta cache key'''

        assert starlette is not None, "starlette must be installed to use StarletteKey"

        request  =None
        
        for i in args:
            if isinstance(i, Request):
                request = i
                break

        assert request, f"function {function.__name__} needs a `request` argument"

        if not isinstance(request, Request):
            raise Exception("`request` must be an instance of `starlette.request.Request`")

        return createStringHashKey(f'{function.__name__}{request.url}')