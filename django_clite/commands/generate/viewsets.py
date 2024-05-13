import click
import pathlib
import inflection

from geny.core.filesystem.files import File
from geny.core.filesystem.transformations import AddLineToFile, TouchFile
from django_clite.decorators.scope import scoped, Scope
from django_clite.commands import command_defaults
from django_clite.commands.callbacks import sanitized_string_callback


@scoped(to=Scope.APP)
@click.command()
@click.argument("name", required=True, callback=sanitized_string_callback)
@click.option("--read-only", is_flag=True, help="Create a read-only viewset.")
@click.option("--full", is_flag=True, help="Create related files (i.e. TestCases)")
@click.option(
    "--skip-import",
    is_flag=True,
    default=False,
    help="Do not import in __init__ module",
)
@click.pass_context
def viewset(ctx, name, read_only, full, skip_import):
    """
    Generate a viewset for a serializable model.
    """

    file = File(
        name=f"viewsets/{name}.py",
        template="viewsets/viewset.tpl",
        context={
            "name": name,
            "module": name,
            "read_only": read_only,
            "namespace": inflection.pluralize(name),
            "classname": inflection.camelize(name),
        },
    )

    # TODO: Create router file
    # router = Directory(
    #     "router",
    #     children=[
    #         File(name="__init__.py", template="app/router_init.tpl"),
    #         File(name="api.py", template="app/router_api.tpl"),
    #         File(name="router.py", template="app/router.tpl"),
    #     ],
    # )
    #
    # router.create(**ctx.obj)

    after_hooks = [
        TouchFile('viewsets/__init__.py')
    ]

    if not skip_import:
        after_hooks.append(
            AddLineToFile(
                pathlib.Path('viewsets/__init__.py'),
                command_defaults.viewset(name),
                prevent_duplicates=True,
            )
        )

    file.create(after_hooks=after_hooks, **ctx.obj)

    if full:
        from .tests import test as cmd

        ctx.invoke(cmd, name=name, scope="viewset", skip_import=skip_import)
