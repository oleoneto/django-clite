# cli:decorators:scope
import os
import click
import functools
from enum import Enum
from pathlib import Path

from cli.utils import core_project_files, project_and_app_names
from cli.core.filesystem.finder import Finder
from cli.core.filesystem.filesystem import FileSystem


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
        )

        django_files = core_project_files()

        # NOTE: Handle forcefull creation
        force = ctx.params.get("force", False)
        parent = ctx.parent
        while parent is not None:
            force = parent.params.get("force", False)
            parent = parent.parent

        # 1. Probably not a django project directory
        if not force and len(django_files) == 0:
            return noop_cmd
        # 2. No django app detected
        elif not force and (to == Scope.APP and not django_files.get("apps.py", None)):
            return noop_cmd
        # 3. No django project detected
        elif not force and (
            to == Scope.PROJECT
            and 1
            > len(
                [django_files.get(x, None) for x in ["asgi.py", "manage.py", "wsgi.py"]]
            )
        ):
            return noop_cmd

        return cmd

    return decorator
