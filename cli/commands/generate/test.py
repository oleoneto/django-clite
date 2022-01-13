import inflection
import click
from cli.commands.generate.helpers import resource_generator
from cli.handlers.filesystem.template_handler import TestTemplateHandler


SUPPORTED_SCOPES = ['model', 'viewset']


@click.command()
@click.argument("name", required=True)
@click.option("-s", "--scope", type=click.Choice(SUPPORTED_SCOPES), required=True)
@click.option('--full', is_flag=True, help='Create templates for all CRUD operations')
@click.pass_context
def test(ctx, name, scope, full):
    """
    Generates a new TestCase.
    """

    def generate_test(n, s):
        resource_generator(
            n,
            parent='tests',
            package=inflection.pluralize(s),
            scope='TestCase',
            template=f"{inflection.singularize(s)}.tpl",
            template_handler=TestTemplateHandler,
            **ctx.obj,
        )

    if full:
        [generate_test(name, t) for t in SUPPORTED_SCOPES]
    else:
        generate_test(name, scope)
