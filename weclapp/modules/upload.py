from .base import BaseModule
from ..parser import CSVParser, add_parser
from ..parser.manage import parsers as weclapp_parsers

basehelp = 'Upload time records'

class UploadModule(BaseModule):
    name = 'upload'
    cmdline_opts = {
        'help': basehelp,
        'description': basehelp,
    }

    @staticmethod
    def init_argparser(parser):
        parser.set_defaults(module = UploadModule)

    def run(self):
        add_parser('csv', CSVParser, default=True)
        return 0
