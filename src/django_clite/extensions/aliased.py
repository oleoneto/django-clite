from click import Group


class AliasedGroup(Group):
    """
    Adds support for abbreviated commands
    """

    def get_command(self, ctx, cmd_name):
        rv = Group.get_command(self, ctx, cmd_name)

        if rv is not None:
            return rv

        matches = [
            match for match in self.list_commands(ctx) if match.startswith(cmd_name)
        ]

        if not matches:
            return None

        if len(matches) != 1:
            raise ctx.fail("Too many matches: %s" % ", ".join(sorted(matches)))

        return Group.get_command(self, ctx, matches[0])
