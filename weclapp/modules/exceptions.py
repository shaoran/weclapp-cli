from ..exception import WeclappBaseException

class WeclappModuleBaseException(WeclappBaseException):
    pass


class InvalidCLIArguments(WeclappModuleBaseException):
    """
    Raised when the CLI arguments are invalid
    """
    pass

__all__ = [ 'InvalidCLIArguments' ]

