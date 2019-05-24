from setuptools import find_packages, setup
import os


# Based upon Django's own setup.py
def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()


setup(
    name="Django CLI",
    version="0.0.alpha2",
    author="Leo Neto",
    author_email="leo@ekletik.com",
    url="https://github.com/oleoneto/Django-CLI",
    description="CLI for managing Django projects",
    long_description=read('README.md'),
    keywords="django automate cli command line tools rails ember python framework devops",
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=[
        'Click',
        'django>=2.2.1'
    ],
    zip_safe=False,
    include_package_data=True,
    packages=find_packages(),
    package_data={
        'djangocli': ['*.json'],
    },
    project_urls={
        "Documentation": "https://github.com/oleoneto/Django-CLI/",
        "Source Code": "https://github.com/oleoneto/Django-CLI/",
    },
    entry_points={
        'console_scripts': [
            'djangocli = djangocli.app:main',
        ]
    },
    scripts=['djangocli/app.py']
)
