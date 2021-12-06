import inspect

def inspectDecorator(func, args, kwargs):
    argspec = inspect.getfullargspec(func)
    data = dict()
    if argspec.args and type(argspec.args is list):
        for index,arg in enumerate(args) :
            data.update({str(argspec.args[index]):str(arg)})
    if kwargs:
        for k, v in kwargs.items():
            data.update({str(k):str(v)})
    return data
