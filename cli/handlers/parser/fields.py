import inflection
from cli.utils.sanitize import sanitized_string
from cli.handlers.filesystem.template_handler import ResourceTemplateHandler


class FieldParsingError(Exception):
    pass


class DjangoField(object):
    def __init__(self, name, kind, model='', options: dict = {}, supported_in_admin: bool = True):
        self.name = sanitized_string(name)
        self.kind = kind
        self.model = model
        self.options = options
        self.supported_in_admin = supported_in_admin

    def template(self):
        temp = self.options.pop('template', None)
        related_name = inflection.pluralize(self.model)
        filepath = inflection.pluralize(self.name)

        content = ResourceTemplateHandler.parsed_template(
            raw=True,
            template=temp,
            context={
                'name': self.name,
                'related_name': related_name,
                'path': filepath
            },
        ) if temp else ""

        for key, value in self.options.items():
            content += f"{key}={value}, "

        content = content.strip()
        content = content[:-1] if content.endswith(',') else content

        return f"""{self.name} = {self.kind}({content})"""

    def __str__(self):
        return f"{self.kind}:{self.name}"


class FieldFactory:
    @classmethod
    def make_field(cls, kind, name, model):
        if kind in ['big', 'bigint', 'big-int']:
            return DjangoField(
                name,
                kind='BigIntegerField'
            )

        if kind in ['bool', 'boolean']:
            return DjangoField(
                name,
                kind='BooleanField',
                options={'default': False}
            )

        if kind in ['char']:
            return DjangoField(
                name,
                kind='CharField',
                options={'max_length': 100, 'blank': False}
            )

        if kind in ['date']:
            return DjangoField(
                name,
                kind='DateField',
                options={'auto_now': True}
            )

        if kind in ['datetime']:
            return DjangoField(
                name,
                kind='DateTimeField',
                options={'auto_now': True}
            )

        if kind in ['dec', 'decimal']:
            return DjangoField(
                name,
                kind='DecimalField'
            )

        if kind in ['duration']:
            return DjangoField(
                name,
                kind='DurationField'
            )

        if kind in ['email']:
            return DjangoField(
                name,
                kind='EmailField'
            )

        if kind in ['file']:
            return DjangoField(
                name,
                model=model,
                kind='FileField',
                supported_in_admin=False,
                options={'template': """blank=False, upload_to='uploads/{{path}}/'"""}
            )

        if kind in ['filepath', 'file-path']:
            return DjangoField(
                name,
                kind='FilePathField',
                supported_in_admin=False,
                options={'template': """blank=True, upload_to='uploads/{{path}}/'"""}
            )

        if kind in ['float']:
            return DjangoField(
                name,
                kind='FloatField'
            )

        if kind in ['belongsto', 'belongs-to', 'fk', 'foreignkey', 'foreign-key']:
            return DjangoField(
                name,
                model=model,
                kind='ForeignKey',
                options={'template': """{{name.capitalize()}}, related_name='{{related_name}}', blank=False"""}
            )

        if kind in ['ip', 'ipaddress', 'ip-address']:
            return DjangoField(
                name,
                kind='GenericIPAddressField'
            )

        if kind in ['image', 'photo']:
            return DjangoField(
                name,
                kind='ImageField',
                supported_in_admin=False,
                options={'template': """blank=False, upload_to='uploads/{{path}}/'"""},
            )

        if kind in ['int', 'integer']:
            return DjangoField(
                name,
                kind='IntegerField',
            )

        if kind in ['hasmany', 'has-many', 'many', 'manytomany', 'many-to-many']:
            return DjangoField(
                name,
                model=model,
                kind='ManyToManyField',
                supported_in_admin=False,
                options={'template': """{{name.capitalize()}}, related_name='{{related_name}}', blank=True"""}
            )

        if kind in ['hasone', 'has-one', 'one', 'onetoone', 'one-to-one']:
            return DjangoField(
                name,
                model=model,
                kind='OneToOneField',
                options={'template': "{{name.capitalize()}}, related_name='{{related_name}}', on_delete=models.CASCADE"}
            )

        if kind in ['slug']:
            return DjangoField(
                name,
                kind='SlugField',
                options={'unique': True}
            )

        if kind in ['string', 'text']:
            return DjangoField(
                name,
                kind='TextField',
                supported_in_admin=False,
                options={'blank': False}
            )

        if kind in ['time']:
            return DjangoField(
                name,
                kind='TimeField',
                options={'auto_now': True}
            )

        if kind in ['url']:
            return DjangoField(name, kind='URLField')

        if kind in ['uuid']:
            return DjangoField(
                name,
                kind='UUIDField',
                options={'template': """default=uuid.uuid4, editable=False"""}
            )

        raise FieldParsingError(f"Field `{kind}:{name}` cannot be parsed. `{kind}` is not a valid field type.")
