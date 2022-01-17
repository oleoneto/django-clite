import click
from cli.commands.generate.helpers import resource_generator


@click.command()
@click.argument('name')
@click.argument("fields", nargs=-1, required=False)
@click.option('-n', '--number', default=1, help='Number of objects to create in fixture.')
@click.pass_context
def fixture(ctx, name, fields, number):
    """
    Generates model fixtures.
    """

    # TODO: Parse fixture fields

    # parsed_fields = FSHelper()

    resource_generator(
        name,
        template='fixture.tpl',
        package='fixtures',
        context={'total': number, 'fields': fields},
        file_extension='.json',
        no_append=True,
        **ctx.obj
    )
