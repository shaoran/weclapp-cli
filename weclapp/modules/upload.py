from .base import BaseModule

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
        return 0
