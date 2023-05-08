# cli:core:filesystem
from pathlib import Path


class File:
    def __init__(self, path: str, template: str, content: bytes, context: dict):
        self._path = path
        self._template = template
        self._content = content

        print(f"{self.path} -> {template}")

    @property
    def template(self) -> str:
        return self._template

    @property
    def path(self) -> str:
        return self._path

    @property
    def name(self) -> str:
        return Path(self._path).name

    @property
    def content(self) -> bytes:
        return self._content
