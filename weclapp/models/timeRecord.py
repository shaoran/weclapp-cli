from .base import WeclappBaseModel

from datetime import datetime

class WeclappTimeRecord(WeclappBaseModel):
    __model__ = 'WeclappTimeRecord'
    __fields__ = [
        ('id', 'id', str),
        ('billable', 'billable', bool),
        ('project_id', 'projectId', str),
        ('task_id', 'projectTaskId', str),
        ('user_id', 'userId', str),
        ('duration', 'durationSeconds', int),
        ('created', 'createdDate', int),
        ('lastmodif', 'lastModifiedDate', int),
        ('startdate', 'startDate', int),
    ]

    def setup(self, **kwargs):
        self.task = None

    def setup(self, **kwargs):
        self.created = datetime.fromtimestamp(int(self.created) // 1000)
        self.lastmodif = datetime.fromtimestamp(int(self.lastmodif) // 1000)
        self.startdate = datetime.fromtimestamp(int(self.startdate) // 1000)
