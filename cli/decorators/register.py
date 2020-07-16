REGISTRY = dict()


def register(f):
    """
    Register a function as a plugin
    """

    REGISTRY[f.__name__] = f
    return f
