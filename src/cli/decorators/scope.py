# cli:decorators:scope
import click
from enum import Enum

from cli.core.filesystem.finder import core_project_files


class Scope(Enum):
    APP = "app"
    PROJECT = "project"


def scoped(to: Scope):
    class NoOpCommand(click.Command):
        def invoke(self, ctx):
            click.echo(
                f"Command {self.name} has '{to.value}' scope but the {to.value} was not detected"
            )
            raise click.Abort()

    @click.pass_context
    def decorator(ctx, cmd: click.Command):
        noop_cmd = NoOpCommand(
            name=cmd.name,
            params=cmd.params,
            context_settings=cmd.context_settings,
            hidden=cmd.hidden,
            callback=cmd.callback,
            help=cmd.help,
            add_help_option=cmd.add_help_option,
            deprecated=cmd.deprecated,
            epilog=cmd.epilog,
            no_args_is_help=cmd.no_args_is_help,
            options_metavar=cmd.options_metavar,
            short_help=cmd.short_help,
        )

        django_files = core_project_files()

        # NOTE: Handle forceful creation
        force = ctx.params.get("force", False)
        parent = ctx.parent
        while parent is not None:
            force = parent.params.get("force", False)
            parent = parent.parent

        if not force:
            # 1. Probably not inside a django project directory
            if len(django_files) == 0:
                return noop_cmd

            # 2. Possibly inside a django project, but no app detected
            elif to == Scope.APP and not django_files.get("apps.py", None):
                return noop_cmd

            # 3. No django project detected
            elif to == Scope.PROJECT and 1 > len(
                [django_files.get(x, None) for x in ["manage.py", "wsgi.py", "asgi.py"]]
            ):
                return noop_cmd

        return cmd

    return decorator
