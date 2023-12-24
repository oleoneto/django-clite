# cli:core:filesystem
import os
from contextlib import contextmanager


@contextmanager
def working_directory(directory):
    # Based on: https://stackoverflow.com/a/53993508/7899348

    cwd = os.getcwd()

    try:
        os.chdir(directory)
        yield directory
    except FileNotFoundError as _:
        yield
    except TypeError as _:
        yield
    finally:
        os.chdir(cwd)
