from setuptools import find_packages, setup

setup(
    name="Django CLI",
    version="0.0.alpha1",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'djangocli': ['*.json'],
    },
    install_requires=[
        'Click',
        'django>=2.1'
    ],
    author="Leo Neto",
    author_email="oleoneto@gmail.com",
    description="CLI for managing Django projects",
    license="MIT",
    keywords="django automate",
    url="https://github.com/oleoneto/Django-CLI",
    project_urls={
        "Documentation": "https://github.com/oleoneto/Django-CLI/",
        "Source Code": "https://github.com/oleoneto/Django-CLI/",
    },
    entry_points='''
        [console_scripts]
        djangocli=app:main
    '''
)
