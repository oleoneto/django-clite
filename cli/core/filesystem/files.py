# cli:core:filesystem
from pathlib import Path


class File:
    def __init__(self, path: str, template: str, context={}, content=""):
        self._path = path
        self._template = template
        self._content = content
        self.context = context

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
    def content(self) -> str:
        return self._content
