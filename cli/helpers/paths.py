# cli:decorators
import os


def add_app_package_paths_to_context(context):
    context.obj['in_app'] = 'apps.py' in os.listdir('.')

    context.obj['cwd'] = os.getcwd()

    context.obj['admin'] = f"{os.getcwd()}/admin/"
    context.obj['admin_inlines'] = f"{os.getcwd()}/admin/inlines/"
    context.obj['fixtures'] = f"{os.getcwd()}/fixtures/"
    context.obj['forms'] = f"{os.getcwd()}/forms/"
    context.obj['migrations'] = f"{os.getcwd()}/migrations/"
    context.obj['models'] = f"{os.getcwd()}/models/"
    context.obj['models_tests'] = f"{os.getcwd()}/models/tests/"
    context.obj['managers'] = f"{os.getcwd()}/models/managers"
    context.obj['serializers'] = f"{os.getcwd()}/serializers/"
    context.obj['serializers_tests'] = f"{os.getcwd()}/serializers/tests/"
    context.obj['tests'] = f"{os.getcwd()}/tests/"
    context.obj['templates'] = f"{os.getcwd()}/templates/"
    context.obj['views'] = f"{os.getcwd()}/views/"
    context.obj['viewsets'] = f"{os.getcwd()}/viewsets/"
