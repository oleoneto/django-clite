# django-dj

A CLI tool that handles creating and managing Django projects

### Requirements
[Requirements](requirements.txt)


### Installation
Install via [pip](http://www.pip-installer.org/):
```
pip install django-dj
```

Install from source:
```
git clone https://bitbucket.org/oleoneto/django-dj.git
cd django-dj
pip install .
```

After installation, the CLI will expose the binary with three names, any of which can be used in place of another:
```
D
dj
django-dj
```


----

### Commands
```
destroy   Removes models, serializers, and other...
generate  Adds models, routes, and other resources
new       Creates projects and apps
```

----

### New
The `new` command (abbreviated `n`) can be used to start new projects as well as new applications. The command tries to simplify how a project is created as well as the applications contained in it. Here's an example of such simplification:

Suppose you want to start a new project and want to create two apps within it:
```
django-admin startproject mywebsite
cd mywebsite/mywebsite/
django-admin startapp blog
django-admin startapp radio
```

The equivalent command in the `django-dj` is:
```
D new project mywebsite blog radio
```
Specifying `apps` when creating a project is optional, but you're likely to need to create one inside of your project directory, so the CLI can handle the creation of all of your apps if you pass them as arguments after your project name.

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
models/
├── album.py
├── artist.py
└── track.py
```

This is done in order to aid the CLI with the creation and deletion of files
in the project as we'll see under the [`generate`](#generator) and [`destroy`](#destroyer) commands.

----

### Generator

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

**Defaults**

As one can see, `class Meta` and `_str_` are added to a model by default along with `uuid`, `created_at` and `updated_at` fields.
The `db_table` name is inferred from the name of the app and the current model while the ordering attribute is defined based on the default `created_at` field.


**Relationships**

If a relationship identifier is passed, the attribute name will be used as the name of the model it relates to.
Specifying a relationship also adds an import statement to the model file. For example:
```bash
D generate model album fk:artist
```

Would create an `artist` attribute like so:
```python
import uuid
from django.db import models
from .artist import Artist

class Album(models.Model):
    artist = models.ForeignKey(Artist, related_name='albums', on_delete=models.DO_NOTHING)

    # Default fields. Used for record-keeping.
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        db_table = 'album'
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
If you are working on an API and use the `Django REST Framework` to support your backend, you can also use the django-dj to create `serializers` and `viewsets`.

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

----

## Destroyer
This command can be used to undo all that a generator can generate.
So, following our example `Album` model, one can remove it from the project by simply running:

```bash
D destroy model album
```

**Supported options:**
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
[Check open issues.](https://bitbucket.org/oleoneto/django-dj/issues)

----

### Pull requests
This project is a work in progress. Contributions are very much welcome.

----

### LICENSE
**django-dj** is [BSD Licensed](LICENSE.txt).
