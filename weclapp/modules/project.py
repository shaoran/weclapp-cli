from argparse import RawTextHelpFormatter
from colorama import Fore, Back, Style

from .base import BaseModule
from ..models import WeclappProject
from .exceptions import InvalidCLIArguments

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

        parser.add_argument('--no-color', action='store_true', default=False, dest='nocolor',
                help='Disable colored output')
        parser.set_defaults(module = ProjectModule)


    def run(self):
        if self.namespace.last == "all":
            time_records = -1
        else:
            try:
                time_records = int(self.namespace.last)
            except:
                time_records = -1

            if time_records < 0:
                raise InvalidCLIArguments('--last is invalid. It only can be a positive number or \'all\'')

        if self.namespace.projects_only or self.namespace.projects_and_tasks:
            time_records = 0

        kwargs = {
            'time_records': time_records,
            'tasks': not self.namespace.projects_only,
        }

        projects = WeclappProject.load(**kwargs)

        self.mark_all_to_show(projects)

        query = self.namespace.query.strip()
        if query != '':
            filter_query(projects, query)

        if not self.namespace.projects_only and not self.namespace.projects_and_tasks:
            self.hide_if_no_time_records(projects)

        with_color = not self.namespace.nocolor

        for proj in projects:
            if proj.hide:
                continue

            msg = '{:10s}{:30s}[ID: {}] Billable: {}'
            if with_color:
                msg = Style.BRIGHT + msg + Style.RESET_ALL

            bill_color = ''
            if with_color:
                bill_color = Fore.RED
            bill_text = 'no'

            if proj.billable:
                bill_text = 'yes'
                if with_color:
                    bill_color = Fore.GREEN

            billable = bill_color + bill_text

            print(msg.format(proj.projnr, proj.name, proj.id, billable))

            for task in proj.tasks:
                if task.hide:
                    continue

                msg = '  {:38s}[ID: {}]'
                if with_color:
                    msg = Style.BRIGHT + Fore.BLUE + msg + Style.RESET_ALL
                print(msg.format(task.name, task.id))
                total = 0
                for record in task.time_records:
                    desc = ''
                    if record.description != '':
                        desc = record.description

                    hours = record.duration / 3600
                    plural = 's'
                    if hours == 1:
                        plural = ''

                    hours = '{:.2f}'.format(hours)

                    msg = '    {:22s}{:5s} hour{:4s}{:10s}'
                    print(msg.format(str(record.startdate), hours, plural, desc))
                    total = total + record.duration

                if total != 0:
                    hours = total / 3600
                    time = "hours"
                    if hours == 1:
                        time = "hour"
                    msg = '    Total time: %.2f %s' % (hours, time)
                    if with_color:
                        msg = Style.BRIGHT + msg + Style.RESET_ALL
                    print(msg)
        return 0

    def mark_all_to_show(self, projects):
        for proj in projects:
            proj.hide = False

            for task in proj.tasks:
                task.hide = False

    def hide_if_no_time_records(self, projects):
        """
        Hide projects & tasks with no time records
        """
        for proj in projects:
            proj.hide = True
            if len(proj.tasks) == 0:
                continue

            for task in proj.tasks:
                task.hide = True
                if len(task.time_records) == 0:
                    continue

                task.hide = False

            # show project if at least one task has hide == False
            if any(map(lambda tt: not tt.hide, proj.tasks)):
                proj.hide = False

def unmask_tasks(project):
    for task in project.tasks:
        task.hide = False

def filter_query(projects, query):
    for proj in projects:
        if match_project(proj, query):
            proj.hide = False
            unmask_tasks(proj)
            continue

        proj.tasks = list(filter(lambda t: match_task(t, query), proj.tasks))

        unmask_tasks(proj)

        proj.hide = True

        if len(proj.tasks) > 0:
            proj.hide = False


def match_task(task, query):
    query = query.lower()
    name = task.name.lower()
    try:
        name.index(query)
    except ValueError:
        return False

    return True

def match_project(project, query):
    query = query.lower()
    name = project.name.lower()
    projnr = project.projnr.lower()

    f = False

    try:
        name.index(query)
        f = True
    except ValueError:
        pass

    if f:
        return True

    try:
        projnr.index(query)
    except ValueError:
        return False

    return True
