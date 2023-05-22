import re
import inflection

from cli.core.fieldparser.factory import make_field


def check_noun_inflection(noun, force_singular=None, force_plural=None):
    """
    Checks whether a noun is plural or singular and gives
    the option to change the noun from plural to singular.
    """

    noun = noun.lower()
    singular = inflection.singularize(noun)
    plural = inflection.pluralize(noun)

    if force_plural == force_singular:
        return noun
    elif force_singular:
        return singular
    elif force_plural:
        return plural

    return noun


def sanitized_string(text):
    """
    Ensures strings are properly sanitized
    and no special characters are present.
    """

    r = inflection.transliterate(text.strip())
    r = re.sub(r"[\:\.\,\;\\\/\?\!\&\$\#\@\)\(\+\=\'\"\-\|\s]+", "_", r)
    return inflection.underscore(r).lower()


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
