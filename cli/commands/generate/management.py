import click
from cli.utils import sanitized_string_callback
from cli.core.filesystem.filesystem import File, FileSystem
from cli.core.templates.template import TemplateParser
from cli.decorators.scope import scoped, Scope


@scoped(to=Scope.APP)
@click.command(name="command")
@click.argument("name", required=True, callback=sanitized_string_callback)
@click.pass_context
def management(cls, name):
    """
    Generate an application command.
    """

    file = File(
        path=f"management/{name}.py",
        template="management.tpl",
        context={
            "name": name,
        },
    )

    FileSystem().create_file(
        file=file,
        content=TemplateParser().parse_file(
            filepath=file.template,
            variables=file.context,
        ),
    )
