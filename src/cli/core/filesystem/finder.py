# cli:core:filesystem
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
