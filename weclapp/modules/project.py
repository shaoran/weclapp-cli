from .base import BaseModule

basehelp = 'Print information about the projects and tasks'

class ProjectModule(BaseModule):
    name = 'project'
    cmdline_opts = {
        'help': basehelp,
        'description': basehelp,
    }

    @staticmethod
    def init_argparser(parser):
        parser.add_argument('-j', '--json', action='store_true', default=False, dest='json',
                help='Print the results as JSON')
        parser.set_defaults(module = ProjectModule)


    def run(self):
        self.check_config()
        return 0
