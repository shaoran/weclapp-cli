import sys
import os
import logging

from colorama import Style, Fore

from ..parser.exceptions import FailedToParse
from .exceptions import ParserNotFound
from ..exception import WeclappBaseException, PrintHelp
from .base import BaseModule
from ..parser import CSVParser, add_parser
from ..parser.manage import parsers as weclapp_parsers

log = logging.getLogger("weclapp-cli")

basehelp = 'Upload time records'

class UploadModule(BaseModule):
    name = 'upload'
    cmdline_opts = {
        'help': basehelp,
        'description': basehelp,
    }

    @staticmethod
    def init_argparser(parser):
        parser.add_argument('-p', '--parser', action='store', dest='parser', metavar='PARSER',
                help='Set the parser to be used. Use --list to get the list of parsers.')
        parser.add_argument('-l', '--list', action='store_true', dest='list', default=False,
                help='List all parsers. The first parser in the list is the default one')
        parser.add_argument('files', action='store', metavar='FILE', nargs='*',
                help='The CSV file to be parsed')
        parser.add_argument('--list-parser-options', action='store_true', default=False, dest='list_parser_opts',
                help='Show the parser options. Use --parser to set the parser, otherwise the default one is shown')
        parser.add_argument('--po', action='append', dest='po', metavar='OPT=VAL',
                help='Parser options, you can use --po multiple times')
        parser.add_argument('--no-color', action='store_true', default=False, dest='nocolor',
                help='Disable colored output')
        parser.set_defaults(module = UploadModule)

    def run(self):
        add_parser('csv', CSVParser, default=True)
        init_parsers(self.namespace.config)

        if self.namespace.list:
            for p in weclapp_parsers:
                print(p['name'])
            return 0

        parser = weclapp_parsers[0]
        if self.namespace.parser:
            try:
                idx = list(map(lambda x: x['name'], weclapp_parsers)).index(self.namespace.parser)
            except:
                raise ParserNotFound('There is no parser \'%s\'' % self.namespace.parser)

            parser = weclapp_parsers[idx]

        if self.namespace.list_parser_opts:
            fmt = '{:15s}{:15s}{}'
            print('Parser: %s\n' % parser['name'])
            print(fmt.format('KEY', 'VALUE', 'DESCRIPTION'))
            for _ in range(40):
                print('-', end='')
            print('-')

            for key,val,desc in parser['parser'].__options__:
                print(fmt.format(key, val, desc))

            print('\n')
            print('use --po "KEY:VAL" to set an option. You can use --po multiple times')
            return 0

        if len(self.namespace.files) == 0:
            raise PrintHelp('No CSV files passed')

        parser_opts = parser['parser'].parse_parse_options(self.namespace.po or {})

        csv_parser = parser['parser'](options=parser_opts)

        time_records = []

        for fn in self.namespace.files:
            time_records += self.parseFile(csv_parser, fn)

        newtrs = []
        for tr in time_records:
            ans = tr.upload_to_weclapp()
            if ans:
                newtrs.append(ans)
            else:
                msg = "time record for project {}, task {} on {} with duration {} {} failed to be uploaded"
                if not self.namespace.nocolor:
                    msg = Fore.RED + msg + Style.RESET_ALL
                hours = int(tr.durationSeconds / 3600)
                plural = 'hours'
                if hours == 1:
                    plural = 'hour'
                print(msg.format(tr.projectId, tr.projectTaskId, tr.startDate, hours, plural))

        msg = "Succesfully uploaded time records"
        if not self.namespace.nocolor:
            msg = Fore.GREEN + msg + Style.RESET_ALL

        print(msg)

        for tr in newtrs:
            tr.print(indent='', with_color=not self.namespace.nocolor, with_projects=True)
        return 0

    def parseFile(self, csv_parser, filename):
        return csv_parser.parseFile(filename)



def init_parsers(config, fn='csv_exporter.py'):
    dn = os.path.dirname(config)
    plugin_file = os.path.join(dn, fn)

    plugin = load_plugin('weclapp_plugin_exporter', plugin_file)

    if plugin and hasattr(plugin, 'parsers'):
        try:
            for pobj in plugin.parsers:
                add_parser(pobj['name'], pobj['parser'], default=pobj.get('default', False))
        except WeclappBaseException:
            log.debug('Error while loading plugin', exc_info=True)
            raise
        except:
            log.debug('Could not load plugin correctly', exc_info=True)


def python_version_gte(*args):
    return sys.version_info >= args

def load_plugin(module_name, path):
    """
    loads the module 'base' from path

    module_name: the module name
    path: the path to the file with the plugin

    return the module if one is found, None otherwise
    """
    mod = None
    try:
        if python_version_gte(3, 5):
            import importlib.util
            spec = importlib.util.spec_from_file_location(module_name, location=path)

            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
        elif (python_version_gte(3, 0)):
            from importlib.machinery import SourceFileLoader
            l = SourceFileLoader(module_name, path)
            mod = l.load_module()
    except:
        log.debug('Could not import plugin \'%s\'', path, exc_info=True)

    return mod
