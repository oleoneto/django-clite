from setuptools import find_packages, setup
import os

setup(
    name="Django CLI",
    version="0.0a4",
    author="Leo Neto",
    author_email="leo@ekletik.com",
    url="https://github.com/oleoneto/django-cli",
    description="CLI for managing Django projects",
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
    license="BSD",
    install_requires=[
        'Click==7.0',
        'jinja2',
        'inflect==2.1.0',
        'django>=2.2.1'
    ],
    zip_safe=False,
    include_package_data=True,
    packages=find_packages(),
    project_urls={
        "Documentation": "https://github.com/oleoneto/django-cli/",
        "Source Code": "https://github.com/oleoneto/django-cli/",
    },
    entry_points={
        'console_scripts': [
            'D=app:main',
            'django-cli=app:main',
            'djungle=app:main'
        ]
    }
)
