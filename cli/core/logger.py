import rich
from rich.console import Console

from cli.decorators.singleton import singleton


@singleton
class Logger:
    def __init__(self, dry: bool = True, verbose: bool = False):
        self.dry = dry
        self.verbose = verbose
        self.console = Console()

        super().__init__()

    def print(self, msg: str):
        if not self.verbose:
            return

        _msg = ""
        if self.dry:
            _msg = "[bold][DRY][/bold] " + msg

        rich.print(_msg)
