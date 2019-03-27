from .base import WeclappBaseModel

class WeclappProject(WeclappBaseModel):
    __model__ = 'WeclappProject'
    __fields__ = [
        ('id', 'id', str),
        ('name', 'name', str),
        ('projnr', 'projectNumber', str),
        ('billable', 'billable', bool),
    ]

    def setup(self, **kwargs):
        self.tasks = []

    def add_task(self, task):

        tids = map(lambda r: r.id, self.tasks)

        if task.id in tids:
            return

        self.tasks.append(task)
