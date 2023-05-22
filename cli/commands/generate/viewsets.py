import click
import inflection
from cli.utils import sanitized_string_callback
from cli.core.filesystem import File, FileSystem
from cli.core.templates import TemplateParser


import_template = """from .{{module}} import {{classname}}ViewSet"""


@click.command()
@click.argument("name", required=True, callback=sanitized_string_callback)
@click.option("--read-only", is_flag=True, help="Create a read-only viewset.")
@click.pass_context
def viewset(ctx, name, read_only):
    """
    Generate a viewset for a serializable model.
    """

    file = File(
        path=f"viewsets/{name}.py",
        template="viewsets/viewset.tpl",
        context={
            "name": name,
            "module": name,
            "read_only": read_only,
            "namespace": inflection.pluralize(name),
            "classname": inflection.camelize(name),
        },
    )

    FileSystem().create_file(
        file=file,
        content=TemplateParser().parse_file(
            filepath=file.template,
            variables=file.context,
        ),
    )
