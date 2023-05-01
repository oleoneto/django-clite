import re
import os
from setuptools import find_packages, setup


with open("README.md", "r") as f:
    long_description = f.read()


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


version = get_version('cli')

setup(
    name="django-clite",
    version=version,
    author="Leo Neto",
    author_email="leo@ekletik.com",
    url="https://github.com/oleoneto/django-clite",
    description="CLI for managing Django projects",
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords="django automate cli command line tools rails ember python framework",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django :: 4.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    license="BSD 3-Clause",
    install_requires=[
        'Click>=8.1',
        'django>=4.2',
        'jinja2>=3.1',
        'inquirer>=3.1.3',
        'inflection>=0.5.1',
        'rich>=13.3',
    ],
    extra_require={
        'click-repl==0.2',
        'pytest',
    },
    zip_safe=False,
    include_package_data=True,
    packages=find_packages(),
    project_urls={
        "Documentation": "https://github.com/oleoneto/django-clite/",
        "Source Code": "https://github.com/oleoneto/django-clite/",
    },
    entry_points={
        'cli.commands': '',
        'console_scripts': [
            'django-clite=cli.app:cli',
        ]
    },
    scripts=['cli/app.py']
)
