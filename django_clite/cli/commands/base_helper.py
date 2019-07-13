import click
import fileinput
import inflection
import os
<<<<<<< HEAD:django_clite/cli/commands/base_helper.py
from django_clite.cli import log_error, log_info
=======
from dj.cli import log_error, log_info
>>>>>>> cdd5ae1b06170474ce89ba48faaf0c847c938c34:dj/cli/commands/base_helper.py


DEFAULT_IMPORT_WARNING = "Module already imported. Skipping..."

DEFAULT_OVERRIDE_WARNING = "Module already exists. Override file?"

DEFAULT_NOUN_NUMBER_WARNING = "Tip: resource name should be singular."

DEFAULT_NOUN_NUMBER_OPTION = "Change resource name from {} to {}?"

DEFAULT_PARSED_CONTENT_LOG = """Filename: {}\nFilepath: {}\n\n---- Begin content ----\n{}\n---- End content ----"""

DEFAULT_DESTROY_LOG = """Will delete...\nFilename: {}\nFilepath: {}\n\nWill also remove imports in __init__.py"""


class BaseHelper(object):

    @classmethod
    def add_import(cls, **kwargs):
        content = None

        try:
            is_dry = kwargs['dry']
        except KeyError:
            is_dry = False

        if not is_dry:
            filename = '__init__.py'
            path = kwargs['path']
            template = kwargs['template']

            try:
                content = template.render(**kwargs)
            except Exception:
                raise EnvironmentError

            try:
                os.chdir(path)

                # Prevent duplicate imports
                for line in fileinput.input(filename):
                    if content in line:
                        log_error(DEFAULT_IMPORT_WARNING)
                        fileinput.close()
                        return
                fileinput.close()

                with open(filename, 'a') as file:
                    file.write(content)
                    file.write('\n')
                file.close()
            except FileNotFoundError:
                raise FileNotFoundError

        return content

    @classmethod
    def check_noun(cls, noun):
        """
        Checks whether a noun is plural or singular and gives
        the option to change the noun from plural to singular.
        """
        noun = noun.lower()

        if inflection.pluralize(noun) == noun:
            log_info(DEFAULT_NOUN_NUMBER_WARNING)
            singular = inflection.singularize(noun)

            if click.confirm(DEFAULT_NOUN_NUMBER_OPTION.format(noun, singular)):
                noun = singular
        return noun

    @classmethod
    def create(cls, **kwargs):
        raise NotImplementedError

    @classmethod
    def create_file(cls, path, filename, file_content):
        directory = os.getcwd()

        try:
            os.chdir(path)
        except FileNotFoundError:
            os.makedirs(path)
            os.chdir(path)

        try:
            with open(filename, 'x') as file:
                file.write(file_content)
                file.write('\n')
            file.close()
            os.chdir(directory)
        except FileExistsError:
            if click.confirm(DEFAULT_OVERRIDE_WARNING):
                with open(filename, 'w') as file:
                    file.write(file_content)
                    file.write('\n')
                file.close()
                os.chdir(directory)
                return
            raise click.Abort

    @classmethod
    def destroy(cls, path, filename, **kwargs):
        try:
            is_dry = kwargs['dry']
        except KeyError:
            is_dry = False

        if is_dry:
            kwargs['filename'] = filename
            click.echo(DEFAULT_DESTROY_LOG.format(filename, path))
            return False
        else:
            try:
                os.chdir(path)
                os.remove(filename)
            except FileNotFoundError:
                log_error("File does not exist.")
                return False
        return True

    @classmethod
    def find_management_file(cls, cwd):

        code = 0
        path = None

        levels = (
            ('manage.py', 1),    # <-- project
            ('settings.py', 2),  # <-- project/project
            ('wsgi.py', 2),      # <-- project/project
            ('apps.py', 3),      # <-- project/project/app
        )

        for filename, c in levels:
            if filename in os.listdir(cwd):
                code = c
                path = os.getcwd()

        if code == 1:
            path = f"{path}/{path.split('/')[-1]}"
        elif code == 3:
            path = f"{path.rsplit('/', 1)[0]}"
        return path

    @classmethod
    def log_dry(cls, **kwargs):
        """
        Responsible for logging commands to the console.
        Used when --dry flag is specified.
        """
        click.echo(DEFAULT_PARSED_CONTENT_LOG.format(
            kwargs['filename'],
            kwargs['path'],
            kwargs['content']
        ))

    @classmethod
    def noun_is_plural(cls, text):
        return inflection.pluralize(text) == text

    @classmethod
    def parse_template(cls, template, **kwargs):
        return template.render(**kwargs)

    @classmethod
    def parse_and_create(cls, **kwargs):
        content = cls.parse_template(**kwargs)

        try:
            is_dry = kwargs['dry']
        except KeyError:
            is_dry = False

        if is_dry:
            cls.log_dry(**kwargs, content=content)
        else:
            cls.create_file(
                path=kwargs['path'],
                filename=kwargs['filename'],
                file_content=content
            )

    @classmethod
    def remove_import(cls, **kwargs):
        try:
            is_dry = kwargs['dry']
        except KeyError:
            is_dry = False

        if not is_dry:
            filename = '__init__.py'

            path = kwargs['path']

            template = kwargs['template']

            try:
                content = template.render(**kwargs)
            except Exception:
                raise EnvironmentError

            try:
                os.chdir(path)

                # Find import line to delete
                s = open(filename).read()
                s = s.replace(content, '')
                f = open(filename, 'w')
                f.write(s)
                f.close()

                for line in fileinput.FileInput(filename, inplace=1):
                    if line.rstrip():
                        print(line, end='')

            except FileNotFoundError:
                raise click.Abort

    @classmethod
    def show_files(cls, path):
        os.listdir(path)
