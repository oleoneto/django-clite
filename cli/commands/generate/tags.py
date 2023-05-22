import click
from cli.utils import sanitized_string_callback
from cli.core.filesystem import File, FileSystem
from cli.core.templates import TemplateParser


@click.command()
@click.argument("name", required=True, callback=sanitized_string_callback)
@click.pass_context
def tag(ctx, name):
    """
    Generate a template tag.
    """

    file = File(
        path=f"templatetags/{name}.py",
        template="templatetags/tag.tpl",
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
