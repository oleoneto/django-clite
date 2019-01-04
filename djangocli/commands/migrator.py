import click
from faker import Faker


@click.group()
def db():
    """
    Handles various database activities
    """
    pass


@db.command()
@click.option('--dry-run', is_flag=True, help="Show output but DO NOT run.")
def seed(dry_run):
    """
    Seeds database with mock data
    """
    data = Faker()
    # click.secho(data.last_name(), fg="green")
    pass


@db.command()
@click.option('--dry-run', is_flag=True, help="Show output but DO NOT run.")
def migrate(dry_run):
    """
    Makes and applies migrations to DB
    """
    pass


@db.command()
@click.option('--dry-run', is_flag=True, help="Show output but DO NOT run.")
def makemigrations(dry_run):
    """
    Generates migrations to be applied to DB
    """
    pass

