import os
import subprocess


DEFAULT_LOAD_FIXTURES_COMMAND = ['python3', 'manage.py', 'loaddata']


class FixtureHelper(object):
  
  @classmethod
  def load_one(cls, path, fixture):
    os.chdir(path)

  @classmethod
  def load_all(cls, path):
    os.chdir(path)
