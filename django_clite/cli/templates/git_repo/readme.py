from jinja2 import Template


readme_template = Template("""# {{ project }}
{% if author %}Author: {{ author }} {% endif %}

#### Requirements
[Requirements](requirements.txt)

----

#### Pipenv and dependencies
Run `pipenv install --deploy` to install all dependencies listed in the Pipfile.

{% if custom_auth %}
----
### Authentication with custom AUTH_USER_MODEL
Authentication is overridden in favor of [`authentication.User`]({{ project }}/authentication/models/user.py). 
If you haven't already, add the following line to your project's [settings.py]({{ project }}/settings.py):
```python
AUTH_USER_MODEL = 'authentication.User'
```

When running migrations for your project for the first time, remember to follow the following workflow:
```
python manage.py makemigrations authentication && \
python manage.py migrate authentication && \
python manage.py migrate
```

This ensures the AUTH_USER_MODEL is set to `authentication.User`. 
It is important to follow the order above because of how django sets up the database.
{% endif %}

### Create superuser
```
python manage.py createsuperuser
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

Project generated with [django-clite](https://bitbucket.org/oleoneto/django-clite)
""")
