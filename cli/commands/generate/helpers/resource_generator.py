import inflection
from cli.utils.sanitize import sanitized_string
from cli.utils.fs.utils import change_directory
from cli.handlers.parser.field_handler import table_name_for_model
from cli.handlers.filesystem.template_handler import ResourceTemplateHandler
from cli.handlers.filesystem.file_handler import FileHandler
from cli.handlers.filesystem.directory import Directory


def resource_generator(
        name,
        package,
        template,
        parent=None,
        filename=None,
        import_template=None,
        file_extension='.py',
        template_handler=ResourceTemplateHandler,
        **kwargs
):
    fh = FileHandler()

    # Context variables
    project_files = kwargs.get('project_files', {})
    app_file = project_files.get('apps.py', None)

    app = app_file.parent.name
    project = app_file.parent.parent.name

    name = sanitized_string(name)
    namespace = inflection.pluralize(name)

    # Force filename if one does not exist
    filename = filename or f"{name}{file_extension}"

    scope = kwargs.get('scope', inflection.singularize(inflection.camelize(package)))
    classname = inflection.camelize(name)
    content = template_handler.parsed_template(template, context={
        'name': name,
        'classname': classname,
        'project': kwargs.get('project', project),
        'app': kwargs.get('app', app),
        'namespace': namespace,
        'table_name': table_name_for_model(name, app),
        **kwargs.get('context', {}),
    })

    # Ensure the top-level package exists and is properly configured
    # Handle resource creation and import

    # TODO: perhaps instead of changing directories, I should pass a pathname to .create_file() instead

    if parent:
        Directory.ensure_directory(parent, **kwargs)
        change_directory(parent, **kwargs)
    Directory.ensure_directory(package, **kwargs)
    change_directory(package, **kwargs)

    fh.create_file(content, filename, **kwargs)

    if kwargs.get('no_append', False):
        pass
    else:
        default_context = {'name': name, 'module': name, 'classname': f"{classname}{scope}"}
        default_context.update(kwargs.get('import_context', {}))

        content = template_handler.parsed_template(
            import_template or """from .{{name}} import {{classname}}""",
            context=default_context,
            raw=import_template is None or type(import_template).__name__ == 'str'
        )

        fh.append_to_file(
            content=content,
            filename='__init__.py',
            prevent_duplication=True,
            **kwargs,
        )

    if parent:
        change_directory('..')
    change_directory('..')
