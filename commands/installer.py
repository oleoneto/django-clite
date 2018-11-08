import click


@click.group()
@click.pass_context
@click.argument('requirement')
def install(ctx, requirement):
    """
    Installs and updates requirements
    """
    pass


@install.command()
@click.argument('reqs', required=False)
def requirements(reqs):
    """
    Attempts to install all requirements
    """
    pass
