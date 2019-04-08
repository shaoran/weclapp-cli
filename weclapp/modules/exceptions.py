__all__ = [ 'InvalidCLIArguments', 'ParserNotFound' ]

from ..exception import WeclappBaseException

class WeclappModuleBaseException(WeclappBaseException):
    pass


class InvalidCLIArguments(WeclappModuleBaseException):
    """
    Raised when the CLI arguments are invalid
    """
    pass

class ParserNotFound(WeclappBaseException):
    """
    Raised when the parser is not found
    """
    pass
