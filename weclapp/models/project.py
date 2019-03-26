from .base import WeclappBaseModel

class WeclappProject(WeclappBaseModel):
    __model__ = 'WeclappProject'
    __fields__ = [
        ('id', 'id', str),
        ('name', 'name', str),
        ('projnr', 'projectNumber', str),
        ('billable', 'billable', bool),
    ]
