# cli:decorators
import os


def add_app_package_paths_to_context(context):
    context.obj['in_app'] = 'apps.py' in os.listdir('../handlers')

    context.obj['cwd'] = os.getcwd()

    context.obj['admin'] = f"{os.getcwd()}/admin/"
    context.obj['admin_actions'] = f"{os.getcwd()}/admin/actions/"
    context.obj['admin_inlines'] = f"{os.getcwd()}/admin/inlines/"
    context.obj['admin_permissions'] = f"{os.getcwd()}/admin/permissions/"
    context.obj['fixtures'] = f"{os.getcwd()}/fixtures/"
    context.obj['forms'] = f"{os.getcwd()}/forms/"
    context.obj['migrations'] = f"{os.getcwd()}/migrations/"
    context.obj['models'] = f"{os.getcwd()}/models/"
    context.obj['models_permissions'] = f"{os.getcwd()}/models/permissions/"
    context.obj['models_tests'] = f"{os.getcwd()}/models/tests/"
    context.obj['models_validators'] = f"{os.getcwd()}/models/validators/"
    context.obj['managers'] = f"{os.getcwd()}/models/managers"
    context.obj['serializers'] = f"{os.getcwd()}/serializers/"
    context.obj['serializers_tests'] = f"{os.getcwd()}/serializers/tests/"
    context.obj['search_indexes'] = f"{os.getcwd()}/search_indexes/"
    context.obj['signals'] = f"{os.getcwd()}/models/signals/"
    context.obj['tasks'] = f"{os.getcwd()}/tasks/"
    context.obj['templates'] = f"{os.getcwd()}/templates/"
    context.obj['templatetags'] = f"{os.getcwd()}/templatetags/"
    context.obj['views'] = f"{os.getcwd()}/views/"
    context.obj['viewsets'] = f"{os.getcwd()}/viewsets/"
