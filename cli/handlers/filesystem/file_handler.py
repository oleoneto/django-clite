import glob
import os
import fileinput
from pathlib import Path
from cli.utils.logger import Logger
from cli.utils.fs.utils import change_directory, make_directory
from cli.handlers.generic_handler import GenericHandler


class ContentDuplicationError(BaseException):
    pass


class FileHandler(GenericHandler):
    def __init__(self, cwd='.', dry=False, force=False, verbose=False, debug=False):
        super(FileHandler, self).__init__(cwd, dry, force, verbose, debug)
        self.__prompts = {'delete': 'Are you sure you want to delete this file?'}

    # File Manipulation

    def append_to_file(self, content, filename, prevent_duplication=False, **kwargs):
        message = f"Append to file [b]{filename}"

        dry = kwargs.get('dry', self.dry)

        if dry:
            Logger.log(message, dry=dry)
            return self.messages['append_skipped']

        try:
            if prevent_duplication:
                for line in fileinput.input(filename):
                    if content in line:
                        raise ContentDuplicationError('Duplicate content found')

            with open(filename, mode='a') as file:
                file.write(content)
                file.write('\n')
        except FileNotFoundError:
            Logger.log(f"File {filename} does not exist.")
            return self.errors['file_does_not_exist']
        except ContentDuplicationError:
            Logger.log(f"Skipped appending due to content duplication", is_visible=kwargs.get('verbose', self.verbose))
            return self.messages['append_skipped']

        Logger.log(message, is_visible=kwargs.get('verbose', self.verbose))
        return self.messages['appended']

    # File Creation

    def create_file(self, content, filename, **kwargs):
        message = f"Create file [b]{filename}"

        dry = kwargs.get('dry', self.dry)

        if dry:
            Logger.log(message, dry=dry)
            return self.messages['create_skipped']

        try:
            with open(filename, mode='x') as file:
                file.write(content)
                file.write('\n')
        except FileExistsError:
            if kwargs.get('force', self.forceful):
                with open(filename, 'w') as file:
                    file.write(content)
                    file.write('\n')
                return self.messages['created']
            return self.errors['file_exists']

        Logger.log(message, is_visible=kwargs.get('verbose', self.verbose))
        return self.messages['created']

    # File destruction

    def remove_file(self, filename, path=None, **kwargs):
        message = f"Remove [b]{filename}"

        dry = kwargs.get('dry', self.dry)

        if dry:
            Logger.log(message, dry=dry)
            return self.messages['delete_skipped']

        # TODO: Handle forceful removal

        try:
            change_directory(path)
            os.remove(filename)
        except FileNotFoundError:
            Logger.log(f"File {filename} does not exist.")
            return self.errors['file_does_not_exist']

        Logger.log(message, is_visible=kwargs.get('verbose', self.verbose))
        return self.messages['deleted']

    # Directory creation

    def create_folder(self, folder, template_handler, **kwargs):
        make_directory(folder.name, **kwargs)
        change_directory(folder.name, **kwargs)

        # Process all template files
        for file in folder.files:
            content = template_handler.parsed_template(file.template, raw=file.raw)
            self.create_file(content, file.filename, **kwargs)

        # Recursively create sub-folders and their files
        for sub_folder in folder.children:
            self.create_folder(sub_folder, template_handler, **kwargs)

        change_directory('..', **kwargs)
        return True

    # Finder

    @classmethod
    def find_file(cls, path, filename):
        pathname = f"{path}/**/{filename}"
        files = glob.glob(pathname, recursive=True)
        filepath = files[0] if len(files) else None
        return filepath

    @classmethod
    def find_files(cls, path, patterns=[]):
        location = Path(path)
        files = [filepath for filepath in location.iterdir() if any(filepath.match(p) for p in patterns)]

        matches = dict()

        for match in files:
            matches[match.name] = match.absolute()

        return matches

    @classmethod
    def scoped_app_directory(cls, posixpath):
        if posixpath.name == 'apps.py':
            scoped_path = posixpath.with_name(posixpath.parent.stem)
        elif server_file:
            scoped_path = posixpath.parent

        return scoped_path

    @classmethod
    def scoped_project_directory(cls, posixpath):
        management_file = posixpath.name == 'manage.py'
        server_file = posixpath.name in ['wsgi.py', 'asgi.py']

        scoped_path = None

        if management_file:
            scoped_path = posixpath.with_name(posixpath.parent.stem)
        elif server_file:
            scoped_path = posixpath.parent

        return scoped_path
