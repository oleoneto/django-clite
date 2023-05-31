# cli:decorators:logger
import functools
import re
from types import FunctionType, MethodType
from typing import Callable

from cli.core.logger import Logger
from cli.utils import modify_and_import, get_source


def _log(msg: str, *args, **kwargs):
    comment = re.match(
        r"^# ((?P<literal>f\".*\")|(?P<raw>(.*)))\W+(?P<tag># logger$)", msg.strip()
    )

    if comment is not None:
        raw, literal, logger_tag = comment["raw"], comment["literal"], comment["tag"]

        if logger_tag is None:
            return

        if raw:
            Logger().print(raw)
        elif literal:
            try:
                Logger().print(eval(literal))
            except Exception as err:
                print(repr(err))
                pass


def _replace(line: str) -> str:
    return re.sub(
        r"^# ((?P<literal>f\".*\")|(?P<raw>(.*)))\W+(?P<tag># logger$)",
        "Logger().print(__file__)",
        line,
    )


def log_me(fn: Callable):
    """
    Valid logger comments:

    1. "This is a comment" # logger
    2. f"This is a comment with a variable {var}" # logger

    NOTE: variables defined within the function scope
    """

    import inspect
    import ast

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        value = fn(*args, **kwargs)
        raw_source, _ = inspect.getsourcelines(fn)
        [_log(line, *args, **kwargs) for line in raw_source]

        return value

    return wrapper
