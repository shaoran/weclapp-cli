from .exceptions import *

class WeclappBaseModel(object):
    __model__ = 'WeclappBaseModel'
    __fields__ = [
        # every model should fill this variable
        # with the field needed
        # (model field, public api field, type)
    ]

    api = None

    def __init__(self, **kwargs):
        for mfield, pfield, klass in self.__fields__:
            if pfield not in kwargs:
                raise ModelInvalidField('%s: The field \'%s\' cannot be found in public API response' % (self.__model__, pfield))

            val = kwargs[pfield]

            if val is not None and not isinstance(val, klass):
                raise ModelInvalidField('%s: The field \'%s\' is not of type \'%s\'' % (self.__model__, pfield, klass.__name__))

            setattr(self, mfield, val)

        self.setup(**kwargs)

    def setup(self, **kwargs):
        """
        Called during initialization. Override this function if
        further initialization is required (for example to convert
        dates from unix timestamps)
        """
        pass


    def todict(self):
        ret = {}

        for mfield, pfield, klass in self.__fields__:
            ret[mfield] = getattr(self, mfield)

        return ret

    def __str__(self):
        return '<%s %s>' % (self.__model__, self.todict())

    def __repr__(self):
        return str(self)
