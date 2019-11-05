"""
Base Interface for Run Command Helpers
"""


class BaseRunHelper(object):

    def run(self, **kwargs):
        return NotImplementedError
