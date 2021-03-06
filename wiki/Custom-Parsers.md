
## Table of contents

- [Custom Parsers](#)
    - [Creating `weclapp.WeclappTimeRecord` objects](#creating-weclappweclapptimerecord-objects)
    - [Custom class structure](#custom-class-structure)
- [Basic example](#basic-example)
- [Including your parser in `weclapp-cli`](#including-your-parser-in-weclapp-cli)
    - [Example](#example)


Every parser has to inherit from the `weclapp.Parser` class. The `upload` module
will create a list of parsers and depending on the `--parser` option of the `upload` module,
it will select one parser.

Then it will use `argparse` to get the command line arguments concerning the parser and
initialize the parser with the command line arguments. All command line arguments are not
required and must have a meaningful default value. The base class takes care to construct
a `argparse.Namsepace` object with the command line values. In most cases you don't need
to overwrite the `__init__` function, but you can use the `setup()` function to do you own
initialization.

Every parser class must define a class variable `__options__` which is an list of tuples.

The tuples in the `__options__` list determine the command line arguments of the parser. The
structure of the tuple is

```python
(cmd argument, default value, help string)
```

Every parser also has to overwrite the `parseFile` method. This method does the parsing
of the file and must return a list of `weclapp.WeclappTimeRecord` objects.

If the parsing fails, you should raise one of these exceptions:

- `weclapp.FailedToParse`: when the parser fails to parse the file, for whatever reason
- `weclapp.InvalidParserOptionFormat`: when a command line arguments has an invalid value

You can access the command line options for the parser through `self.options`.

## Creating `weclapp.WeclappTimeRecord` objects

The time record object that is returned by weclapp's public API is a large dictionary. Only a few
keys are of interest for this project. You can see a list of the keys that `weclapp-cli` maps
to `weclapp.WeclappTimeRecord` in [weclapp/models/timeRecord.py L13][1].

The next table shows the keys that are needed in order for uploading a new time record:

| key               | description                 | Type                | Required?          |
| ----------------- | --------------------------- | ------------------- | ------------------ |
| `billable`        | is the time record billable | `bool`              | No, default `True` |
| `projectId`       | the ID of the project       | `str`               | yes                |
| `projectTaskId`   | the ID of the project task  | `str`               | yes                |
| `durationSeconds` | the duration of the record  | `int`               | yes                |
| `startDate`       | the time of day             | `int`, JS timestamp | yes                |
| `description`     | a description               | `str`               | No                 |

**Example**

```python
from datetime import datetime
from weclapp import WeclappTimeRecord

# 5th of April 2019, 9 AM
day = datetime(2019, 4, 5, 9, 0)

time_record = WeclappTimeRecord(
    billable = False,
    projectId = '15246',
    projectTaskId = '43121',
    durationSeconds = 3 * 60 * 60,
    startDate = int(day.timestamp() * 1000),
    description = 'A simple task')

time_record.print(indent='')

# prints
# 2019-04-05 09:00:00   3.00  hours   A simple task
```

## Custom class structure

```python
from weclapp import Parser

class MyCustomCSV(Parser):
    __options__ = [
        # your cmd line options
    ]

    def setup(self):
        # in case you need custom initialization
        pass

    def parseFile(self, filename):
        # the parser
        # return a list of weclapp.WeclappTimeRecord objects
        pass

```

# Basic example

This example shows how to construct a parser class that handles files where

- the first column is a date with time
- the second column is the project id
- the third column is the task id
- the fourth column is the duration
- the fifth column is the description


It should parse this file

    date;projectId;projectTaskId;durationSeconds;description
    2019.02.01 09:30 UTC;112211;888888;5;some description
    2019.02.01 09:30 UTC;112211;777777;3;some description


A simple program:

```python
#!/usr/bin/env python

import sys

import pandas as pd
from weclapp import Parser, WeclappTimeRecord, FailedToParse

class MySimpleCSV(Parser):
    __options__ = [
        ('sep', ';', 'CSV separator'),
    ]

    def parseFile(self, filename):
        try:
            df = pd.read_csv(filename, sep=self.options.sep, parse_dates=['date'])
        except Exception as e:
            raise FailedToParse('Could not parse csv file: %s' % (str(e)))

        timerecords = []

        for idx, row in df.iterrows():
            tr_dict = {
                'startDate': int(row['date'].timestamp() * 1000),
                'projectId': str(row['projectId']),
                'projectTaskId': str(row['projectTaskId']),
                'durationSeconds': row['durationSeconds'] * 3600,
                'description': row['description'],
            }

            timerecords.append(WeclappTimeRecord(**tr_dict))
        return timerecords


def main():
    if len(sys.argv) != 2:
        print('usage: %s csv-file' % sys.argv[0], file=sys.stderr)
        return 1

    opts = dict(sep=';')

    p = MySimpleCSV(options=opts)

    records = p.parseFile(sys.argv[1])

    for rec in records:
        rec.print(indent='')

    return 0

if __name__ == '__main__':
    sys.exit(main())
```

# Including your parser in `weclapp-cli`

The default path of the config file is `${HOME}/.config/weclapp-cli/config.yml`. To include
your parser(s) in `weclapp-cli`, you need to create a file `csv_exporter.py` in the same
directory of the config file. By default you should create the file
`${HOME}/.config/weclapp-cli/csv_exporter.py`.

The `csv_exporter.py` file must have a variable `parsers` which is a list of your custom
parsers. Every item in this list must be a dictionary:

    { 'name': 'your parser name', 'parser': <the parser class>, [ 'default': <bool> ] }

`name` should be a unique string. With `weclapp-cli upload --parser "parser-name"` you can select
the parser to be used. If the `default` key is `True`, then your parser will become the default
parser and you don't need to use the `--parser` option.

## Example

```python
# ${HOME}/.config/weclapp-cli/csv_exporter.py

import pandas as pd
from weclapp import Parser, WeclappTimeRecord, FailedToParse

class MySimpleCSV(Parser):
    __options__ = [
        ('sep', ';', 'CSV separator'),
    ]

    def parseFile(self, filename):
        try:
            df = pd.read_csv(filename, sep=self.options.sep, parse_dates=['date'])
        except Exception as e:
            raise FailedToParse('Could not parse csv file: %s' % (str(e)))

        timerecords = []

        for idx, row in df.iterrows():
            tr_dict = {
                'startDate': int(row['date'].timestamp() * 1000),
                'projectId': str(row['projectId']),
                'projectTaskId': str(row['projectTaskId']),
                'durationSeconds': row['durationSeconds'] * 3600,
                'description': row['description'],
            }

            timerecords.append(WeclappTimeRecord(**tr_dict))
        return timerecords

parsers = [
    { 'name': 'simplecsv', 'parser': MySimpleCSV, 'default': True },
]
```

**Display list of parsers**

    $ weclapp-cli upload --list
    simplecsv
    csv

**Display command line arguments for your parser**

    $ weclapp-cli upload --parser simplecsv --list-parser-options
    Parser: simplecsv

    KEY            VALUE          DESCRIPTION
    -----------------------------------------
    sep            ;              CSV separator


    use --po "KEY:VAL" to set an option. You can use --po multiple times

If your parser is the default, you don't need to pass `--parser simplecsv`


[1]: https://github.com/shaoran/weclapp-cli/blob/master/weclapp/models/timeRecord.py#L13
