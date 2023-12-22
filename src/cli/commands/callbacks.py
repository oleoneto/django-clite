from cli.utils import sanitized_string
from cli.core.field_parser.factory import make_field


def sanitized_string_callback(ctx, param, value):
    return sanitized_string(value)


def fields_callback(ctx, param, value):
    model_fields = []
    model_relationships = []

    model = ctx.params.get("name")

    for pair in value:
        # Ignore malformed field pairs
        if pair.find(":") == -1:
            continue

        kind, name = pair.split(":")

        f = make_field(kind=kind, name=name, model=model)
        if f.kind is not None:
            model_fields.append(f)

            if f.is_relationship:
                model_relationships.append(f)

    return model_fields, model_relationships
