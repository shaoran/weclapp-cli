from .base import BaseModule
from ..api import WeclappAPI

basehelp = 'Print information about the projects and tasks'

class ProjectModule(BaseModule):
    name = 'projects'
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

        api = WeclappAPI(self.config)
        projects = api.load_projects()
        for proj in projects:
            print('%s [%s] %s' % (proj.id, proj.projnr, proj.name))
            for task in proj.tasks:
                print('  %s %s' % (task.id, task.name))
                total = 0
                for record in task.time_records:
                    print('    %s %.2f h %s desc="%s"' % (record.id, record.duration / 3600, record.startdate, record.description))
                    total = total + record.duration

                print('    Total time: %.2f h' % (total / 3600))

            print()
        return 0
