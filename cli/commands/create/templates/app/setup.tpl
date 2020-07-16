from setuptools import setup
import os
import re


def read(f):
    return open(f, 'r', encoding='utf-8').read()


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


version = get_version('{{ app }}')

setup(
    name='{{ app }}',
    url='{{ url }}',
    author='{{ author }}',
    author_email='{{ email }}',
    description='{{ description }}',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
)
