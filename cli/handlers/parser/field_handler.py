import os
import inflection
import fileinput
from cli.handlers.parser.fields import FieldFactory
from cli.utils.sanitize import sanitized_string
# from faker.providers import company, date_time, internet, misc
# from faker import Faker


# fake = Faker()
# fake.add_provider(company)
# fake.add_provider(date_time)
# fake.add_provider(internet)
# fake.add_provider(misc)


def parse_fields(tokens: tuple, model: str = None):
    fields = []
    import_list = []

    for token in tokens:
        kind, name = token.split(':')
        field = FieldFactory.make_field(kind, name, model)

        fields.append(field)

        if field.kind in ['ForeignKey', 'ManyToManyField', 'OneToOneField']:
            import_list.append(field)

    return fields, import_list


def table_name_for_model(model, app=None):
    return f"{f'{sanitized_string(app)}_' if app else ''}{inflection.pluralize(sanitized_string(model))}"


def register_field(value, collection):
    """Ensure last key does not have an added comma"""
    if value not in collection:
        if len(collection) > 0:
            collection[-1] += ','

        value = value.replace(',', '')
        collection.append(value)


def jsonified_field(value):
    if type(value).__name__ == 'str':
        return f'"{value}"'
    if type(value).__name__ == 'bool':
        return f'{value}'.lower()
    return value


def related_resource_is_in_scope(model):
    """
    Searches the current directory for the specified model
    either by filename or import statement in __init__.py

    If the model is not found in the current scope, a warning is displayed
    asking the user whether the model should be created.
    """

    filename = model.lower()
    filename += ".py" if not model.endswith(".py") else ""

    # FIXME: This should read the file to check if a class for the `model` argument exists in it.
    if filename in os.listdir(os.getcwd()):
        return True

    try:
        package_initializer_file = f"{os.getcwd()}/__init__.py"
        for line in fileinput.input(package_initializer_file):
            if model.capitalize() in line:
                fileinput.close()
                return True
    except FileNotFoundError:
        fileinput.close()
        return False
