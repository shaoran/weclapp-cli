from .base import WeclappBaseModel

class WeclappTask(WeclappBaseModel):
    __model__ = 'WeclappTask'
    __fields__ = [
        ('id', 'id', str),
        ('allow', 'allowTimeTracking', bool),
        ('name', 'name', str),
        ('project_id', 'projectId', str),
    ]

    project = None

    time_records = []

    def add_time_record(self, record):

        rids = map(lambda r: r.id, self.time_records)

        if record.id in rids:
            return

        self.time_records.append(record)
        self.time_records = sorted(self.time_records, key=lambda r: r.created)
