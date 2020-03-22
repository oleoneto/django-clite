from setuptools import find_packages, setup


with open("README.md", "r") as f:
    long_description = f.read()


setup(
    name="django-clite",
    version="0.2.11",
    author="Leo Neto",
    author_email="leo@ekletik.com",
    url="https://bitbucket.org/oleoneto/django-clite",
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
        'click-repl==0.1.6',
        'jinja2',
        'inflection',
        'django>=2.2.4',
        'tox',
        'pytest==5.3.0',
        'faker',
        'inquirer',
    ],
    zip_safe=False,
    include_package_data=True,
    packages=find_packages(),
    project_urls={
        "Documentation": "https://bitbucket.org/oleoneto/django-clite/",
        "Source Code": "https://bitbucket.org/oleoneto/django-clite/",
    },
    entry_points={
        'console_scripts': [
            'D=app:main',
            'djc=app:main',
            'django-clite=app:main',
        ]
    },
    scripts=['app.py']
)
