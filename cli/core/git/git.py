import subprocess

from .protocols import Git


class GitHandler(Git):
    def initialize(self) -> bool:
        success = False

        try:
            subprocess.check_output(["git", "init"])
            subprocess.check_output(["git", "add", "--all"])
            subprocess.check_output(["git", "commit", "-m", "feat: initial commit"])
            success = True
        except subprocess.CalledProcessError as error:
            pass

        return success

    def add_origin(self, origin: str) -> bool:
        success = False

        try:
            subprocess.check_output(["git", "remote", "add", "origin", origin])
            success = True
        except subprocess.CalledProcessError:
            pass

        return success
