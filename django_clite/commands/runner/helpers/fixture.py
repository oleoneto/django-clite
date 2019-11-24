import os
from .runner import RunnerHelper


DEFAULT_LOAD_FIXTURES_COMMAND = ['python3', 'manage.py', 'loaddata']


class FixtureHelper(RunnerHelper):
  
    @classmethod
    def load_one(cls, path, fixture):
        os.chdir(path)

    @classmethod
    def load_all(cls, path):
        os.chdir(path)

    def run(self, **kwargs):
        pass
