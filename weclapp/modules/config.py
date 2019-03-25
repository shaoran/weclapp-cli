from .base import BaseModule

class ConfigModule(BaseModule):
    cmdline = "config"

    @staticmethod
    def init_argparser(parser):
        parser.set_defaults(module = ConfigModule)
