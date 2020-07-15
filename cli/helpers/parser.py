import inflection


def sanitized_string(text):
    """
    Ensures strings are properly sanitized
    and no special characters are present.
    """

    r = inflection.transliterate(text)
    r = r.replace(' ', '-')
    return inflection.underscore(r).lower()
