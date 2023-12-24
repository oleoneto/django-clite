# cli:core:field_parser
import inflection

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


class Field:
    def __init__(
            self,
            kind: str,
            name: str = "",
            model: str = "",
            options: dict = None,
            supports_admin: bool = True,
            is_fk_relationship: bool = False,
            is_many_to_many_relationship: bool = False,
    ):
        self.model = model
        self.kind = kind
        self.name = name
        self.supported_in_admin = supports_admin
        self.is_fk_relationship = is_fk_relationship
        self.is_many_relationship = is_many_to_many_relationship
        self._options = {} if options is None else options

    @property
    def is_relationship(self) -> bool:
        return self.is_fk_relationship or self.is_many_relationship

    @property
    def is_media_field(self) -> bool:
        return self.kind in ["FileField", "FilePathField", "ImageField"]

    @property
    def klass_name(self):
        return inflection.camelize(inflection.singularize(self.name)).strip()

    @property
    def module_name(self):
        return inflection.singularize(self.name).strip()

    @property
    def upload_path(self) -> str:
        if not self.is_media_field:
            return ""

        return f"uploads/{inflection.pluralize(self.model.lower())}/{inflection.pluralize(self.name)}/"

    @property
    def example_value(self):
        if json_compatible_fields.get(self.kind):
            return ""
        return None

    @property
    def options(self):
        if self.is_relationship:
            self._options.update(
                {"related_name": f"'{inflection.singularize(self.model.lower())}'"}
            )

        options = [self.klass_name] if self.is_relationship else []
        options.append(f"_('{self.name}')")

        for k, v in self._options.items():
            options.append(f"{k}={v}")

        if self.is_media_field:
            options.append(f"upload_to='{self.upload_path}'")

        return ", ".join(options)


__many_to_many_relationship_field = Field(
    kind="ManyToManyField",
    options={"blank": True, "on_delete": "models.DO_NOTHING"},
    supports_admin=False,
)

__foreign_key_relationship_field = Field(
    kind="ForeignKey", options={"blank": False, "on_delete": "models.DO_NOTHING"}
)

__one_to_one_relationship_field = Field(
    kind="OneToOneField",
    options={"blank": False, "on_delete": "models.CASCADE", "primary_key": True},
)

__big_integer_field = Field(kind="BigIntegerField")

__generic_ip_field = Field(kind="GenericIPAddressField")

__fields = {
    # Numeric
    "big": __big_integer_field,
    "bigint": __big_integer_field,
    "big-int": __big_integer_field,
    "decimal": Field(kind="DecimalField"),
    "float": Field(kind="FloatField"),
    "int": Field(kind="IntegerField"),
    "integer": Field(kind="IntegerField"),
    # Boolean
    "bool": Field(kind="BooleanField", options={"default": False}),
    "boolean": Field(kind="BooleanField", options={"default": False}),
    # Text
    "char": Field(kind="CharField", options={"max_length": 100, "blank": False}),
    "email": Field(kind="EmailField"),
    "slug": Field(kind="SlugField", options={"unique": True}),
    "string": Field(kind="TextField", options={"blank": False}, supports_admin=False),
    "text": Field(kind="TextField", options={"blank": False}, supports_admin=False),
    "url": Field(kind="URLField"),
    "uuid": Field(
        kind="UUIDField", options={"default": "uuid.uuid4", "editable": False}
    ),
    # Files
    "file": Field(kind="FileField", options={"blank": False}, supports_admin=False),
    "filepath": Field(
        kind="FilePathField", options={"blank": True}, supports_admin=False
    ),
    "file-path": Field(
        kind="FilePathField", options={"blank": True}, supports_admin=False
    ),
    "image": Field(kind="ImageField", options={"blank": False}, supports_admin=False),
    "photo": Field(kind="ImageField", options={"blank": False}, supports_admin=False),
    # Date
    "date": Field(kind="DateField", options={"auto_now": True}),
    "datetime": Field(kind="DateTimeField", options={"auto_now": True}),
    "duration": Field(kind="DurationField"),
    "time": Field(kind="TimeField", options={"auto_now": True}),
    # Ip
    "ip": __generic_ip_field,
    "ipaddress": __generic_ip_field,
    "ip-address": __generic_ip_field,
    # Relationships
    # - FK
    "belongsto": __foreign_key_relationship_field,
    "belongs-to": __foreign_key_relationship_field,
    "fk": __foreign_key_relationship_field,
    "foreignkey": __foreign_key_relationship_field,
    "foreign-key": __foreign_key_relationship_field,
    # - One
    "one": __one_to_one_relationship_field,
    "one-to-one": __one_to_one_relationship_field,
    "hasone": __one_to_one_relationship_field,
    "has-one": __one_to_one_relationship_field,
    # - Many
    "hasmany": __many_to_many_relationship_field,
    "has-many": __many_to_many_relationship_field,
    "many": __many_to_many_relationship_field,
    "manytomany": __many_to_many_relationship_field,
    "many-to-many": __many_to_many_relationship_field,
}


def make_field(kind, name, model) -> Field:
    f = __fields.get(kind)

    if f is not None:
        f.name = name
        f.model = model

        if f.kind in ["ForeignKey", "OneToOneField"]:
            f.is_fk_relationship = True

        if f.kind in ["ManyToManyField"]:
            f.is_many_relationship = True

        return f

    return Field(kind=None, name=None, model=None, options=None)
