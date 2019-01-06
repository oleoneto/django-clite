# Django CLI [WIP]

CLI that handles creating and managing Django projects

#### Minimum requirements
- `click 7.x`
- `django 2.1`
- `python 3.6`
- `pip`
- `git`


#### Installation [WIP]
Start by cloning the repo.
```
git clone https://github.com/oleoneto/Django-CLI.git
cd Django-CLI
pip install .
```


#### Project structure [WIP]
This CLI makes some assumptions about the structure of your Django application.
It assumes that each of your resources (models, forms, serializers) are grouped 
together and that each resource is kept in its own Python file.

This is done in order to aid the CLI with the creation and deletion of files
in the project as we'll see under the [`generate`](#generator) and [`destroy`](#destroyer) commands. 

-----------------------------------------------

#### Commands [WIP]
```
destroy   Model, route, and template destroyer
generate  Model, route, and template generator
```

---------------------------------------------


## Generator

The generator is accessible through the `generate` command. 
It can be used to create the following resources:
- forms 
- models
- routes
- serializers
- viewsets

The generator supports `dry run`, meaning it can provide you with the console log 
of the desired command without creating any files in your directory structure. 
This is useful if you want to see what a command accomplishes before committing to it.


#### Generating Models
In order to generate a model, specify the type identifier and then the name of the attribute field. 
Type identifiers are abbreviated to a more generic name that omits the word `Field`. The input here is case-insensitive, 
but the fields will be CamelCased in the python file as in the example specified below:

```bash
django-cli generate model album text:title image:artwork bool:compilation
```

This would add the following model `album.py` under the `models` directory:
```python
from django.db import models


class Album(models.Model):
    title = models.TextField(blank=True)
    artwork = models.ImageField(blank=True, upload_to='uploads')
    compilation = models.BooleanField(default=False)
    
    # Default fields. Omit with the --no-defaults flag
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
django-cli generate model album fk:artist
```
Would create an `artist` attribute like so:
```python
from django.db import models
from .artist import Artist


class Album(models.Model):
    artist = models.ForeignKey(Artist, related_name='albums', on_delete=models.DO_NOTHING)
    
    # Default fields. Omit with the --no-defaults flag
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        db_table = 'album'
        ordering = ['-created_at']
        
    def __str__(self):
        return self.created_at

```

Currently supported relationship identifiers
- FK: ForeignKeyField
- One: OneToOneField
- Many: ManyToManyField


-----------------------------

## Destroyer
This command can be used to undo all that a generator can generate.
So, following our example `Album` model, one can remove it from the project by simply running:

```bash
djangocli destroy model album
```

**Supported options:**
- form
- model
- viewset
- serializer

-----------------------------


### Pull requests
This project is a work in progress. Contributions are very much welcome.

**Django CLI** is [MIT Licensed](LICENSE).
