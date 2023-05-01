import subprocess
from cli.logger import logger
from cli.handlers.generic_handler import GenericHandler


class GitHandler(GenericHandler):
    @classmethod
    def initialize(cls, origin=None, **kwargs):
        dry = kwargs.get('dry', cls.dry)
        verbose = kwargs.get('verbose', cls.verbose)

        if dry:
            logger.log("Skipping initialization of repository", is_visible=verbose)
            return False

        try:
            subprocess.check_output(['git', 'init'])
            subprocess.check_output(['git', 'add', '--all'])
            subprocess.check_output(['git', 'commit', '-m', 'Initial commit'])
            logger.log('Successfully initialized git repository')
            return True
        except subprocess.CalledProcessError as error:
            logger.log(repr(error))

        if origin:
            try:
                subprocess.check_output(['git', 'remote', 'add', 'origin', origin])
                logger.log(f'Successfully added origin {origin}', is_visible=cls.verbose)
            except subprocess.CalledProcessError as error:
                logger.log(repr(error))

        return True
