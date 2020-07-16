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
        'Framework :: Django :: 3.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    license="BSD",
    install_requires=[
        'Click==7.0',
        'django>=2.2.4',
        'faker>=4.1.0',
        'jinja2>=2.11.2',
        'inquirer>=2.6.3',
        'inflection>=0.4.0',
    ],
    extra_require={
        'click-repl==0.1.6',
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
            'D=cli.app:cli',
            'django-clite=cli.app:cli',
        ]
    },
    scripts=['cli/app.py']
)
