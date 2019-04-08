__all__ = [ 'ParserInvalidType', 'ParserNameNotUnique', 'FailedToParse', 'InvalidParserOptionFormat' ]

from ..exception import WeclappBaseException

class WeclappParserBaseException(WeclappBaseException):
    pass


class ParserInvalidType(WeclappParserBaseException):
    """
    Raised when the parser class is not a parser
    """
    pass

class ParserNameNotUnique(WeclappParserBaseException):
    """
    Raised when the parser class is not a parser
    """
    pass

class FailedToParse(WeclappParserBaseException):
    """
    Raised when the parser cannot parse a file
    """
    pass

class InvalidParserOptionFormat(WeclappParserBaseException):
    """
    Raised when the parsed option does not adhere KEY=VALUE
    """
