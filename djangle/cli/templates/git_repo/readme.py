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
[Requirements](requirements_template.txt)

----

#### Virtual environment + install requirements_template
```
source venv/bin/activate && pip install -r requirements_template.txt
```

----
### Auth User Model
**IMPORTANT:** authentication is overridden in favor of `core.User`. This setting is present in [settings.py]({{ project }}/settings.py) as `AUTH_USER_MODEL`.
When running migrations for the project for the first time, remember to follow the following workflow:
```
./manage.py makemigrations core && \
./manage.py migrate core && \
./manage.py makemigrations && \
./manage.py migrate
```

This ensures the default authentication user is set to `core.User`, as defined in `AUTH_USER_MODEL`. 
It is important to follow the order above because of how django sets up the database.


### Create superuser
```
./manage.py createsuperuser
```

----

### Environment variables
For safety and privacy reasons, use environment variables instead of hard-coding some values:
```
DEBUG = os.environ.get("DEBUG") == "True"
SECRET_KEY = os.environ.get("SECRET_KEY", "Replace SECRET_KEY with environment variable")
```

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
