from setuptools import find_packages, setup


with open("README.md", "r") as f:
    long_description = f.read()


setup(
    name="django-dj",
    version="0.0.9-beta.1",
    author="Leo Neto",
    author_email="leo@ekletik.com",
    url="https://bitbucket.org/oleoneto/django-dj",
    description="CLI for managing Django projects",
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords="django automate cli command line tools rails ember python framework",
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
        'inflection',
        'django>=2.2.1',
        'tox'
    ],
    zip_safe=False,
    include_package_data=True,
    packages=find_packages(),
    project_urls={
        "Documentation": "https://bitbucket.org/oleoneto/django-dj/",
        "Source Code": "https://bitbucket.org/oleoneto/django-dj/",
    },
    entry_points={
        'console_scripts': [
            'D=app:main',
            'dj=app:main',
            'django-dj=app:main',
        ]
    },
    scripts=['app.py']
)
