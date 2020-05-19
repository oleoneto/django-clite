=============
{{ app }}
=============

`{{ app }}` is a django app.

Quick start
-----------

1. Add "{{ app }}" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        '{{ app }}',
    ]

2. Include the polls URLconf in your project urls.py like this::

    path('{{ app }}/', include('{{ app }}.urls')),

3. Run ``python manage.py migrate`` to create the app models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to start a new chat (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/{{ app }}/ to use the app.