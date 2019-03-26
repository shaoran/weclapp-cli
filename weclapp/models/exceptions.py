from ..exception import WeclappBaseException

class WeclappModelBaseException(WeclappBaseException):
    pass


class ModelInvalidField(WeclappModelBaseException):
    """
    Raised when a field from the API response does not match
    the specification
    """
    pass


__all__ = [ 'ModelInvalidField' ]
