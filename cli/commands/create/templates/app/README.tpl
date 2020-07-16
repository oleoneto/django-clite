# {{ app }}

{{ package_description }}

![PyPI - License](https://img.shields.io/pypi/l/{{ app }})
![PyPI - Version](https://img.shields.io/pypi/v/{{ app }})
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/{{ app }})
![PyPI - Downloads](https://img.shields.io/pypi/dm/{{ app }})

#### Dependencies
Use of **{{ app }}** requires:
-

Those apps will need to be installed in the ``INSTALLED_APPS`` tuple of your django project.


#### Models
The app is split into the following models:
-

#### Installation
1. Add **{{ app }}** to your `INSTALLED_APPS` setting like this::
```python
    INSTALLED_APPS = [
        # other apps...
        '{{ app }}',
    ]
```

Alternatively, you can also add this app like so::
```python
    INSTALLED_APPS = [
        # other apps...
        '{{ app }}.apps.{{ app_classname }}Config',
    ]
```

2. Include the polls URLconf in your project urls.py like this::
```python
    path('{{ app_namespace }}/', include('{{ app }}.urls', namespace='{{ app }}')),
```

2.1. Optionally, you can also add the api endpoints in your project urls.py like so::
```python
    path('api/', include('{{ app }}.api', namespace='{{ app }}_api')),
```

3. Run ``python manage.py migrate`` to create the app models.

4. Start the development server and visit [`http://127.0.0.1:8000/admin/`](http://127.0.0.1:8000/admin/)
   to start a add chat groups and messages (you'll need the Admin app enabled).

5. Visit [`http://127.0.0.1:8000/{{ app_namespace }}/`](http://127.0.0.1:8000/{{ app_namespace }}/) to use the app.
You should have the following urls added to your url schemes:
```
    http://127.0.0.1:8000/{{ app_namespace }}/
    # list missing urls here...
```

5.1. If you've included the api urls as well, you can visit the endpoints by visiting::
```
    http://127.0.0.1:8000/api/{{ app_namespace }}
    # list missing urls here...
```

## License
**{{ app }}** is [{{ license }}-licensed](LICENSE.md).

------

Built with [django-clite](https://github.com/oleoneto/django-clite).
