import sys
import coloredlogs, logging

from argparse import ArgumentParser

from .config.config import def_config, Config
from .modules import ConfigModule, ProjectModule, UploadModule
from .api import WeclappAPI
from . import ConfigInvalid, WeclappBaseException
from .models.base import WeclappBaseModel

modules = [
    ConfigModule,
    ProjectModule,
    UploadModule,
]


log = logging.getLogger("weclapp-cli")

class WeclappApp(object):
    """
    A container class of modules which boots the app
    """

    def __init__(self, args = sys.argv):
        parser = ArgumentParser(prog=args[0], description='Weclapp command line interface')

        parser.add_argument('-c', '--config', action='store', default=def_config, metavar='FILE',
                help='Sets the path of configuration file. Default %s' % def_config)

        parser.add_argument('-d', '--debug', action='store_true', default=False,
                help='Enable debug output')

        subparser = parser.add_subparsers(title="COMMANDS", description='weclapp-cli commands',
                help='Pass -h after the command to get additional help for the command')

        self.modules = []

        for mod in modules:
            p = subparser.add_parser(mod.name, **mod.cmdline_opts)
            mod.init_argparser(p)

        self.parser = parser
        self.args = args


    def run(self):
        namespace = self.parser.parse_args(self.args[1:])
        if not hasattr(namespace, 'module'):
            print('COMMAND not specified\n---------------------\n', file=sys.stderr)
            self.parser.print_help(file=sys.stderr)
            return 1

        if namespace.debug:
            coloredlogs.install(level='DEBUG')
            logging.basicConfig(level=logging.DEBUG)

        cfg = Config(path=namespace.config)
        try:
            cfg.parse()
        except WeclappBaseException:
            raise ConfigInvalid('Invalid configuration. Please execute \'weclapp-cli config\' to create a new configuration')

        if namespace.module.autoload_api:
            WeclappBaseModel.__api__ = WeclappAPI(cfg.config)

        return namespace.module(self, namespace, cfg.config).run()
