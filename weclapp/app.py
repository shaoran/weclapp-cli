import sys

from argparse import ArgumentParser

from .config.config import def_config

from .modules import ConfigModule

modules = [
    ConfigModule,
]

class WeclappApp(object):
    """
    A container class of modules which boots the app
    """

    def __init__(self, args = sys.argv):
        parser = ArgumentParser(prog=args[0], description='Weclapp command line interface')

        parser.add_argument('-c', '--config', action='store', default=def_config, metavar='FILE',
                help='Sets the path of configuration file. Default %s' % def_config)

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

        return namespace.module(self, namespace).run()
