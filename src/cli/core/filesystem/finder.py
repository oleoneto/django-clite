# cli:core:filesystem
import os
from pathlib import Path

from cli.core.filesystem.protocols import FinderProtocol


class Finder(FinderProtocol):
    @classmethod
    def find(cls, path: Path, patterns: list[str]) -> dict:
        files = [fp for fp in path.iterdir() if any(fp.match(p) for p in patterns)]

        matches = dict()
        for match in files:
            matches[match.name] = match.absolute()
        return matches


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
