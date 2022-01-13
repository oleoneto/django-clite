DEFAULT_NOT_IN_SCOPE_WARNING = """Cannot find model {} in {} scope. Want to create model?"""

SPECIAL_RELATIONSHIP = ['get_user_model()']

JSON_COMPATIBLE_FIELDS = {
    'BigIntegerField': 'pyint',
    'BooleanField': 'pybool',
    'CharField': 'text',
    'DateField': 'future_date',
    'DateTimeField': 'iso8601',
    'DecimalField': 'pydecimal',
    'EmailField': 'safe_email',
    'GenericIPAddressField': 'ipv4',
    'FileField': 'file_path',
    'FilePathField': 'file_path',
    'FloatField': 'pyfloat',
    'ImageField': 'image_url',
    'IntegerField': 'pyint',
    'SlugField': 'slug',
    'TextField': 'text',
    'TimeField': 'time',
    'URLField': 'url',
    'UUIDField': 'uuid4',
}

DEFAULT_SPECIAL_INHERITABLE_TYPES = {
    'abstract-user': 'django.contrib.auth.models',
    'abstract-base-user': 'django.contrib.auth.models',
    'base-user': 'django.contrib.auth.models',
    'user': 'django.contrib.auth.models',
}

