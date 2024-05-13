# cli:core:field_parser
import inflection
# from typing import NamedTuple
from dataclasses import dataclass
from geny.core.decorators.singleton import singleton


json_compatible_fields = {
    "BigIntegerField": "pyint",
    "BooleanField": "pybool",
    "CharField": "text",
    "DateField": "future_date",
    "DateTimeField": "iso8601",
    "DecimalField": "pydecimal",
    "EmailField": "safe_email",
    "GenericIPAddressField": "ipv4",
    "FileField": "file_path",
    "FilePathField": "file_path",
    "FloatField": "pyfloat",
    "ImageField": "image_url",
    "IntegerField": "pyint",
    "SlugField": "slug",
    "TextField": "text",
    "TimeField": "time",
    "URLField": "url",
    "UUIDField": "uuid4",
}


@dataclass
class FieldOptions:
    kind: str
    options: dict = None
    supports_admin: bool = True
    is_fk_relationship: bool = False
    is_many_relationship: bool = False

    @property
    def is_relationship(self) -> bool:
        return self.is_fk_relationship or self.is_many_relationship

    @property
    def is_media_field(self) -> bool:
        return self.kind in ["FileField", "FilePathField", "ImageField"]

    @classmethod
    def klass_name(cls, attr_name):
        return inflection.camelize(inflection.singularize(attr_name)).strip()

    @classmethod
    def module_name(cls, attr_name):
        return inflection.singularize(attr_name).strip()

    @classmethod
    def upload_path(cls, attr_name, model_name) -> str:
        if not cls.is_media_field:
            return ""

        return f"uploads/{inflection.pluralize(model_name.lower())}/{inflection.pluralize(attr_name)}/"

    @property
    def example_value(self):
        x = json_compatible_fields.get(self.kind, "")
        return x

    def field_options(self, attr_name: str, model_name: str):
        if self.options is None:
            self.options = {}

        if self.is_relationship:
            self.options.update(
                {"related_name": f"'{inflection.pluralize(inflection.dasherize(model_name.lower()))}'"}
            )

        options = [self.klass_name(attr_name)] if self.is_relationship else []
        options.append(f"_('{attr_name}')")

        if self.options is None:
            return ""

        for k, v in self.options.items():
            options.append(f"{k}={v}")

        if self.is_media_field:
            options.append(f"upload_to='{self.upload_path(attr_name, model_name)}'")

        return ", ".join(options)


@singleton
class AttributeFactory:
    def __init__(self, associations: dict[str, FieldOptions], aliases: dict[str, str]):
        self.registry = associations
        self.aliases = aliases

    def field_options(self, kind: str, name: str) -> FieldOptions:
        if kind == "":
            return None

        options = self.registry.get(kind, None)

        if options is None:
            alias = self.aliases.get(kind, None)
            options = self.registry.get(alias, None)

        if options is None:
            return None

        return options

    def parsed_fields(self, values: list[str]) -> dict[str, FieldOptions]:
        pairs = dict(arg.split(':') for arg in values)

        fields = {}
        for n, k in pairs.items():
            f = self.field_options(k, n)
            fields[n] = f

        return fields


attribute_aliases = {
    "bigint": "big",
    "big-int": "big",
    "integer": "int",
    "boolean": "bool",
    "string": "text",
    "file-path": "filepath",
    "photo": "image",
    "ipaddress": "ip",
    "ip-address": "ip",
    "belongsto": "fk",
    "belongs-to": "fk",
    "foreignkey": "fk",
    "foreign-key": "fk",
    "one-to-one": "one",
    "hasone": "one",
    "has-one": "one",
    "many": "hasmany",
    "has-many": "hasmany",
    "manytomany": "hasmany",
    "many-to-many": "hasmany",
}

field_registry = {
    # Relationships
    "fk": FieldOptions(kind="ForeignKey", options={"blank": False, "on_delete": "models.DO_NOTHING"}, is_fk_relationship=True),
    "one": FieldOptions(
        kind="OneToOneField",
        options={"blank": False, "on_delete": "models.CASCADE", "primary_key": True}, is_fk_relationship=True
    ),
    "hasmany": FieldOptions(
        kind="ManyToManyField",
        options={"blank": True, "on_delete": "models.DO_NOTHING"},
        supports_admin=False,
        is_many_relationship=True
    ),

    # Boolean
    "bool": FieldOptions(kind="BooleanField", options={"default": False}),

    # Numeric
    "big": FieldOptions(kind="BigIntegerField"),
    "decimal": FieldOptions(kind="DecimalField", options={"decimal_places": 2, "max_digits": 8}),
    "float": FieldOptions(kind="FloatField"),
    "int": FieldOptions(kind="IntegerField"),

    # Text
    "char": FieldOptions(kind="CharField", options={"max_length": 100, "blank": False}),
    "email": FieldOptions(kind="EmailField"),
    "slug": FieldOptions(kind="SlugField", options={"unique": True}),
    "text": FieldOptions(kind="TextField", options={"blank": False}, supports_admin=False),
    "url": FieldOptions(kind="URLField"),
    "uuid": FieldOptions(kind="UUIDField", options={"default": "uuid.uuid4", "editable": False}),

    # Files
    "file": FieldOptions(kind="FileField", options={"blank": False}, supports_admin=False),
    "filepath": FieldOptions(kind="FilePathField", options={"blank": True}, supports_admin=False),
    "image": FieldOptions(kind="ImageField", options={"blank": False}, supports_admin=False),

    # Date
    "date": FieldOptions(kind="DateField", options={"auto_now": True}),
    "datetime": FieldOptions(kind="DateTimeField", options={"auto_now": True}),
    "duration": FieldOptions(kind="DurationField"),
    "time": FieldOptions(kind="TimeField", options={"auto_now": True}),

    # Ip
    "ip": FieldOptions(kind="GenericIPAddressField"),
}

# Singleton
AttributeFactory(field_registry, attribute_aliases)
