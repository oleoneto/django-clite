import subprocess

from .protocols import Git
from cli.decorators.singleton import singleton
# from cli.core.logger import logger


@singleton
class GitHandler(Git):
    def initialize(self) -> bool:
        try:
            subprocess.check_output(["git", "init"])
            subprocess.check_output(["git", "add", "--all"])
            subprocess.check_output(["git", "commit", "-m", "feat: initial commit"])
            return True
        except subprocess.CalledProcessError as _:
            pass

        return False

    def add_origin(self, origin: str) -> bool:
        try:
            subprocess.check_output(["git", "remote", "add", "origin", origin])
            return True
        except subprocess.CalledProcessError:
            pass

        return False
