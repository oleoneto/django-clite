import click
import os
import inflection


__author__ = 'Leo Neto'


COMMANDS_FOLDER = os.path.join(os.path.dirname(__file__), 'commands')


class DiscoverableGroup(click.MultiCommand):
    def list_commands(self, ctx):
        rv = []

        commands = {
            command_path.rsplit('/', 1)[-1]: command_path  # command_name: command_path
            for command_path, _, files in os.walk(COMMANDS_FOLDER) if 'main.py' in files
        }

        """
        Only include top-level commands.
        That is, if we find a directory structure like so:
            commands/read/main.py
            commands/read/file/main.py
            commands/read/url/main.py

        We will only add `read` as a command and expect `file` and `url`
        to have been added as sub-commands of `read` already.
        """

        for func, path in commands.items():

            # Skip packages beginning or ending in underscores (_)
            command = path.split('commands/')[-1].split('/')[0]
            if command not in rv and not (command.startswith('_') or command.endswith('_')):
                # print(func)
                rv.append(func)

        rv.sort()
        return rv

    def get_command(self, ctx, name):
        ns = {}
        fn = os.path.join(COMMANDS_FOLDER, name, 'main.py')

        try:
            with open(fn) as f:
                code = compile(f.read(), fn, 'exec')
                eval(code, ns, ns)
        except FileNotFoundError:
            # Fail gracefully if command is not found or fails to load
            pass

        try:
            return ns[name]
        except KeyError:
            # Fail gracefully if command is not found or fails to load
            pass


@click.command(cls=DiscoverableGroup)
@click.option('--dry', is_flag=True, help="Display output without creating files.")
@click.option('--force', is_flag=True, help="Override any conflicting files.")
@click.option('--verbose', is_flag=True, help="Run in verbose mode.")
@click.version_option()
@click.pass_context
def cli(ctx, dry, force, verbose):
    """
    django-clite: by Leo Neto

    A CLI to handle the creation and management of your Django projects.

    The CLI has some options about how your project should be structured in order for it to maximize the
    amount of automatic configuration it can provide you. Since Django itself adheres to configuration over
    convention, you are free to bypass conventions of the CLI if you so choose.
    """

    # Note for contributors:
    #
    #

    ctx.ensure_object(dict)

    ctx.obj['dry'] = dry
    ctx.obj['force'] = force
    ctx.obj['verbose'] = verbose

    # Note for contributors:
    #
    # File system helper included in cli context.
    # Helper needs to be passed down to sub-commands.


if __name__ == '__main__':
    cli()
