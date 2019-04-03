import sys
import logging

from colorama import Fore, Back, Style

from .base import WeclappBaseModel

log = logging.getLogger("weclapp-cli")

class WeclappProject(WeclappBaseModel):
    __model__ = 'WeclappProject'
    __fields__ = [
        ('id', str, False),
        ('name', str, False),
        ('projectNumber', str, False),
        ('billable', bool, False),
    ]
    __fetch_command__ = 'project'

    def setup(self, **kwargs):
        self.tasks = []

    def add_task(self, task):

        tids = map(lambda r: r.id, self.tasks)

        if task.id in tids:
            return

        self.tasks.append(task)

    def print(self, indent='', with_color=True, file=sys.stdout):
        msg = '{}{:10s}{:30s}[ID: {}] Billable: {}'
        if with_color:
            msg = Style.BRIGHT + msg + Style.RESET_ALL

        bill_color = ''
        if with_color:
            bill_color = Fore.RED
        bill_text = 'no'

        if self.billable:
            bill_text = 'yes'
            if with_color:
                bill_color = Fore.GREEN

        billable = bill_color + bill_text

        print(msg.format(indent, self.projectNumber, self.name, self.id, billable))

    @classmethod
    def load(cls, tasks=True, time_records=100, **kwargs):
        """
        Loads projects

        params:

            tasks         if set, load the project tasks and bind them to the projects
            time_records  load the last n time records. If n is -1, then load all time
                          records. If tasks is not set, this setting is ignored
            kwargs        arguments accepted by the base class
        """
        from .task import WeclappTask             # avoiding circle dependencies
        from .timeRecord import WeclappTimeRecord # avoiding circle dependencies
        projects = super().load(**kwargs)

        if not tasks:
            return projects

        projects_map = { p.id: p for p in projects }

        tasks = WeclappTask.load()

        for task in tasks:
            proj = projects_map.get(task.projectId, None)
            if proj is None:
                log.debug('No project loaded for task %s with projectId %s', task.id, task.projectId)
                continue

            proj.add_task(task)
            task.project = proj

        if time_records == 0:
            return projects

        tasks_map = { t.id: t for t in tasks }

        time_records = WeclappTimeRecord.load(sort='-startDate', pageSize=time_records, serializeNulls=True)

        for tr in time_records:
            task = tasks_map.get(tr.projectTaskId, None)
            if task is None:
                log.debug('No task loaded for the time record %s with projectTaskId %s', tr.id, tr.projectTaskId)
            proj = projects_map.get(tr.projectId, None)
            if proj is None:
                log.debug('No project loaded for time record %s with projectId %s', tr.id, tr.projectId)

            task.add_time_record(tr)
            tr.task = task

        # sorting
        for task in tasks:
            task.time_records = sorted(task.time_records, key=lambda r: r.startDate, reverse=True)

        return projects
