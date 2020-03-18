# helpers:file_system
import os
import inflection
import fileinput
import subprocess
from .parser import sanitized_string
from .templates import rendered_file_template
from django_clite.helpers.finders import get_app_name
from django_clite.helpers.finders import get_project_name
from django_clite.helpers.finders import walk_up
from .logger import *


PREVIOUS_WORKING_DIRECTORY = '..'


class FSHelper(object):
    """
    FS, File System Helper

    Use this helper to handle all things related to
    searching, creating, and deleting files.
    """

    def __init__(self, cwd, dry=False, force=False, default=False, verbose=False):
        """
        :param cwd: current working directory
        :param dry: specifies if file system should be changed
        :param force: specifies if files should be overridden
        """

        self.__dry = dry
        self.__force = force
        self.__project_name = None
        self.__cwd = cwd
        self.__default = default
        self.__verbose = verbose
        self.__project_directory = None
        self.__path_to_management_file = None
        self.__management_file = None
        self.__app = get_app_name(verbose=verbose)

        self.__settings_file = self.find_settings_file()

        self.find_project_files()

        os.chdir(self.__cwd)

    def check_noun(self, noun):
        """
        Checks whether a noun is plural or singular and gives
        the option to change the noun from plural to singular.
        """
        noun = noun.lower()

        if inflection.pluralize(noun) == noun:
            log_standard(DEFAULT_NOUN_NUMBER_WARNING)
            singular = inflection.singularize(noun)

            if click.confirm(
                    DEFAULT_NOUN_NUMBER_OPTION.format(noun, singular)
            ):
                noun = singular
        return noun

    ##################################
    # Class properties

    @property
    def app_name(self):
        return self.__app

    @property
    def directory(self):
        return self.__project_directory

    @property
    def management_file(self):
        return self.__management_file \
            if self.__management_file \
            else self.find_project_files()[-1]

    @property
    def settings_file(self):
        return self.__settings_file

    @property
    def is_dry(self):
        return self.__dry

    @property
    def is_force(self):
        return self.__force

    def get_cwd(self):
        return self.__cwd

    def set_cwd(self, path):
        self.__cwd = path

    def get_project(self):
        return self.__project_name \
            if self.__project_name \
            else get_project_name(
                management_file=self.management_file,
                find_first=True
            )

    def set_project(self, name):
        self.__project_name = name

    def get_verbose(self):
        return self.__verbose

    def set_verbose(self, verbose):
        self.__verbose = verbose

    cwd = property(fget=get_cwd, fset=set_cwd)

    project_name = property(fget=get_project, fset=set_project)

    verbose = property(fget=get_verbose, fset=set_verbose)

    ##################################
    # Writing to the file system

    def default_create(self, model, context, **kwargs):

        model = self.check_noun(model)
        model = sanitized_string(model)
        classname = inflection.camelize(model)
        context['classname'] = classname

        filename = f"{model.lower()}.py"

        template = kwargs.get('template')
        template_import = kwargs.get('template_import')
        templates_directory = kwargs.get('templates_directory')

        content = rendered_file_template(
            path=templates_directory,
            template=template,
            context=context
        )

        import_content = rendered_file_template(
            path=templates_directory,
            template=template_import,
            context=context
        )

        self.add_import(
            template=template_import,
            content=import_content
        )

        self.create_file(
            path=self.cwd,
            filename=filename,
            content=content
        )

        scope = kwargs.get('scope') if kwargs.get('scope') else ''
        resource = f"{classname}{scope}"
        log_success(DEFAULT_CREATE_MESSAGE.format(filename, resource))

    def create_package(self, project, package, **kwargs):
        """
        Create a package and any associated modules
        :param project: name of the project this package belongs to
        :param package: name of the package to be created
        :return: True if package is created. False otherwise
        """

        project = sanitized_string(project)
        package = sanitized_string(package)

        content = f'# {project}:{kwargs.get("app")}:{package}'

        os.mkdir(package)
        os.chdir(package)

        _ = self.create_file(
            path=os.getcwd(),
            filename='__init__.py',
            content=content
        )

        if self.__verbose:
            log_info(f"Created package {package} at {os.getcwd()}")

        os.chdir(PREVIOUS_WORKING_DIRECTORY)
        return _

    def create_file(self, content, filename, path=None):
        """
        :param content: content for created file
        :param filename: name for created file
        :param path: location of created file
        :return: True if file is created. False otherwise
        """

        if self.is_dry:
            self.__log_dry(
                path=path,
                filename=filename,
                content=content
            )
            return False

        path = path if path else self.__cwd

        try:
            os.chdir(path)
        except FileNotFoundError:
            os.makedirs(path)
            os.chdir(path)

        try:
            with open(filename, 'x') as file:
                file.write(content)
                file.write('\n')
            file.close()
            os.chdir(path)
        except FileExistsError:
            if self.__force or click.confirm(DEFAULT_OVERRIDE_WARNING.format(filename)):
                with open(filename, 'w') as file:
                    file.write(content)
                    file.write('\n')
                file.close()
                os.chdir(path)
            return False

        if self.verbose:
            log_info(f"Created {filename} at {path}")

        return True

    def destroy_file(self, filename, path=None):
        """
        :param filename: name of file to be destroyed
        :param path: location of file to be destroyed
        :return: True if file is created. False otherwise
        """

        path = path if path else self.__cwd

        if self.is_dry:
            click.echo(DEFAULT_DESTROY_LOG.format(filename, path))
            return False
        else:
            try:
                os.chdir(path)
                os.remove(filename)
            except FileNotFoundError:
                log_error(f"File {filename} does not exist.")
                return False

        if self.verbose:
            log_info(f"Removed {filename} from {path}")

        return True

    def default_destroy_file(self, model, **kwargs):

        if not self.__dry and not self.__force:
            click.confirm('Are you sure you want to delete this file?', abort=True)

        filename = f'{model}.py'
        classname = inflection.camelize(model)

        try:
            # Optional import removal
            content = rendered_file_template(
                path=kwargs.get('templates_directory'),
                template=kwargs.get('template_import'),
                context={
                    'classname': classname,
                    'model': model
                }
            )

            self.remove_import(content=content)
        except AttributeError or ValueError:
            pass

        return self.destroy_file(
            filename=filename,
            path=self.__cwd
        )

    def add_import(self, content, path=None, **kwargs):
        """
        :param content: content for import statement
        :param path: path to __init__ file
        :param kwargs:
        :return: template content
        """

        filename = '__init__.py'

        path = path if path else self.__cwd

        if self.is_dry:
            self.__log_dry(
                path=path,
                filename=filename,
                content=content,
            )
            return content
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
            with open(filename, 'w') as file:
                file.write(content)
                file.write('\n')

        if self.verbose:
            log_info(f"Added: {content} to {path}/{filename}")

        return content

    def remove_import(self, content, path=None, **kwargs):
        """
        :param content: content for import statement
        :param path: path to __init__ file
        :param kwargs:
        :return: template content
        """

        filename = '__init__.py'

        path = path if path else self.__cwd

        if not self.is_dry:
            try:
                os.chdir(path)

                # Find import line to remove
                s = open(filename).read()
                s = s.replace(content, '')
                f = open(filename, 'w')
                f.write(s)
                f.close()

                for line in fileinput.FileInput(filename, inplace=1):
                    if line.rstrip():
                        print(line, end='')

                if self.verbose:
                    log_info(f"Removed: {content} from {path}/{filename}")

            except FileNotFoundError:
                raise click.Abort

    def parse_templates(self, parings, names, directory, folders=None, **kwargs):
        """
        :param parings: mapping of file and template names
        :param names: names of templates to be parsed
        :param directory: template files directory
        :param folders: project folders to create
        :param kwargs: context and other arguments
        :return: True if templates are parsed
        """

        if folders is not None:
            for folder in folders:
                try:
                    os.makedirs(folder)
                except FileExistsError:
                    log_error(f"Directory {folder} already exists")

        for file, template in parings.items():
            i = names.index(template)
            template = names[i]

            content = rendered_file_template(
                path=directory,
                template=template,
                context=kwargs.get('context')
            )

            self.create_file(
                path=os.getcwd(),
                filename=file,
                content=content,
            )

            if self.verbose:
                log_info(f"Created file {file} from {template}")

        return True

    def create_repository(self):
        if not self.is_dry:
            subprocess.check_output(['git', 'init'])
            subprocess.check_output(['git', 'add', '--all'])
            subprocess.check_output(['git', 'commit', '-m', 'Initial commit'])
            log_success('Successfully initialized git repository')
            return True
        log_success("Skipping creation of git repository")
        return False

    ##################################
    # Locate files

    def find_project_files(self, path=None):
        """
        Searches the set working directory for any of 4 key Django
        files to determine from where a command is being run:

            manage.py, settings.py, wsgi.py, and apps.py

        This is used to ensure commands that create or delete resources
        are always run in the correct directory and within a Django project.
        """

        current_dir = path if path else self.__cwd

        code = 0
        path = None

        levels = (
            ('manage.py', 1),  # <-- project
            ('settings.py', 2),  # <-- project/project
            ('wsgi.py', 2),  # <-- project/project
            ('apps.py', 3),  # <-- project/project/app
        )

        for filename, c in levels:
            try:
                if filename in os.listdir(current_dir):
                    code = c
                    path = current_dir
            except FileNotFoundError:
                log_error(f'{current_dir} does not exist.')

        if code == 1:
            self.__project_directory = path
            self.__management_file = os.path.join(
                self.__project_directory, 'manage.py'
            )

        elif code == 2 or code == 3:
            for c, d, f in walk_up('.'):
                if 'manage.py' in f:
                    self.__project_directory = c
                    self.__management_file = os.path.join(
                        self.__project_directory, 'manage.py'
                    )
                    break

        return path, self.__project_directory, self.__management_file

    def find_settings_file(self):
        """
        Finds settings.py file
        :return: file or None
        """
        settings = os.path.join(self.__cwd, 'settings.py')
        if not os.path.exists(settings):
            return None
        return settings

    def list_project_directory(self):
        for f in os.listdir(self.__cwd):
            log_standard(f)

    ##################################
    # Logging

    def __log_dry(self, content, filename, path=None):
        """
        Responsible for logging commands to stdout.
        Used when --dry flag is specified.
        """

        path = path if path else self.__cwd

        log_verbose(
            header=f'{path}{filename}',
            message=content,
        )

        # click.echo(DEFAULT_PARSED_CONTENT_LOG.format(
        #     filename,
        #     path,
        #     content
        # ))

    ##################################

    def __str__(self):
        return 'FileSystemHelper'

    ##################################
