import sys
import os
import logging

from ..exception import WeclappBaseException
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
        parser.add_argument('files', action='store', metavar='FILE', nargs='+',
                help='The CSV file to be parsed')
        parser.add_argument('--project-id', action='store', metavar='PROJECT ID', dest='project_id',
                help='The default project id, used by parser if no project id was found in the parsed file')
        parser.add_argument('--task-id', action='store', metavar='TASK ID', dest='task_id',
                help='The default task id, used by parser if no task id was found in the parsed file')
        parser.set_defaults(module = UploadModule)

    def run(self):
        add_parser('csv', CSVParser, default=True)
        init_parsers(self.namespace.config)

        return 0


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
