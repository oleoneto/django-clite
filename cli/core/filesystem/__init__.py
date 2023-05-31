# cli:core:filesystem
from .protocols import (
    ReaderProcotol,
    WriterProtocol,
    FileHandlerProtocol,
    FinderProtocol,
    SystemProtocol,
)
from .directories import Directory
from .files import File
from .finder import Finder
from .system import NullOS, SystemOS
from .filesystem import FileSystem
