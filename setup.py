from setuptools import find_packages, setup


with open("README.md", "r") as f:
    long_description = f.read()


setup(
    name="djangle-cli",
    version="0.0.2",
    author="Leo Neto",
    author_email="leo@ekletik.com",
    url="https://github.com/oleoneto/djangle",
    description="CLI for managing Django projects",
    long_description=long_description,
    long_description_content_type='text/markdown',
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
        "Documentation": "https://github.com/oleoneto/djangle/",
        "Source Code": "https://github.com/oleoneto/djangle/",
    },
    entry_points={
        'console_scripts': [
            'D=app:main',
            'djangle=app:main',
            'djangle-cli=app:main'
        ]
    },
    scripts=['app.py']
)
