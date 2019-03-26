from ..config import Config
from .. import WeclappBaseException, ConfigInvalid

class BaseModule(object):
    """
    The base module
    """

    name = 'base'
    cmdline_opts = {}

    def __init__(self, app, namespace):
        self.app = app
        self.namespace = namespace
        self.config = None

    @staticmethod
    def init_argparser(parser):
        pass

    def run(self, namespace):
        raise Exception('The run method has to be overriden')

    def check_config(self):
        cfg = Config(path=self.namespace.config)
        try:
            cfg.parse()
        except WeclappBaseException:
            raise ConfigInvalid('Invalid configuration. Please execute \'weclapp-cli config\' to create a new configuration')

        self.config = cfg.config
