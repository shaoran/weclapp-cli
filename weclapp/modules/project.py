from argparse import RawTextHelpFormatter

from .base import BaseModule
from ..models import WeclappProject

basehelp = 'Print information about the projects and tasks'
epilog = """
If you use --projects-only or --projects-with-tasks then time
records are not fetched.

If you want to display all time records, then use --last all
"""

class ProjectModule(BaseModule):
    name = 'projects'
    cmdline_opts = {
        'help': basehelp,
        'description': basehelp,
        'epilog': epilog,
        'formatter_class': RawTextHelpFormatter,
    }

    @staticmethod
    def init_argparser(parser):
        parser.add_argument('-p', '--projects-only', action='store_true', default=False, dest='projects_only',
                help='Show only projects')

        parser.add_argument('-t', '--projects-with-tasks', action='store_true', default=False, dest='projects_and_tasks',
                help='Show only projects and tasks.')

        parser.add_argument('-l', '--last', action='store', default=100, dest='last', metavar='N',
                help='Show the last N time records.')

        parser.add_argument('-q', '--query', action='store', default='', dest='query', metavar='QUERY',
                help='Filter projects and tasks by query.\nDisplays the projects & tasks that contains the query.')
        parser.set_defaults(module = ProjectModule)


    def run(self):
        projects = WeclappProject.load()
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
