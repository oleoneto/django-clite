# cli:core:filesystem
import io
import os
from typing import IO

from cli.core.filesystem.protocols import (
    ReaderProcotol,
    WriterProtocol,
    WriteCommandResult,
)
from cli.decorators.singleton import singleton
from cli.core.logger import Logger


@singleton
class SystemOS(ReaderProcotol, WriterProtocol):
    @classmethod
    def close(cls, *args, **kwargs):
        return os.close(*args, **kwargs)

    @classmethod
    def open(cls, *args, **kwargs) -> io.TextIOWrapper:
        return open(*args, **kwargs)

    @classmethod
    def getcwd(cls) -> str:
        return os.getcwd()

    @classmethod
    def mkdir(cls, *args, **kwargs):
        return os.mkdir(*args, **kwargs)

    @classmethod
    def write(cls, *args, **kwargs):
        return os.write(*args, **kwargs)

    @classmethod
    def remove(cls, *args, **kwargs):
        return os.remove(*args, **kwargs)

    def __repr__(self):
        return "system_os"


@singleton
class NullOS(ReaderProcotol, WriterProtocol):
    @classmethod
    def close(cls, *args, **kwargs):
        return None

    @classmethod
    def open(cls, *args, **kwargs) -> io.TextIOWrapper:
        class NullOSFileContext(io.TextIOWrapper):
            def __enter__(self):
                return self.buffer

        return NullOSFileContext(buffer=IO())

    @classmethod
    def getcwd(cls):
        return ""

    @classmethod
    def mkdir(cls, *args, **kwargs):
        return None

    @classmethod
    def write(cls, *args, **kwargs):
        return 0

    @classmethod
    def remove(cls, *args, **kwargs):
        return None

    def __repr__(self):
        return "null_os"
