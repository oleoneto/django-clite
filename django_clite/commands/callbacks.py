from django_clite.cli.utils import sanitized_string
from django_clite.core.field_parser.factory import AttributeFactory


def sanitized_string_callback(_ctx, _param, value):
    return sanitized_string(value)


def fields_callback(ctx, _param, values):
    return AttributeFactory().parsed_fields(values)
