import click
from cli.helpers.templates import rendered_file_template


@click.group()
@click.argument('args', nargs=-1, required=False)
@click.pass_context
def parse(ctx, args):
    """Parses a given template with the specified arguments."""


@parse.command(name='jinja')
@click.argument('template')
@click.pass_context
def parse_jinja_template(ctx, template):
    pass
