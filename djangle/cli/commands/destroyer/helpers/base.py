import os
import fileinput
from djangle.cli import log_error, log_success


class DestroyHelper(object):

    @classmethod
    def destroy(cls, **kwargs):
        log_success("Remove import")
        # cls.remove_import(**kwargs)

        log_success("Delete type")
        # cls.delete(**kwargs)
    # end def

    @classmethod
    def remove_import(cls, **kwargs):
        init_file = '__init__.py'
        path = kwargs['path']
        name = kwargs['model']

        try:
            content = kwargs['template'].render(model=kwargs['model'])
        except Exception:
            log_error("Wrong arguments passed.")
            raise EnvironmentError

        try:
            os.chdir(path)

            for line in fileinput.input(init_file, inplace=True):
                if content not in line:
                    print(line, end='')
            fileinput.close()

        except FileNotFoundError:
            log_error(f"__init__ file not found.")
            raise FileNotFoundError
    # end def

    @classmethod
    def delete(cls, **kwargs):
        path = kwargs['path']
        name = kwargs['model']
        filename = f"{name.lower()}.py"

        try:
            os.chdir(path)
            os.remove(filename)
            log_success(f"Successfully removed {filename} for {name.capitalize()}")
        except FileNotFoundError:
            log_error(f"File {filename} for {name.capitalize()} type not found.")
    # end def
# end class
