import functools


def count_calls(f):
    @functools.wraps(f)
    def wrapper_count_calls(*args, **kwargs):
        wrapper_count_calls.num_calls += 1
        print(f"Call {wrapper_count_calls.num_calls} of {f.__name__!r}")
        return f(*args, **kwargs)
    wrapper_count_calls.num_calls = 0
    return wrapper_count_calls
