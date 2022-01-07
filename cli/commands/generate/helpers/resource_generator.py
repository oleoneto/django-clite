import inflection
from cli.utils.sanitize import sanitized_string
from cli.utils.fs.utils import change_directory
from cli.handlers.filesystem.template_handler import ResourceTemplateHandler as rth
from cli.handlers.filesystem.file_handler import FileHandler
from cli.handlers.filesystem.directory import Directory


def resource_generator(name, package, template, import_template=None, file_extension='.py', template_handler=rth, **kwargs):
    fh = FileHandler()

    project_files = kwargs.get('project_files', {})
    app_file = project_files.get('apps.py', None)

    app = app_file.parent.name
    project = app_file.parent.parent.name

    # Context variables
    name = sanitized_string(name)
    namespace = inflection.pluralize(name)
    filename = f"{name}{file_extension}"
    scope = kwargs.get('scope', inflection.singularize(inflection.camelize(package)))
    classname = inflection.camelize(name)
    content = template_handler.parsed_template(template, context={
        'name': name,
        'classname': classname,
        'project': kwargs.get('project', project),
        'app': kwargs.get('app', app),
        'namespace': namespace,
        **kwargs.get('context', {}),
    })

    # Ensure the top-level package exists and is properly configured
    # Handle resource creation and import

    Directory.ensure_directory(package, **kwargs)

    change_directory(package, **kwargs)

    fh.create_file(content, filename, **kwargs)

    if kwargs.get('no_append', False):
        pass
    else:
        content = template_handler.parsed_template(
            import_template or """from .{{name}} import {{classname}}""",
            context=kwargs.get('import_context', {'name': name, 'module': name, 'classname': f"{classname}{scope}"}),
            raw=import_template is None or type(import_template).__name__ == 'str'
        )

        fh.append_to_file(
            content=content,
            filename='__init__.py',
            prevent_duplication=True,
            **kwargs,
        )
