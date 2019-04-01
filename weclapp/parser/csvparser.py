from .parser import Parser

class CSVParser(Parser):
    """
    The file is a CSV like like with this structure:

          DATE    TIME          DESC            TIME          DESC
        +-------+-------------+---------------+-------------+---------------+
        |       | Projekt NR  |               | Projekt NR  |               |
        |       | Task ID     |               | Task ID     |               |
        | date  | 5           | description 1 | 3           | description 1 |
        | date  | 6           |               | 2           | description 2 |
        +-------+-------------+---------------+-------------+---------------+

    The first two lines function as a header. The first and third cells of the
    the header rows are ignored. 'Projekt Nr' and TASK ID have to be the
    weclapp project number and the project task.

    The date column and the time columns are mandatory. The description column
    may be empty.

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
    pass
