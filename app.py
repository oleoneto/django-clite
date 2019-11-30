import click
from django_clite.commands import create
from django_clite.commands import destroy
from django_clite.commands import generate
from django_clite.commands import run
from django_clite.commands import inspect


__author__ = 'Leo Neto'


class AliasedGroup(click.Group):
    """
    Adds support for abbreviated commands
    """
    def get_command(self, ctx, cmd_name):
        rv = click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv
        matches = [x for x in self.list_commands(ctx)
                   if x.startswith(cmd_name)]
        if not matches:
            return None
        elif len(matches) == 1:
            return click.Group.get_command(self, ctx, matches[0])
        ctx.fail('Too many matches: %s' % ', '.join(sorted(matches)))


@click.command(cls=AliasedGroup)
@click.version_option()
@click.pass_context
def main(ctx):
    """
    django-clite: by Leo Neto

    A CLI to handle the creation and management of your Django projects.

    The CLI has some options about how your project should be structured in order for it to maximize the
    amount of automatic configuration it can provide you. Since Django itself adheres to configuration over
    convention, you are free to bypass conventions of the CLI if you so choose.
    """

    # Note for contributors:
    #
    # Commands should be added as sub-commands of the main click group.
    # This enables sub-command chaining. For example:
    #       Add `run` command to `main`:
    #
    #       main.add_command(run)
    #
    #       Then, run:
    #       django_clite run run-sub-command`

    ctx.ensure_object(dict)

    # Note for contributors:
    #
    # File system helper included in cli context.
    # Helper needs to be passed down to sub-commands.


main.add_command(create)
main.add_command(destroy)
main.add_command(generate)
main.add_command(run)
main.add_command(inspect)

if __name__ == '__main__':
    main()
