import click
from cli.utils import sanitized_string_callback
from cli.core.filesystem import File, FileSystem
from cli.core.templates import TemplateParser
from cli.constants import TEMPLATES_KEY


@click.command()
@click.argument("name", required=True, callback=sanitized_string_callback)
@click.pass_context
def validator(ctx, name):
    """
    Generate a validator.
    """

    file = File(
        path=f"models/validators/{name}.py",
        template="models/validator.tpl",
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
