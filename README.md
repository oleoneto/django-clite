# Django CLI [WIP]

CLI that handles creating and managing Django projects

#### Minimum requirements
- `django 2.1`
- `python 3.6`
- `pip`
- `git`


#### Installation [WIP]
Start by cloning the repo.
```
git clone https://github.com/oleoneto/Django-CLI.git
```

-----------------------------------------------

#### Commands
```
db        Handles various database activities
destroy   Model, route, and template destroyer
generate  Model, route, and template generator
install   Installs and updates requirements
new       Creates new apps and projects
```

---------------------------------------------


## Generator

The generator is accessible through the `generate` command. It can be used to create `forms`, `models`, `routes`, `serializers`, and `viewsets`.
The generator supports `dry run` meaning it can provide you with the console log of the desired command without creating any files in your directory structure. 
This is useful if you want to see what a command does before committing to it. 
You can also pipe the full output to a file and modify it to your liking. 
This is supported by providing the `generate` command with the `--save` flag.

So, instead of doing this:
```bash
django-cli generate --dry model Store char:name | cat > Store.py
```

You can do this:
```bash
django-cli generate --save model Store char:name
```

The `--save` flag will get the file names from the `form`, `model`, `serializer`, `route`, or `viewset` and add the object type to the name of the file to avoid clashing with other files.
The flag is non-destructive and will not create files if it encounters files with the same name in the output directory.


### Generating Models
In order to generate a model, specify the type identifier and then the name of the attribute field. 
Type identifiers are abbreviated to a more generic name without the word `Field`. The input here is case-insensitive, but the fields will be CamelCased in the python file. An example is specified below.

```bash
django-cli generate model Album text:title image:artwork bool:compilation
```

This would add the following in model in `models.py`:
```python
class Album(models.Model):
    title = models.TextField(blank=True)
    artwork = models.ImageField(blank=True, upload_to='/uploads/')
    compilation = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    
    class Meta:
        db_table = 'Album_table'
        ordering = ['-created_at']

    def __str__(self):
        return self.title
```
**Defaults**

As one can see, `class Meta` and `_str_` are added to a model by default along with both `created_at` and `updated_at` fields. 
The `db_table` name is inferred from the name of the model while the ordering attribute is defined based on the default `created_at` field. 
The return of the `__str__` is the last attribute of type `CharField` for the model.
Should defaults not be needed, one can optionally turn them off by passing the `--no-defaults` flag as argument. 
Please note that this flag will omit both `created_at` and `updated_at` fields as well as `class Meta` and `__str__`.


**Relationships**

If a relationship identifier is passed, the attribute name will be used as the name of the model it relates to. For example:
```bash
django-cli generate model Album FK:artist
```
Would create an attribute like so:
```python
artist = models.ForeignKey(Artist, related_name='albums', on_delete=models.DO_NOTHING)
```

Currently supported relationship identifiers
- FK: ForeignKeyField
- One: OneToOneField
- Many: ManyToManyField


**Model Admin**

If the `--admin` flag is specified, the following code is added to the `admin.py` file:
```python
class AlbumAdmin(admin.ModelAdmin):
	pass
	
admin.site.register(Album, AlbumAdmin)
```
No default implementations for the admin model are supported as of now.


**Supported flags for model generator**:
- `--admin`       Register model to admin site
- `--abstract`    Creates an abstract model type
- `--no-defaults` Omit class Meta, created_at, updated_at, and __str__

-------------------------

### Generating Routes

Routes are equivalent to `views` only here the CLI taken this idea a bit further and treats routes as say the `ember-cli` treats routes.
The generator is concerned with both the **view function** as well as the **html template** and the the **url pattern**. 
For consistency, the CLI gives the view, the template, as well as the url pattern the same name. Here's how you create a route:
```bash
django-cli generate route albums
```

This in turn will affect three different file:

In `views.py`
```python
def albums(request):
    context = {
        'active': True,
        'route': 'albums',
    }
    return render(request, 'albums.html', context)
```

In `albums.html`
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Albums</title>
    <link rel="stylesheet" href="static/css/main.css">
</head>
<body>
    <h1>Template fo Albums</h1>
    
    <script src="static/js/main.js"></script>
</body>
</html>
```

In `urls.py`
```python
urlpatterns += [ path('albums/', albums, name='albums') ]
```

**Defaults**

The route generator makes two assumptions: 1. a template file is needed, 2. a url pattern is needed. 
If this default behavior does not suit your project's design, you can disable the defaults by specifying the `--no-defaults` flag.
Alternatively, you can opt out of either default individually.

You can specify the name of a framework with your route to have both `css` and `js` CDN links be added to your linked stylesheets and scripts.
This version currently supports the following frameworks:
- Bootstrap (css, js)
- Bulma (css)
- Foundation (css, js)


**Supported flags for routes generator**
- `--no-template`     Do not generate a template file
- `--no-url`          Do not include in app's url patterns
- `--framework`       Name of css framework to link in stylesheets

-----------------------------



## Destroyer
Essentially undoes all that a generator would generate.



-----------------------------


## Installer
Management of dependencies and requirements.


-----------------------------


## Db
Handles database-related activities like generating and applying migrations, seeding and/or viewing the database.


-----------------------------


### Pull requests
This project is a work in progress. Contributions are very much welcome.

**Django CLI** is [MIT Licensed](LICENSE).
