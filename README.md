# django-clite

A CLI tool that handles creating and managing Django projects

![PyPI - License](https://img.shields.io/pypi/l/django-clite?style=flat-square)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-clite?style=flat-square)
![PyPI](https://img.shields.io/pypi/v/django-clite?style=flat-square)
![Bitbucket Pipelines](https://img.shields.io/bitbucket/pipelines/oleoneto/django-clite/development?style=flat-square)
![PyPI - Downloads](https://img.shields.io/pypi/dm/django-clite?style=flat-square)

### Requirements
[Requirements](requirements.txt)


### Installation
Install via [pip](http://www.pip-installer.org/):
```bash
pip install django-clite
```

Install from source:
```
git clone https://bitbucket.org/oleoneto/django-clite.git
cd django-clite
pip install .
```

After installation, the CLI will expose the binary with two names, any of which can be used in place of another:
```
D
django-clite
```


----

### Commands
```
destroy   Deletes models, serializers, and other resources
generate  Adds models, routes, and other resources
new       Creates projects and apps
run       Run maintenance, development, and deployment scripts.
```

#### New
The `new` command (abbreviated `n`) can be used to start new projects as well as new applications. The command tries to simplify how a project is created as well as the applications contained in it. Here's an example of such simplification:

Suppose you want to start a new project and want to create two apps within it:
```
django-admin startproject mywebsite
cd mywebsite/mywebsite/
django-admin startapp blog
django-admin startapp radio
```

The equivalent command in the `django-clite` is:
```bash
D new project mywebsite blog radio
```

Specifying `apps` when creating a project is optional, but you're likely to need to create one inside of your project directory, so the CLI can handle the creation of all of your apps if you pass them as arguments after your project name.

##### Creating new projects
To create a new project, simply run `D new project project_name`. This command supports the following flags:

**Flags:**

```
--docker       Add support for Docker
--dokku        Add support for Dokku
--custom-auth  Add support for custom AUTH_USER_MODEL
```

The `--docker` flag will create a `Dockerfile` as well as a `docker-compose.yml` file within your project. These are pre-configured to support the following services: web (the Django application itself), a database (`postgres`), proxy server (`nginx`), and a caching server (`redis`).

The `--dokku` flag will add dokku-specific configuration to your project within the `dokku` directory. The default configuration will allow you to push to your dokku-enabled remote server and deploy your Django project in an instant.

The `--custom-auth` flag is used to provide a simple override of the `AUTH_USER_MODEL`. This creates a `User` model under `authentication.models.user`. One can simply specify the override in `settings.py` by setting:

```python
AUTH_USER_MODEL = 'authentication.User'
```

##### Project structure
This CLI makes some assumptions about the structure of your Django project.
1. It assumes that your apps are one level below the root of your project directory, one level below where `manage.py` is. For example:
```
mywebsite
├── mywebsite
│   ├── __init__.py
│   ├── blog
│   ├── radio
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
└── requirements.txt
```

2. It assumes that your app resources are grouped together by type in packages. For example:
```
radio
├── __init__.py
├── admin
├── apps.py
├── forms
├── middleware
├── migrations
├── models
├── serializers
├── templates
├── tests
├── urls.py
├── views
└── viewsets
```

3. Each class representing a `model`, `serializer`, `viewset`, or `form` is located in its own Python module. For example:
```
models/
├── album.py
├── artist.py
└── track.py
```

This is done in order to aid the CLI with the creation and deletion of files
in the project as we'll see under the [`generate`](#generator) and [`destroy`](#destroyer) commands.

#### Generator

The generator is accessible through the `generate` command (abbreviated `g`).
It can be used to create the following:
- **admin**
- **form**
- **model**
- **serializer**
- **template**
- **test**
- **view**
- **viewset**

If you need all of the above, you can use the **resource** sub-command instead of running the individual sub-commands listed above.

The generator supports `--dry`, meaning it can provide you with the output of the desired command without creating any files in your directory structure.
This is useful if you want to see what a command accomplishes before fully committing to it.

#### Generating Models
In order to generate a model, specify the type identifier and then the name of the attribute field. Type identifiers are abbreviated to a more generic name that omits the word `Field`. The input here is case-insensitive, but the fields will be properly CamelCased in the corresponding Python file as in the example below:

```bash
D generate model album text:title image:artwork bool:is_compilation
```

This would add the following model `album.py` under the `models` directory:
```python
import uuid
from django.db import models


class Album(models.Model):
    title = models.TextField(blank=True)
    artwork = models.ImageField(blank=True, upload_to='uploads')
    compilation = models.BooleanField(default=False)

    # Default fields. Used for record-keeping.
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        db_table = 'radio_albums'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
          super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.uuid}
```
As in the example above, the database table name is derived from both the app name (`radio`) and the model name (`album`).

This command supports the following flags:
```
--abstract         Creates an abstract model type.
--register-admin   Register model to admin site.
--register-inline  Register model to admin site as inline.
--test-case        Creates a TestCase for model.
--full             Adds all related resources and TestCase
--inherits         Add model inheritance.
```

Note the presence of the `--inherits` flag. You can specify a base model and the generated model will extend it. For example:
```bash
D generate model track -i audio
```

Will generate the following model:

```python
import uuid
from django.db import models
from .audio import Audio


class Track(Audio):
    # model fields here...
```

**Defaults**

As one can see, `class Meta` and `_str_` are added to a model by default along with `uuid`, `created_at` and `updated_at` fields.
The `db_table` name is inferred from the name of the app and the current model while the ordering attribute is defined based on the default `created_at` field.


**Relationships**

If a relationship identifier is passed, the attribute name will be used as the name of the model it relates to.
Specifying a relationship also checks the current app scope for the specified related model. If such model does not exist in scope, the CLI will prompt you to create the missing model. How to invoke the command:

```bash
D generate model track char:title belongsto:album
```

What the output would look like:
```python
import uuid
from django.db import models
from .album import Album

class Track(models.Model):
    title = models.CharField(max_length=100)
    album = models.ForeignKey(Album, related_name='tracks', on_delete=models.PROTECT)

    # Default fields. Used for record-keeping.
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        db_table = 'radio_tracks'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
          super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.uuid}'
```

Supported relationship identifiers:
- **FK**: ForeignKeyField
- **One**: OneToOneField
- **Many**: ManyToManyField

#### Generating Serializers and Viewsets
If you are working on an API and use the `Django REST Framework` to support your backend, you can also use the `django-clite` to create `serializers` and `viewsets`.

The commands are much like the ones used to generate a model except you don't specify any model attributes, just the model name:
```bash
D generate serializer album
```

Which outputs:
```python
from rest_framework import serializers
from .models import Album


class AlbumSerializer(serializers.ModelSerializer):

    class Meta:
        model = Album
        fields = "__all__"
```

Similarly, a `viewset` can be generated like so:

```bash
D generate viewset album
```

Which in turn would generate the following `viewset`:
```python
from rest_framework import viewsets
from rest_framework import permissions
from .router import router
from ..models import Album
from ..serializers import AlbumSerializer


class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
   
router.register('albums', AlbumViewSet)
```

#### Generating admin models
```bash
D generate admin album
```

This will generate an admin model (inlines supported through `--inline`). The admin model class will be saved under `admin/album.py`, or if an inline model, under `admin/inlines/album.py`:

```python
from django.contrib import admin
from ..models import Album

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    pass
```

An inline model would look like this:
```python
from django.contrib import admin
from ...models import Album

class AlbumInline(admin.StackedInline):
    model = Album
    extra = 1
```

#### Generating views
```bash
D generate view album --list
```

Specifying a flag of `--list` will generate a ListView as the one below. The `detail` flag will generate a DetailView. These are both class-based views. If a function-based view is preferred instead, one can simply run `D generate view blog`, to generate a view with the name `blog_view`.

```python
from django.utils import timezone
from django.view.generic.list import ListView
from ..models import Album

class AlbumListView(ListView):

    model = Album
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context
```

When generating list or detail views, the model name is inferred from the view name. This ensures consistency, as it also helps with other cli-related automation.

#### Generating templates
```
D generate template homepage
```

This command will simply generate an HTML template with the specified name.

```jinja2
{% load static from staticfiles %}

{% comment %}
    Template for homepage
    Describe the template here.
{% endcomment %}

{% block header %}{% endblock header %}

{% block body %}{% endblock body %}

{% block footer %}{% endblock footer %}

{% block scripts %}{% endblock scripts %}
```

----

#### Generating complete resources
The `resource` sub-command is ideal if you want to add a model along with admin, serializer, view, viewset, template, and tests. You can invoke the command the same way you would the model command:
```bash
D generate resource album text:title image:artwork bool:is_compilation fk:album
```
This will generate a model with the specified attributes and all the related classes specified above. For consistency sake, the underlying implementation will prompt you for the same things the `model` sub-command would.


#### Destroyer
This command can be used to undo all that a generator can generate.
So, following our example `Album` model, one can remove it from the project by simply running:

```bash
D destroy model album --full
```

**Supports:**
- **admin**
- **form**
- **model**
- **resource**
- **serializer**
- **template**
- **test**
- **view**
- **viewset**

----

### To Do
[Check open issues.](issues)


### Pull requests
This project is a work in progress. Contributions are very much welcome.


### LICENSE
**django-clite** is [BSD Licensed](LICENSE.txt).
