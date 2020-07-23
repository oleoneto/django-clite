from cli.click import DiscoverableGroup


class AliasedAndDiscoverableGroup(DiscoverableGroup):
    """
    Combines support for abbreviated and auto-discoverable commands/plugins
    """

    def __get_command(self, ctx, cmd_name):
        return DiscoverableGroup.get_command(self, ctx, cmd_name)

    def get_command(self, ctx, cmd_name):
        matches = [x for x in self.list_commands(ctx) if x.startswith(cmd_name)]

        if not matches:
            return None
        elif len(matches) == 1:
            return self.__get_command(ctx, matches[0])
        ctx.fail('Too many matches: %s' % ', '.join(sorted(matches)))