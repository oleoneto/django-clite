import click
import os
from cli import COMMANDS_FOLDER


class DiscoverableGroup(click.MultiCommand):
    """
    Adds support for auto-discoverable commands/plugins
    """

    # Commands are auto-discovered if they are placed under the COMMAND_FOLDER.
    #
    # But please be sure to do the following for this to work:
    #   1. Name your package and click command the same.
    #   2. Place your command definition within your package's main.py module
    #   3. Any sub-commands of your command should be added to the top-most command in the package's main.py module.
    #
    #   If you would like to skip a plugin/command from being auto-discovered,
    #   simply rename the package by either prepending or appending any number of underscores (_).
    #   Any code contained within the package will be ignored.

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
