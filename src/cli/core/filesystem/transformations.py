# cli:core:filesystem:transformations
from pathlib import Path


class FileTransformation:
    def __init__(self, file: str):
        self.file = file

    def run(self):
        raise NotImplementedError


class MoveFile(FileTransformation):
    def __init__(self, file: str, target: str):
        super().__init__(file)
        self.target = target

    def run(self):
        from_ = Path(self.file)
        to_ = Path(self.target)
        from_.rename(to_)


class DeleteFile(FileTransformation):
    def __init__(self, file: str):
        super().__init__(file)

    def run(self):
        file = Path(self.file)
        file.unlink(missing_ok=True)
