# {{ project }}
{% if author %}Author: {{ author }} {% endif %}

#### Requirements
[Requirements](Pipfile)

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
For safety reasons, prefer to use environment variables instead of hard-coding sensitive values.
This project has two environment files [`.env`](.env) and [`.env-example`](.env-example) which you can use to
manage your application configuration and secrets.

Your actual secrets should live in `.env`. This file should not be committed to your repository, but should be added to 
[`.gitignore`](.gitignore).
Use `.env-example` to specify the keys that must be set in order for your application to run once deployed.


---

### To Do
[Check out our open issues](/issues)

---

### Pull requests
Found a bug or have a feature request? [Contribute](/pulls)

---

### LICENSE
**{{ project }}**. [Check out the license](LICENSE).

----

Project generated with [django-clite](https://github.com/oleoneto/django-clite)
