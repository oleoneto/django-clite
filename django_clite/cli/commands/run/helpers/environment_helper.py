import re
from .base_run_helper import BaseRunHelper


class EnvironmentHelper(BaseRunHelper):

    @staticmethod
    def __read_environment(env_file):
        """
        Use this to read environment variables from a .env file

        Based on implementations found on the links below:
            https://gist.github.com/bennylope/2999704
            https://wellfire.co/learn/easier-12-factor-django/
        """

        try:
            with open(env_file) as f:
                content = f.read()
        except IOError:
            content = ''

        keys = {}

        for line in content.splitlines():
            first_match = re.match(r'\A([A-Za-z_0-9]+)=(.*)\Z', line)
            if first_match:
                key, value = first_match.group(1), first_match.group(2)
                second_match = re.match(r"\A'(.*)'\Z", value)
                if second_match:
                    value = second_match.group(1)
                third_match = re.match(r'\A"(.*)"\Z', value)
                if third_match:
                    value = re.sub(r'\\(.)', r'\1', third_match.group(1))
                keys[key] = value

        return keys

    def __copy_env(self, env_file, project_name=None, dokku=True):
        keys = self.__read_environment(env_file)

        options = ['.env-dokku', '.env-example']

        output = options[0] if dokku else options[1]

        with open(output, 'w') as file:
            for k, v in keys.items():
                if dokku:
                    v = v.split("#")[0]
                    if v not in ['False', 'True']:
                        v = f"'{v}'"
                    statement = f"dokku config:set --no-restart {project_name} {k}={v}\n"
                else:
                    statement = f'{k}=\n'
                file.write(statement)

    def copy_dokku(self, env_file, project_name):
        self.__copy_env(env_file, project_name)

    def copy_example(self, env_file):
        self.__copy_env(env_file, dokku=False)

    def run(self, **kwargs):
        project_name = kwargs['project_name']

        env_file = kwargs['filepath'] if kwargs['filepath'] else kwargs['path'] + '/.env'

        self.copy_example(env_file)
        self.copy_dokku(env_file, project_name)
