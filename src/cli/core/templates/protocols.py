# cli:core:templates
from typing import Protocol


class TemplateParserProtocol(Protocol):
    def parse_file(self, filepath: str, variables: dict) -> str:
        ...

    def parse_string(self, content: str, variables: dict) -> str:
        ...
