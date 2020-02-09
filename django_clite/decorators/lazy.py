# Lazy decorator
# source: http://theorangeduck.com/page/lazy-python
from functools import wraps


def lazy(func):

    @wraps(func)
    def wrapped_lazy_func(*args, **kwargs):
        wrapped = lambda x: func(*args, **kwargs)
        wrapped.__name__ = "lazy-" + func.__name__
        return wrapped

    return wrapped_lazy_func
