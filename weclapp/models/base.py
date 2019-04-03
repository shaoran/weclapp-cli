import sys
import math

from .exceptions import *

class WeclappBaseModel(object):
    __model__ = 'WeclappBaseModel'
    __fields__ = [
        # every model should fill this variable
        # with the field needed
        # (public api field, type, can_be_None)
    ]

    __api__ = None
    __fetch_command__ = None
    __expect_status_code__ = 200
    __method__ = 'GET'

    def __init__(self, **kwargs):
        for field, klass, can_be_None in self.__fields__:
            val = kwargs.get(field, None)
            if val is None:
                if can_be_None:
                    setattr(self, field, None)
                    continue
                else:
                    raise ModelInvalidField('%s: The field \'%s\' cannot be found in public API response or is NULL' % (self.__model__, field))

            if not isinstance(val, klass):
                raise ModelInvalidField('%s: The field \'%s\' is not of type \'%s\'' % (self.__model__, field, klass.__name__))


            setattr(self, field, val)

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


    @classmethod
    def load(cls, sort=None, pageSize=100, serializeNulls=True):
        """
        Fetches the data from the public API

        params:

            sort           the sort parameters
            pageSize       number of elements
            serializeNulls serialize NULL entries

        See https://www.weclapp.com/api2/ for a better understanding
        of these parameters

        If you pass pageSize=-1, then it will fetch all elements

        pageSize is capped at 500
        """
        if cls.__api__ is None:
            raise ApiNotLoaded('The API is not loaded, cannot fetch the data')

        if cls.__fetch_command__ is None:
            raise WrongFetchCommand('This class (%s) has no valid fetch command' % cls.__name__)

        if pageSize > 500:
            pageSize = 500

        num_of_pages = 1

        if pageSize == -1:
            api = cls.__api__.call('%s/count' % cls.__fetch_command__, 'GET')
            length = api['result']
            num_of_pages = math.ceil(length / 500)
            pageSize = 500

        res = []
        for i in range(num_of_pages):
            query = {
                'page': i+1,
            }
            if sort:
                query['sort'] = sort

            query['pageSize'] = pageSize

            if serializeNulls:
                query['serializeNulls'] = 1

            data = cls.__api__.call(cls.__fetch_command__, cls.__method__, query=query,
                    expected_status_code=cls.__expect_status_code__)

            res += [ cls(**p) for p in data['result'] ]

        return res

    def print(self, indent='', with_color=True, file=sys.stdout):
        """
        Overwrite this
        """
        pass
