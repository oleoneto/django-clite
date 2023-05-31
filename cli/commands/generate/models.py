import click
import inflection

from cli.utils import sanitized_string_callback, fields_callback
from cli.core.filesystem.filesystem import File, FileSystem
from cli.core.templates.template import TemplateParser
from cli.decorators.scope import scoped, Scope
from cli.core.logger import Logger


@scoped(to=Scope.APP)
@click.command()
@click.argument("name", required=True, callback=sanitized_string_callback)
@click.argument("fields", nargs=-1, required=False, callback=fields_callback)
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
@click.option(
    "--skip-import",
    is_flag=True,
    default=False,
    help="Do not import in __init__ module",
)
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
    skip_import,
):
    """
    Generates a model under the models directory.
    One can specify multiple attributes after the model's name, like so:

        django-clite g model track int:number char:title fk:album bool:is_favorite

    This will generate a Track model and add a foreign key of Album.
    If the model is to be added to admin.site one can optionally opt in by specifying the --register-admin flag.
    """

    if api and full:
        Logger().print("Flags --api and --full cannot be used simultaneously.")
        raise click.Abort()

    model_fields, model_imports = fields

    file = File(
        path=f"models/{name}.py",
        template="models/model.tpl",
        context={
            "api": api,
            "abstract": abstract,
            "classname": inflection.camelize(name),
            "fields": model_fields,
            "imports": model_imports,
            "name": name,
            "table_name": f"{TemplateParser().app}.{inflection.pluralize(name)}",
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
                "name": name,
                "classname": inflection.camelize(name),
            },
        ),
        add_import_statement=not skip_import,
    )

    def generate_related_resources():
        if admin or api or full:
            from .admin import admin as cmd

            ctx.invoke(cmd, name=name, fields=fields, skip_import=skip_import)

        if fixtures or api or full:
            from .fixtures import fixture as cmd

            ctx.invoke(cmd, model=name, fields=fields)

        if form or full:
            from .forms import form as cmd

            ctx.invoke(cmd, name=name, skip_import=skip_import)

        if serializers or api or full:
            from .serializers import serializer as cmd

            ctx.invoke(cmd, name=name, skip_import=skip_import)

        if views or full:
            from .views import view as cmd

            ctx.invoke(cmd, name=name, full=full, skip_import=skip_import)

        if viewsets or api or full:
            from .viewsets import viewset as cmd

            ctx.invoke(cmd, name=name, skip_import=skip_import)

    generate_related_resources()
