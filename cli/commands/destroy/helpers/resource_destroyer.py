import os

import inflection
from cli.handlers.filesystem.file_handler import FileHandler
from cli.handlers.filesystem.template_handler import ResourceTemplateHandler
from cli.utils.fs.utils import change_directory
from cli.utils.sanitize import sanitized_string
from cli.utils.logger import Logger


def resource_destroyer(
        name,
        package,
        parent=None,
        filename=None,
        file_extension='.py',
        import_template=None,
        template_handler=ResourceTemplateHandler,
        **kwargs
):
    fh = FileHandler()

    # Context variables
    project_files = kwargs.get('project_files', {})
    app_file = project_files.get('apps.py', None)

    # app = app_file.parent.name
    # project = app_file.parent.parent.name

    name = sanitized_string(name)

    # Force filename if one does not exist
    filename = filename or f"{name}{file_extension}"

    scope = kwargs.get('scope', inflection.singularize(inflection.camelize(package)))
    classname = inflection.camelize(name)

    try:
        if parent:
            change_directory(parent, **kwargs)
        change_directory(package, **kwargs)
    except FileNotFoundError:
        Logger.log(f'File or directory {parent or package} does not exit.')
        return

    # FIXME: delete files
    fh.remove_file(filename, path=os.getcwd(), **kwargs)

    if kwargs.get('ignore_import', False):
        pass
    else:
        default_context = {'name': name, 'module': name, 'classname': f"{classname}{scope}"}
        default_context.update(kwargs.get('import_context', {}))

        content = template_handler.parsed_template(
            import_template or """from .{{name}} import {{classname}}""",
            context=default_context,
            raw=import_template is None or type(import_template).__name__ == 'str'
        )
        fh.remove_line_from_file(content, filename='__init__.py', **kwargs)
    if parent:
        change_directory('..')
    change_directory('..')
