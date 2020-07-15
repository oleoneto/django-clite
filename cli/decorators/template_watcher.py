# Add logic here to allow template watchers to automatically get
# TEMPLATES and TEMPLATES_DIR properties
from functools import wraps


def is_template_watcher(function):

	@wraps(function)
	def wrapper():
		function.__TEMPLATES_DIR = ''
		return function
	return wrapper
