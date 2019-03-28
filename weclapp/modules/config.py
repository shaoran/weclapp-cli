import sys
import yaml

from .base import BaseModule
from ..config import Config

basehelp = 'Generate a new configuration file needed to access the public weclapp API'

class ConfigModule(BaseModule):
    name = 'config'
    cmdline_opts = {
        'help': basehelp,
        'description': """%s\n
        \n
        In order to access the pubic API of you weclapp server, you need to provide
        these domain, the path and your API TOKEN for authentification. Your API TOKEN
        is found in the account settings page once you've logged in.\n\n
        If you run in batch mode, then you must pass all arguments. In the interactive
        mode you don't need to pass any parameter.
        """ % basehelp,
    }
    autoload_api = False

    @staticmethod
    def init_argparser(parser):
        def_path = '/webapp/api/v1'
        parser.add_argument('-l', '--list', action='store_true', default=False, dest='list',
                help='Show the stored configuration. Batch mode is ignore in this case')
        parser.add_argument('-b', '--batch-mode', action='store_true', default=False, dest='batch',
                help='Batch mode, disables interactive mode. Interactive mode is enabled by default')
        parser.add_argument('-d', '--domain', action='store', dest='domain', metavar='DOMAIN',
                help='The domain of the public API')
        parser.add_argument('-p', '--path', action='store', dest='path', metavar='PATH', default=def_path,
                help='The path of the public API, default: %s' % def_path)
        parser.add_argument('-t', '--api-token', action='store', dest='apitoken', metavar='API-TOKEN',
                help='Your API-TOKEN. Log in into weclapp, go to the account setting where you\'ll find the API TOKEN')
        parser.add_argument('-s', '--ssl', action='store', dest='ssl', default=True,
                help='Use SSL to access public API')
        parser.set_defaults(module = ConfigModule)


    def run(self):
        if self.namespace.list:
            return self.list_config()

        cfg = Config(path=self.namespace.config)

        if not self.namespace.batch:
            print('Generating a new configuration file %s' % self.namespace.config)
            try:
                cfg.parse()
                self.namespace.domain = cfg.config.get("domain", None)
                self.namespace.path = cfg.config.get("path", None)
                self.namespace.apitoken = cfg.config.get("apitoken", None)
                ssl = cfg.config.get("ssl", None)
                if ssl is not None:
                    self.namespace.ssl = ssl
            except:
                pass


        args = {}

        if self.namespace.domain is not None:
            args['domain'] = self.namespace.domain

        if self.namespace.path is not None:
            args['path'] = self.namespace.path

        if self.namespace.apitoken is not None:
            args['apitoken'] = self.namespace.apitoken

        if self.namespace.ssl:
            args['ssl'] = "yes"
        else:
            args['ssl'] = "no"

        if self.namespace.batch:
            if len(args) != 3:
                print('In batch mode, please provide all arguments\n', file=sys.stderr)
                self.app.parser.print_help(file=sys.stderr)
                return 1

            args["verbose"] = False

        newcfg = cfg.interactive_config(**args)
        cfg.set_new_config(newcfg)

        cfg.save()
        return 0

    def list_config(self):
        cfg = Config(path=self.namespace.config)

        cfg.parse()
        yaml.dump(cfg.config, sys.stdout)
        return 0
