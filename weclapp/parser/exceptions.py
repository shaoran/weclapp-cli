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

__all__ = [ 'ParserInvalidType', 'ParserNameNotUnique' ]
