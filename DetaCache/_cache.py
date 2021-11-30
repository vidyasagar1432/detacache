from functools import wraps


def detaCache(urlArg:str,dbCache = None):
    def wrapped(function):
        @wraps(function)
        async def wrappedFunction(*args, **kwargs):
            if not dbCache:
                print('Deta base not found!')
                return await function(*args, **kwargs)
            url = kwargs.get(urlArg)
            data = dbCache.get(key=url)
            if not data:
                _data = await function(*args, **kwargs)
                dbCache.put(data={'value':_data},key=url)
                return _data
            return data['value']
        return wrappedFunction
    return wrapped

