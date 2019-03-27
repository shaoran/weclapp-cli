from .base import WeclappBaseModel

class WeclappTask(WeclappBaseModel):
    __model__ = 'WeclappTask'
    __fields__ = [
        ('id', 'id', str),
        ('allow', 'allowTimeTracking', bool),
        ('name', 'name', str),
        ('project_id', 'projectId', str),
    ]
