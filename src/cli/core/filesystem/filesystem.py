# cli:core:filesystem
import os
from os import PathLike
from contextlib import contextmanager


@contextmanager
def working_directory(directory: PathLike | str):
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
