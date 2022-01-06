import subprocess
from cli.utils.logger import Logger
from cli.handlers.generic_handler import GenericHandler


class GitHandler(GenericHandler):
    @classmethod
    def initialize(cls, origin=None, **kwargs):
        dry = kwargs.get('dry', cls.dry)
        verbose = kwargs.get('verbose', cls.verbose)

        if dry:
            Logger.log("Skipping initialization of repository", is_visible=verbose)
            return False

        try:
            subprocess.check_output(['git', 'init'])
            subprocess.check_output(['git', 'add', '--all'])
            subprocess.check_output(['git', 'commit', '-m', 'Initial commit'])
            Logger.log('Successfully initialized git repository')
            return True
        except subprocess.CalledProcessError as error:
            Logger.log(repr(error))

        if origin:
            try:
                subprocess.check_output(['git', 'remote', 'add', 'origin', origin])
                Logger.log(f'Successfully added origin {origin}', is_visible=cls.verbose)
            except subprocess.CalledProcessError as error:
                Logger.log(repr(error))

        return True
