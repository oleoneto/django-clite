import re
import inflection


def inflect(noun, force_singular=False, force_plural=False):
    if force_plural == force_singular:
        return noun
    elif force_singular:
        return inflection.singularize(noun)
    elif force_plural:
        return inflection.pluralize(noun)

    return noun


def sanitized_string(text):
    r = inflection.transliterate(text.strip())
    r = re.sub(r"[:.,;\\/?!&$#@)(+=\'\"\-|\s]+", "_", r)
    r = r.strip("_")  # remove leading or trailing underscores
    return inflection.underscore(r).lower()
