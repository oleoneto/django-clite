import click


def log_info(message):
    click.secho(message, fg='yellow')


def log_success(message):
    click.secho(message, fg='green')


def log_error(message):
    click.secho(message, fg='red')


def file_created(filename=''):
    log_success("Successfully created %s" % filename)


def file_exists(filename=''):
    log_error("File already exists %s" % filename)


class AliasedGroup(click.Group):
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
