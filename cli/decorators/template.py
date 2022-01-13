import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__)).rsplit('/', 1)[0]


def watch_templates(scope=''):
	def wrapper(f):
		f.templates_directory = os.path.join(BASE_DIR, 'templates', scope)
		f.template_files = [f for f in os.listdir(f.templates_directory) if f.endswith('tpl')]
		return f
	return wrapper
