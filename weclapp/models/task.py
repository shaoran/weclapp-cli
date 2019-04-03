import sys
from colorama import Fore, Back, Style

from .base import WeclappBaseModel

class WeclappTask(WeclappBaseModel):
    __model__ = 'WeclappTask'
    __fields__ = [
        ('id', str, False),
        ('allowTimeTracking', bool, False),
        ('name', str, False),
        ('projectId', str, False),
    ]
    __fetch_command__ = 'projectTask'

    def setup(self, **kwargs):
        self.time_records = []
        self.project = None

    def add_time_record(self, record):

        rids = map(lambda r: r.id, self.time_records)

        if record.id in rids:
            return

        self.time_records.append(record)

    def print(self, indent='  ', with_color=True, file=sys.stdout):
        msg = '{}{:38s}[ID: {}]'
        if with_color:
            msg = Style.BRIGHT + Fore.BLUE + msg + Style.RESET_ALL
        print(msg.format(indent, self.name, self.id), file=file)
