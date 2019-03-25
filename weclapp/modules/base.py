class BaseModule(object):
    """
    The base module
    """

    name = 'base'
    cmdline_opts = {}

    def __init__(self, app, namespace):
        self.app = app
        self.namespace = namespace

    @staticmethod
    def init_argparser(parser):
        pass

    def run(self, namespace):
        raise Exception('The run method has to be overriden')
