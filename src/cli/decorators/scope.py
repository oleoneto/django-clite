# cli:decorators:scope
import os

import click
from enum import Enum

from geny.core.filesystem.finder import core_project_files


class Scope(Enum):
    APP = "app"
    PROJECT = "project"


def scoped(to: Scope):
    def decorator(cmd: click.Command):
        def allowed_to_continue() -> bool:
            django_files = core_project_files(os.getcwd())

            # TODO: Handle forceful creation

            # 1. Probably not inside a django project directory
            if len(django_files) == 0:
                return False

            # 2. Possibly inside a django project, but no app detected
            if to == Scope.APP and django_files.get("apps.py", None):
                return True

            # 3. No django project detected
            matched_project_files = [
                x
                for x in django_files.keys()
                if x in ["manage.py", "wsgi.py", "asgi.py"]
            ]
            if to == Scope.PROJECT and len(matched_project_files) > 0:
                return True

            return False

        class ScopedCommand(click.Command):
            def invoke(self, ctx):
                if allowed_to_continue():
                    super().invoke(ctx)
                    return

                click.echo(
                    f"Command {cmd.name} has '{to.value}' scope but the {to.value} was not detected",
                    err=True,
                )
                raise click.Abort()

        return ScopedCommand(
            add_help_option=cmd.add_help_option,
            callback=cmd.callback,
            context_settings=cmd.context_settings,
            deprecated=cmd.deprecated,
            epilog=cmd.epilog,
            help=cmd.help,
            hidden=cmd.hidden,
            name=cmd.name,
            no_args_is_help=cmd.no_args_is_help,
            options_metavar=cmd.options_metavar,
            params=cmd.params,
            short_help=cmd.short_help,
        )

    return decorator
