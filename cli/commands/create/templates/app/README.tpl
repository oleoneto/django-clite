# {{ package_name }}

{{ package_description }}

![PyPI - License](https://img.shields.io/pypi/l/{{ package_name }})
![PyPI - Version](https://img.shields.io/pypi/v/{{ package_name }})
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/{{ package_name }})
![PyPI - Downloads](https://img.shields.io/pypi/dm/{{ package_name }})

#### Dependencies
Use of **{{ package_name }}** requires:
-

Those apps will need to be installed in the ``INSTALLED_APPS`` tuple of your django project.


#### Models
The app is split into the following models:
-

#### Installation
1. Add **{{ package_name }}** to your `INSTALLED_APPS` setting like this::
```python
    INSTALLED_APPS = [
        # other apps...
        '{{ package_name }}',
    ]
```

Alternatively, you can also add this app like so::
```python
    INSTALLED_APPS = [
        # other apps...
        '{{ package_name }}.apps.{{ package_classname }}Config',
    ]
```

2. Include the polls URLconf in your project urls.py like this::
```python
    path('{{ package_namespace }}/', include('{{ package_name }}.urls', namespace='{{ package_name }}')),
```

2.1. Optionally, you can also add the api endpoints in your project urls.py like so::
```python
    path('api/', include('{{ package_name }}.api', namespace='{{ package_name }}_api')),
```

3. Run ``python manage.py migrate`` to create the app models.

4. Start the development server and visit [`http://127.0.0.1:8000/admin/`](http://127.0.0.1:8000/admin/)
   to start a add chat groups and messages (you'll need the Admin app enabled).

5. Visit [`http://127.0.0.1:8000/{{ package_namespace }}/`](http://127.0.0.1:8000/{{ package_namespace }}/) to use the app.
You should have the following urls added to your url schemes:
```
    http://127.0.0.1:8000/{{ package_namespace }}/
    # list missing urls here...
```

5.1. If you've included the api urls as well, you can visit the endpoints by visiting::
```
    http://127.0.0.1:8000/api/{{ package_namespace }}
    # list missing urls here...
```

## License
**{{ package_name }}** is [{{ package_license }}-licensed](LICENSE.md).

------

Built with [django-clite](https://github.com/oleoneto/django-clite).
