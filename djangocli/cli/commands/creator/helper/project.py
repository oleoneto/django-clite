import click
import os


class BaseHelper(object):

    def create(self, *args, **kwargs):
        raise NotImplementedError
    # end def

    def create_file(self, path, filename, file_content):
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
            if click.prompt(f"Override existing {filename} file?"):
                with open(filename, 'w') as file:
                    file.write(file_content)
                    file.write('\n')
                file.close()
                os.chdir(directory)
                return
            raise FileExistsError
    # end def

    def create_from_template(self, template, **kwargs):
        return template.render(**kwargs)
    # end
# end
