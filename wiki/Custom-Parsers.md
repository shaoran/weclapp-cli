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

## Minimal example

[1]: https://github.com/shaoran/weclapp-cli/blob/master/weclapp/models/timeRecord.py#L13
