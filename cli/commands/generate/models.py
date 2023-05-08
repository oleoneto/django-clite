import click
import logging
import inflection
from cli.utils import sanitized_string_callback
from cli.core.filesystem import File
from cli.constants import FILE_SYSTEM_HANDLER_KEY
from cli.logger import logger


@click.command()
@click.argument("name", required=True, callback=sanitized_string_callback)
@click.argument(
    "fields", nargs=1, required=False, callback=lambda x, y, z: x
)  # TODO: fields_callback
@click.option("-a", "--abstract", is_flag=True, help="Creates an abstract model type")
@click.option("--api", is_flag=True, help="Adds only related api resources")
@click.option("--full", is_flag=True, help="Adds all related resources")
@click.option("--admin", is_flag=True, help="Register admin model")
@click.option("--fixtures", is_flag=True, help="Create model fixture")
@click.option("--form", is_flag=True, help="Create model form")
@click.option("--serializers", is_flag=True, help="Create serializers")
@click.option("--templates", is_flag=True, help="Create templates")
@click.option("--tests", is_flag=True, help="Create tests")
@click.option("--views", is_flag=True, help="Create views")
@click.option("--viewsets", is_flag=True, help="Create viewsets")
@click.pass_context
def model(
    ctx,
    name,
    fields,
    abstract,
    api,
    full,
    admin,
    fixtures,
    form,
    serializers,
    templates,
    tests,
    views,
    viewsets,
):
    """
    Generates a model under the models directory.
    One can specify multiple attributes after the model's name, like so:

        django-clite g model track int:number char:title fk:album bool:is_favorite

    This will generate a Track model and add a foreign key of Album.
    If the model is to be added to admin.site one can optionally opt in by specifying the --register-admin flag.
    """

    if api and full:
        logger.error("Flags --api and --full cannot be used simultaneously.")
        raise click.Abort

    handler = ctx.obj[FILE_SYSTEM_HANDLER_KEY]

    imports = []

    file = File(
        path=f"models/{name}.py",
        template="models/model.tpl",
        content=None,
        context={
            "api": api,
            "abstract": abstract,
            "fields": fields,
            "imports": imports,
            "classname": inflection.camelize(name),
        },
    )

    # TODO: TemplateHandler
