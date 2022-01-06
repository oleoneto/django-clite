import re
import inflection


def sanitized_string(text):
    """
    Ensures strings are properly sanitized
    and no special characters are present.
    """

    r = inflection.transliterate(text.strip())
    r = re.sub(r"[\:\.\,\;\\\/\?\!\&\$\#\@\)\(\+\=\'\"\-\|\s]+", "_", r)
    return inflection.underscore(r).lower()


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
