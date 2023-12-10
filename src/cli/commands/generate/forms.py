import click
import inflection

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
def form(ctx, name, skip_import):
    """
    Generate a form.
    """

    file = File(
        name=f"forms/{name}.py",
        template="form.tpl",
        context={
            "name": name,
            "classname": inflection.camelize(name),
        },
    )

    file.create(
        import_statement=TemplateParser().parse_string(
            content="from .{{name}} import {{classname}}Form",
            variables={
                "name": name,
                "classname": inflection.camelize(name),
            },
        ),
        add_import_statement=not skip_import,
        **ctx.obj,
    )
