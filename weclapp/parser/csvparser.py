import logging

from dateutil.parser import parse as date_parse

from .parser import Parser
from .exceptions import FailedToParse, InvalidParserOptionFormat

log = logging.getLogger("weclapp-cli")

class CSVParser(Parser):
    """
    The file is a CSV like like with this structure:

          DATE    TIME          DESC            TIME          DESC
        +-------+-------------+---------------+-------------+---------------+
        |       | Project iD  |               | Project ID  |               |
        |       | Task ID     |               | Task ID     |               |
        | date  | 5           | description 1 | 3           | description 1 |
        | date  | 6           |               | 2           | description 2 |
        +-------+-------------+---------------+-------------+---------------+

    The first two lines function as a header. The first and third cells of the
    the header rows are ignored. 'Project ID' and TASK ID have to be the
    weclapp project number and the project task.

    The date column and the time columns are mandatory. The description column
    may be empty. The date column is parsed with dateutils.parser.parse function.
    If this function parses successfully the date, then this date is used. Please
    take a look at https://dateutil.readthedocs.io/en/stable/parser.html for more
    information about the different strings that are parsed by this function.

    In the description don't use the character used for separation, this parser
    does not support escaped strings.

    If you want to set the time to something different  than timeStart, then you
    can do this:

      11:15/6

    that means that the timeStart will be 11:15 and that you book 6 hours to the
    project.

    The table can have unlimited number of projects, every project must consist of
    two columns, one with the time, another with the description.
    """
    __options__ = [
        ('sep', ';', 'The CSV separator'),
        ('timeStart', '09:00', 'The start of the time record'),
        ('encoding', 'utf-8', 'Default file encoding'),
    ]

    def parseFile(self, filename):
        try:
            with open(filename, encoding=self.options.encoding) as fp:
                lines = [ x.strip() for x in fp.readlines() ]
        except:
            log.debug('Cannot open the file', exc_info=True)
            raise FailedToParse('Could not open file')

        if len(lines) < 3:
            raise FailedToParse('Invalid format, header is missing or first data line is missing')

        pinfo = []

        headers = [ lines[0].split(self.options.sep), lines[1].split(self.options.sep) ]

        hl = abs(len(headers[0]) - len(headers[1]))
        if hl > 1:
            raise FailedToParse('Invalid format, the header rows do not match, invalid length')

        if hl == 1:
            if len(headers[0]) > len(headers[1]):
                idx = 1
            else:
                idx = 0
            headers[idx].append('')

        if len(headers[0]) % 2 == 0:
            headers[0].append('')
            headers[1].append('')

        # thanks to https://opensourcehacker.com/2011/02/23/tuplifying-a-list-or-pairs-in-python/
        headers = [ list(zip(*[h[x::2] for x in (1, 2)])) for h in headers ]
        headers = [ [ h[0] for h in k ] for k in headers ]
        headers = list(zip(*headers))

        print(headers)

        return []
