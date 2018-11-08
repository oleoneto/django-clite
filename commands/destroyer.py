import click


@click.group()
@click.option('--resource', help="Resource to be destroyed")
@click.option('--dry-run', is_flag=True, help="Show output but DO NOT run.")
def destroy(resource, dry_run):
    """
    Model, route, and template destroyer
    """
    proceed = click.confirm("Are you sure you want to destroy the resource?", show_default=True, default=False)


@destroy.command()
def model():
    """
    Destroys a model and removes it from admin site
    """
    pass


@destroy.command()
def route():
    """
    Destroys the route and its template file
    """
    pass


@destroy.command()
def viewset():
    """
    Destroys the viewset for a serializable model
    """
    pass
