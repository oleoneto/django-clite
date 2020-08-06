import os
import inflection
from cli.helpers import sanitized_string
from cli.decorators import watch_templates
from cli.helpers.fs import FSHelper, ensure_directory


BASE_DIR = os.path.dirname(os.path.abspath(__file__)).rsplit('/', 1)[0]


@watch_templates(os.path.join(BASE_DIR, 'templates'))
class Generator(FSHelper):

    def __init__(self, cwd, dry=False, force=False, default=False, verbose=False, requires=[]):
        ensure_directory(cwd)
        [ensure_directory(self.cwd, d) for d in requires]
        super(Generator, self).__init__(cwd, dry, force, default, verbose)

    def create(self, model, **kwargs):
        pass

    def delete(self, model, **kwargs):
        pass
