import click
import os
from cli import COMMANDS_FOLDER, PLUGINS_FOLDER


def run_command(command, ns):
    with open(command) as f:
        code = compile(f.read(), command, 'exec')
        eval(code, ns, ns)


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

    COMMAND_PATHS = [COMMANDS_FOLDER]

    def __get_commands(self):
        commands = {}

        if PLUGINS_FOLDER is not None:
            self.COMMAND_PATHS.append(PLUGINS_FOLDER)

        # Core commands + plugins
        for path in self.COMMAND_PATHS:
            c = {
                command_path.rsplit('/', 1)[-1]: command_path  # command_name: command_path
                for command_path, _, files in os.walk(path) if 'main.py' in files
            }

            commands.update(c)

        return commands

    def list_commands(self, ctx):
        rv = []

        commands = self.__get_commands()

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
            command = path.split('/')[-1]
            if command not in rv and not (command.startswith('_') or command.endswith('_')):
                rv.append(func)

        rv.sort()
        return rv

    def get_command(self, ctx, name):
        ns = {}
        fn = os.path.join(COMMANDS_FOLDER, name, 'main.py')

        try:
            run_command(fn, ns)
        except FileNotFoundError:
            try:
                pfn = os.path.join(PLUGINS_FOLDER, name, 'main.py')
                run_command(pfn, ns)
            except FileNotFoundError or TypeError:
                pass

        try:
            return ns[name]
        except KeyError:
            # Fail gracefully if command is not found or fails to load
            pass
