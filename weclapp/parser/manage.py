import inspect

from .exceptions import ParserInvalidType, ParserNameNotUnique
from .parser import Parser

parsers = []

def add_parser(name, parser, default=False):
    """
    Add a new parser to the list of parsers

    name must be a unique name
    parser must be a weclapp.Parser class
    """
    if name in map(lambda p: p['name'], parsers):
        raise ParserNameNotUnique('The parser \'%s\' is already in the parser list' % name)

    if not (inspect.isclass(parser) and issubclass(parser, Parser)):
        raise ParserInvalidType('Invalid class. It is not a weclapp.Parser class')

    idx = len(parsers)
    if default:
        idx = 0

    parsers.insert(idx, { 'name': name, 'parser': parser})
