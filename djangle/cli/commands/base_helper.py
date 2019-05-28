import click
import os
import fileinput
from djangle.cli import log_error


class BaseHelper(object):

    @classmethod
    def show_files(cls, path):
        # TODO: Implement show_files()
        # List all files in the current directory
        os.listdir(path)
    # end def

    @classmethod
    def create(cls, *args, **kwargs):
        raise NotImplementedError
    # end def

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

            can_override = click.confirm(f"Override existing {filename} file?")
            if can_override:
                with open(filename, 'w') as file:
                    file.write(file_content)
                    file.write('\n')
                file.close()
                os.chdir(directory)
                return
            raise FileExistsError
    # end def

    @classmethod
    def parse_template(cls, template, **kwargs):
        return template.render(**kwargs)
    # end def

    @classmethod
    def add_import(cls, **kwargs):
        try:
            content = kwargs['template'].render(model=kwargs['model'])
        except Exception:
            raise EnvironmentError

        try:
            os.chdir(kwargs['path'])

            # Prevents duplicate imports
            for line in fileinput.input('__init__.py'):
                if content in line:
                    log_error("Module already imported. Skipping...")
                    fileinput.close()
                    return
            fileinput.close()

            with open('__init__.py', 'a') as file:
                file.write(content)
                file.write('\n')
            file.close()
        except FileNotFoundError:
            raise FileNotFoundError
        return content
    # end def
