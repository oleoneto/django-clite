from jinja2 import Template


readme_template = Template("""# {{ project }}
{% if author %}Author: {{ author }} {% endif %}

#### CLI Documentation
```
Instructions: https://github.com/oleoneto/Django-CLI/README.md
Issues: https://github.com/oleoneto/Django-CLI/issues
```

----

#### Requirements
[Requirements](requirements.txt)

----

#### Pipenv and dependencies
```
pipenv sync
```

----
### Auth User Model
**IMPORTANT:** authentication is overridden in favor of `core.User`. This setting is present in [settings.py]({{ project }}/settings.py) as `AUTH_USER_MODEL`.
When running migrations for the project for the first time, remember to follow the following workflow:
```
./manage.py makemigrations authentication && \
./manage.py migrate authentication && \
./manage.py makemigrations && \
./manage.py migrate
```

This ensures the default authentication user is set to `authentication.User`, as defined in `AUTH_USER_MODEL`. 
It is important to follow the order above because of how django sets up the database.


### Create superuser
```
./manage.py createsuperuser
```

----

### Environment variables
For safety reasons, prefer to use environment variables instead of hard-coding sensitive values. One option is to use 
`django-environ`, another is to use an environment file `.env`. Here's an [example environment file](.env.example).

----

### To Do
[All open and closed issues found here](/issues)

----

### Pull requests
[Contributions can be pushed here](/pulls)

----

### LICENSE
**{{ project }}**. [Check out the license](LICENSE).

""")
