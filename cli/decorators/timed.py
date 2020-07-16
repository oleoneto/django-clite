# cli:decorators:timed
import time
from functools import wraps


def timed(f):
    """
    Based on code by Martin Heinz
    https://gist.github.com/MartinHeinz/2e2d258b2e6b77280dab04aad9707a7a
    """

    @wraps(f)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()

        value = f(*args, **kwargs)

        end_time = time.perf_counter()

        print('{0:<10}.{1:<8} : {2:<8}'.format(f.__module__, f.__name__, end_time - start_time))

        return value
    return wrapper
