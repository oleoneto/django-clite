import re
import os
import inflection
from pathlib import Path
import importlib, sys
from typing import Callable

# from cli.core.filesystem.directories import Directory
from cli.core.filesystem.finder import Finder
from cli.core.fieldparser.factory import make_field


def check_noun_inflection(noun, force_singular=None, force_plural=None):
    """
    Checks whether a noun is plural or singular and gives
    the option to change the noun from plural to singular.
    """

    noun = noun.lower()
    singular = inflection.singularize(noun)
    plural = inflection.pluralize(noun)

    if force_plural == force_singular:
        return noun
    elif force_singular:
        return singular
    elif force_plural:
        return plural

    return noun


def sanitized_string(text):
    """
    Ensures strings are properly sanitized
    and no special characters are present.
    """

    r = inflection.transliterate(text.strip())
    r = re.sub(r"[\:\.\,\;\\\/\?\!\&\$\#\@\)\(\+\=\'\"\-\|\s]+", "_", r)
    return inflection.underscore(r).lower()


def core_project_files() -> dict:
    return Finder().find(
        path=Path(os.getcwd()),
        patterns=[
            "apps.py",
            "asgi.py",
            "manage.py",
            "wsgi.py",
        ],
    )


def project_and_app_names(django_files: dict) -> tuple[str, str]:
    for k, v in django_files.items():
        if k == "apps.py":
            return v.parent.parent.name, v.parent.name
        elif k in ["asgi.py", "manage.py", "wsgi.py"]:
            return v.parent.name, ""
    return "", ""


def modify_and_import(module_name, package, modification_func):
    spec = importlib.util.find_spec(module_name, package)
    source = spec.loader.get_source(module_name)

    new_source = modification_func(source)
    module = importlib.util.module_from_spec(spec)

    codeobj = compile(new_source, module.__spec__.origin, "exec")
    exec(codeobj, module.__dict__)

    sys.modules[module_name] = module
    return module


def get_source(fn: Callable, transformer: Callable, drop_decorators: bool = True):
    import sys
    import itertools
    import inspect

    _s = inspect.getsource(fn)

    if _s is None:
        return ""

    # Remove tabs to make local functions global
    lines = _s.expandtabs().splitlines()
    stripped = lines[0].lstrip()
    indent = sys.maxsize
    if stripped:
        indent = min(indent, len(lines[0]) - len(stripped))

    for pos in range(len(lines)):
        stripped = lines[pos].lstrip()

        if drop_decorators and stripped.startswith("@"):
            lines[pos] = ""
            continue

        current_indent = max(0, len(lines[pos]) - len(stripped) - indent)
        lines[pos] = " " * current_indent + transformer(stripped)

    return "\n".join(lines)


# ===========================
# Callbacks
# ===========================


def sanitized_string_callback(ctx, param, value):
    return sanitized_string(value)


def fields_callback(ctx, param, value):
    model_fields = []
    model_relationships = []

    model = ctx.params.get("name")

    for pair in value:
        # Ignore malformed field pairs
        if pair.find(":") == -1:
            continue

        kind, name = pair.split(":")

        f = make_field(kind=kind, name=name, model=model)
        if f.kind is not None:
            model_fields.append(f)

            if f.is_relationship:
                model_relationships.append(f)

    return model_fields, model_relationships
