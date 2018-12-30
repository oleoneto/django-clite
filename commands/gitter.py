import os
import click


class Git(click.MultiCommand):

    def init(self, ctx):
        click.echo("Initialized")
        pass

    def clone(self, ctx):
        click.echo("cloned")
        pass


git = Git(help="Git wrapper")
