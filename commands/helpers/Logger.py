import datetime


class Logger(object):
    def __init__(self):
        pass

    def log(self, func):
        """
        Logs activities in the CLI
        :return:
        """

        msg = "{} run on {}\n".format(func.name, datetime.date.today())

        with open('django_cli.log', 'a') as file: file.write(msg)
        file.close()
