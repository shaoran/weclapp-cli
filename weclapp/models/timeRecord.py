import sys
import json
import logging

from .base import WeclappBaseModel

from datetime import datetime

log = logging.getLogger("weclapp-cli")

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

    def dict_for_upload(self):
        ret = {}

        for field in ['billable', 'projectId', 'projectTaskId', 'durationSeconds' ]:
            ret[field] = getattr(self, field)

        ret['startDate'] = int(self.startDate.timestamp() * 1000)

        if isinstance(self.description, str) and self.description.strip() != '':
            ret['description'] = self.description

        return ret

    def print(self, indent='    ', with_color=True, file=sys.stdout, with_projects=False):
        desc = ''
        if self.description != '':
            desc = self.description

        hours = int(self.durationSeconds / 3600)
        plural = 's'
        if hours == 1:
            plural = ''

        hours = '{:.2f}'.format(hours)

        msg = '{}{}{}{:22s}{:5s} hour{:4s}{:10s}'

        proj = ''
        task = ''
        if with_projects:
            proj = 'PROJECT {:6s}'.format(self.projectId)
            if hasattr(self, 'projectNumber') and self.projectNumber is not None:
                nr = self.projectNumber.strip()
                proj = '{}{:10s}'.format(proj, '[%s]' % self.projectNumber)
            task = 'TASK {:6s}'.format(self.projectTaskId)

        print(msg.format(indent, proj, task, str(self.startDate), hours, plural, desc), file=file)

    def upload_to_weclapp(self):
        """
        uploads the time record to weclapp

        You can only upload time reports without a valid id

        returns the newly created time report, None otherwise
        """

        body = json.dumps(self.dict_for_upload())

        try:
            res = self.__api__.call(self.__fetch_command__, 'POST', body=body, expected_status_code=201)
        except:
            log.debug('Failed to upload the time record', exc_info=True)
            return None

        return type(self)(**res)
