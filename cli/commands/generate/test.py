import click
import inflection
from cli.commands.generate.helpers import resource_generator
from cli.handlers.filesystem.template_handler import TestTemplateHandler


SUPPORTED_SCOPES = ['model', 'viewset']


@click.command()
@click.argument('name', required=True)
@click.option('-s', '--scope', type=click.Choice(SUPPORTED_SCOPES), required=True)
@click.option('--full', is_flag=True, help=f'Create tests for {SUPPORTED_SCOPES}')
@click.pass_context
def test(ctx, name, scope, full):
    """
    Generates new TestCases.
    """

    def generate(n, s):
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
        [generate(name, s) for s in SUPPORTED_SCOPES]
    else:
        generate(name, scope)
