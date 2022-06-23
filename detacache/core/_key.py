
import inspect

from ._helpers import createStringHashKey

def detaKeyGen(function:object, args: tuple, kwargs: dict):
    '''Returns a deta cache key'''

    argspec = inspect.getfullargspec(function)

    data = {str(argspec.args[index]): str(arg) if isinstance(arg,
            (dict, list, tuple, set, str, int, bool)) else None for index, arg in enumerate(args)
            if argspec.args and type(argspec.args is list)}

    data.update({str(k): str(v) if isinstance(v, (dict, list, tuple, set, str, int, bool))
                else None for k, v in kwargs.items() if kwargs})
    
    return createStringHashKey(f'{function.__name__}{data}')


