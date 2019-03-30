import logging

from .base import WeclappBaseModel

log = logging.getLogger("weclapp-cli")

class WeclappProject(WeclappBaseModel):
    __model__ = 'WeclappProject'
    __fields__ = [
        ('id', 'id', str),
        ('name', 'name', str),
        ('projnr', 'projectNumber', str),
        ('billable', 'billable', bool),
    ]
    __fetch_command__ = 'project'

    def setup(self, **kwargs):
        self.tasks = []

    def add_task(self, task):

        tids = map(lambda r: r.id, self.tasks)

        if task.id in tids:
            return

        self.tasks.append(task)

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
            proj = projects_map.get(task.project_id, None)
            if proj is None:
                log.debug('No project loaded for task %s with project_id %s', task.id, task.project_id)
                continue

            proj.add_task(task)
            task.project = proj

        if time_records == 0:
            return projects

        tasks_map = { t.id: t for t in tasks }

        time_records = WeclappTimeRecord.load(sort='-startDate', pageSize=time_records, serializeNulls=True)

        for tr in time_records:
            task = tasks_map.get(tr.task_id, None)
            if task is None:
                log.debug('No task loaded for the time record %s with task_id %s', tr.id, tr.task_id)
            proj = projects_map.get(tr.project_id, None)
            if proj is None:
                log.debug('No project loaded for time record %s with project_id %s', tr.id, tr.project_id)

            task.add_time_record(tr)
            tr.task = task

        # sorting
        for task in tasks:
            task.time_records = sorted(task.time_records, key=lambda r: r.startdate, reverse=True)

        return projects
