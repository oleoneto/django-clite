import click

from cli.utils import sanitized_string_callback
from cli.core.filesystem.files import File
from cli.core.templates.template import TemplateParser
from cli.decorators.scope import scoped, Scope


@scoped(to=Scope.APP)
@click.command()
@click.argument("name", required=True, callback=sanitized_string_callback)
@click.option(
    "--skip-import",
    is_flag=True,
    default=False,
    help="Do not import in __init__ module",
)
@click.pass_context
def validator(ctx, name, skip_import):
    """
    Generate a validator.
    """

    file = File(
        name=f"models/validators/{name}.py",
        template="models/validator.tpl",
        context={
            "name": name,
        },
    )

    file.create(
        import_statement=TemplateParser().parse_string(
            content="from .{{name}} import {{name}}_validator",
            variables={
                "module": name,
            },
        ),
        add_import_statement=not skip_import,
        **ctx.obj,
    )
