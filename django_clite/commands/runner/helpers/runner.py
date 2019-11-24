from django_clite.helpers import FSHelper


class RunnerHelper(FSHelper):
    """
    Base Interface for Run Command Helpers
    """

    def run(self, **kwargs):
        return NotImplementedError
