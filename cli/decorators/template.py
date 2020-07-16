import os


def watch_templates(directory):
	def wrapper(f):
		f.TEMPLATES_DIRECTORY = directory
		f.TEMPLATE_FILES = [f for f in os.listdir(directory) if f.endswith('tpl')]
		return f
	return wrapper
