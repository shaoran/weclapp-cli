from ..config import Config
from .. import WeclappBaseException, ConfigInvalid

class BaseModule(object):
    """
    The base module
    """

    name = 'base'
    cmdline_opts = {}
    autoload_api = True

    def __init__(self, app, namespace, config):
        self.app = app
        self.namespace = namespace
        self.config = config

    @staticmethod
    def init_argparser(parser):
        pass

    def run(self, namespace):
        raise Exception('The run method has to be overriden')
