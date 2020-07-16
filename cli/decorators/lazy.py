# Lazy decorator
# source: http://theorangeduck.com/page/lazy-python
from functools import wraps


def lazy(f):
    @wraps(f)
    def wrapped_lazy_func(*args, **kwargs):
        wrapped = lambda x: f(*args, **kwargs)
        wrapped.__name__ = "lazy-" + f.__name__
        return wrapped

    return wrapped_lazy_func
