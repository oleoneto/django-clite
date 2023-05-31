import click
import inflection

from cli.utils import sanitized_string_callback
from cli.core.filesystem.filesystem import File, FileSystem
from cli.core.templates.template import TemplateParser
from cli.decorators.scope import scoped, Scope

from .template import template


SUPPORTED_CLASSES = [
    "create",
    "detail",
    "list",
    "update",
]


@scoped(to=Scope.APP)
@click.command()
@click.argument("name", required=True, callback=sanitized_string_callback)
@click.option("--klass", type=click.Choice(SUPPORTED_CLASSES))
@click.option("--full", is_flag=True, help="Create all CRUD views")
@click.option(
    "--skip-templates",
    is_flag=True,
    default=False,
    help="Skip generation of related templates.",
)
@click.option(
    "--skip-import",
    is_flag=True,
    default=False,
    help="Do not import in __init__ module",
)
@click.pass_context
def view(ctx, name, klass, full, skip_templates, skip_import):
    """
    Generate a view function or class.
    """

    klasses = SUPPORTED_CLASSES if full else [klass]

    for k in klasses:
        file = File(
            path=f"views/{name}{'_' + k if k else ''}.py",
            template=f"views/{k if k else 'view'}.tpl",
            context={
                "name": name,
                "classname": inflection.camelize(name),
                "namespace": inflection.pluralize(name),
                "template_name": f"{name}{'_' + k if k else ''}.hml",
            },
        )

        FileSystem().create_file(
            file=file,
            content=TemplateParser().parse_file(
                filepath=file.template,
                variables=file.context,
            ),
            import_statement=TemplateParser().parse_string(
                content="from .{{name}} import {{classname}}",
                variables={
                    "name": f"{name}{'_' + k if k else ''}",
                    "classname": f"{inflection.camelize(name)+inflection.camelize(k)+'View' if k else name}",
                },
            ),
            add_import_statement=not skip_import,
        )

        if not skip_templates:
            ctx.invoke(template, name=name, klass=k)
