__all__ = [ 'ModelInvalidField', 'ApiNotLoaded', 'WrongFetchCommand' ]

from ..exception import WeclappBaseException

class WeclappModelBaseException(WeclappBaseException):
    pass


class ModelInvalidField(WeclappModelBaseException):
    """
    Raised when a field from the API response does not match
    the specification
    """
    pass

class ApiNotLoaded(WeclappModelBaseException):
    """
    Raised when the api is not loaded
    """
    pass

class WrongFetchCommand(WeclappModelBaseException):
    """
    Raised when the model class has a wrong fetch command
    """
    pass
