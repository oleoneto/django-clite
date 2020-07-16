def set_path(path):
    """
    Register a unit on a function
    """

    def decorator_set_path(f):
        f.path = path
        return f
    return decorator_set_path
