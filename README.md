# Django CLI [WIP]

CLI that handles creating and managing Django projects

#### Requirements
[Requirements](requirements.txt)


#### Installation [WIP]
Start by cloning the repo.
```
git clone https://github.com/oleoneto/Django-CLI.git
cd Django-CLI
pip install .
```

----

#### Commands
```
destroy   Removes models, serializers, and other...
generate  Adds models, routes, and other resources
new       Creates projects and apps
```

----

## New
The `new` command (abbreviated `n`) can be used to start new projects as well as new applications. The command tries to simplify how a project is created as well as the applications contained in it. Here's an example of such simplification:

Suppose you want to start a new project and want to create two apps within it:
```
django-admin startproject API
cd API/API/
django-admin startapp developers
```

The equivalent command in this CLI is:
```
django-cli new project API developers
```
Specifying an `app` when creating a project is optional, but you're likely to need to create one inside of your project directory, so the CLI can handle the creation of all of your apps as arguments after your project name.

#### Project structure
This CLI makes some assumptions about the structure of your Django project.
1. It assumes that your apps are one level below the root of your project directory, one level below where `manage.py` is. For example:
```
PROJECT
├── PROJECT
│   ├── __init__.py
│   ├── My_Application_1
│   ├── My_Application_2
│   ├── My_Application_3
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
└── requirements.txt
```
2. It assumes that your app resources are grouped together by type. For example:
```
My_Application_1
├── __init__.py
├── admin.py
├── apps.py
├── forms
├── migrations
├── models
├── serializers
├── templates
├── tests
├── urls.py
├── views
└── viewsets
```
3. Each class representing a `model`, `serializer`, `viewset`, or `form` is located in its own Python file. For example:
```
models
├── album.py
├── book.py
└── person.py
```

This is done in order to aid the CLI with the creation and deletion of files
in the project as we'll see under the [`generate`](#generator) and [`destroy`](#destroyer) commands.

----

## Generator

The generator is accessible through the `generate` command (abbreviated `g`).
It can be used to create the following resources:
- **forms**
- **models**
- **routes**
- **serializers**
- **viewsets**

The generator supports `--dry-run`, meaning it can provide you with the console log
of the desired command without creating any files in your directory structure.
This is useful if you want to see what a command accomplishes before fully committing to it.


#### Generating Models
In order to generate a model, specify the type identifier and then the name of the attribute field.
Type identifiers are abbreviated to a more generic name that omits the word `Field`. The input here is case-insensitive,
but the fields will be properly CamelCased in the corresponding Python file as in the example below:

```bash
django-cli g model album text:title image:artwork bool:compilation
```

This would add the following model `album.py` under the `models` directory:
```python
from django.db import models
from cloudinary.models import CloudinaryField


class Album(models.Model):
    title = models.TextField(blank=True)
    artwork = models.ImageField(blank=True, upload_to='uploads')
    compilation = models.BooleanField(default=False)

    # Default fields. Used for record-keeping.
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        db_table = 'album'
        ordering = ['-created_at']

    def __str__(self):
        return self.created_at

```
**Defaults**

As one can see, `class Meta` and `_str_` are added to a model by default along with both `created_at` and `updated_at` fields.
The `db_table` name is inferred from the name of the model while the ordering attribute is defined based on the default `created_at` field.


**Relationships**

If a relationship identifier is passed, the attribute name will be used as the name of the model it relates to.
Specifying a relationship also adds an import statement to the model file. For example:
```bash
django-cli g model album fk:artist
```
Would create an `artist` attribute like so:
```python
from django.db import models
from cloudinary.models import CloudinaryField
from .artist import Artist

class Album(models.Model):
    artist = models.ForeignKey(Artist, related_name='albums', on_delete=models.DO_NOTHING)

    # Default fields. Used for record-keeping.
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        db_table = 'album'
        ordering = ['-created_at']

    def __str__(self):
        return self.created_at

```

Currently supported relationship identifiers
- **FK**: ForeignKeyField
- **One**: OneToOneField
- **Many**: ManyToManyField

#### Generating Serializers and Viewsets
If you are working on an API and use the `Django REST Framework` to support your
project backend, you can also use this CLI to create `serializers` and `viewsets`.

The commands are much like the ones used to generate a model except you don't specify any model attributes, just the model name:

```bash
django-cli g serializer album
```

Which outputs:
```python
from rest_framework import serializers
from ..models.album import Album


class AlbumSerializer(serializers.ModelSerializer):

    # Add related fields below:
    # Example relation fields are:
    # -- HyperlinkedIdentityField
    # -- HyperlinkedRelatedField
    # -- PrimaryKeyRelatedField
    # -- SlugRelatedField
    # -- StringRelatedField

    # You can also create a custom serializer, like so:
    # likes = LikeSerializer(many=True)

    class Meta:
        model = Album
        fields = "__all__"
```

Similarly, a `viewset` can be generated like so:

```bash
django-cli g viewset album
```

Which in turn would generate the following `viewset`:
```python
from rest_framework import viewsets
from ..models.album import Album
from ..serializers.album import AlbumSerializer


class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
```

----

## Destroyer
This command can be used to undo all that a generator can generate.
So, following our example `Album` model, one can remove it from the project by simply running:

```bash
django-cli d model album
```

**Supported options:**
- **form**
- **model**
- **viewset**
- **serializer**

----

### To Do
[Check open issues.](https://github.com/oleoneto/Django-CLI/issues)

----

### Pull requests
This project is a work in progress. Contributions are very much welcome.

----

### LICENSE
**Django CLI** is [MIT Licensed](LICENSE).
