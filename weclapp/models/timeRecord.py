import sys

from .base import WeclappBaseModel

from datetime import datetime

class WeclappTimeRecord(WeclappBaseModel):
    __model__ = 'WeclappTimeRecord'
    __fields__ = [
        ('id', str, True),
        ('billable', bool, True),
        ('projectId', str, False),
        ('projectTaskId', str, False),
        ('userId', str, True),
        ('durationSeconds', int, False),
        ('createdDate', int, True),
        ('lastModifiedDate', int, True),
        ('startDate', int, False),
        ('description', str, True),
    ]
    __fetch_command__ = 'timeRecord'

    def setup(self, **kwargs):
        self.task = None

        if self.createdDate:
            self.createdDate = datetime.fromtimestamp(int(self.createdDate) // 1000)

        if self.lastModifiedDate:
            self.lastModifiedDate = datetime.fromtimestamp(int(self.lastModifiedDate) // 1000)

        if self.startDate:
            self.startDate = datetime.fromtimestamp(int(self.startDate) // 1000)

        if self.description is None:
            self.description = ''

        self.description = self.description.strip()

    def print(self, indent='    ', with_color=True, file=sys.stdout):
        desc = ''
        if self.description != '':
            desc = self.description

        hours = int(self.durationSeconds / 3600)
        plural = 's'
        if hours == 1:
            plural = ''

        hours = '{:.2f}'.format(hours)

        msg = '{}{:22s}{:5s} hour{:4s}{:10s}'
        print(msg.format(indent, str(self.startDate), hours, plural, desc), file=file)
