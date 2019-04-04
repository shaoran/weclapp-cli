# WECLAP CLI

`weclapp-cli` is a limited command line interface to [weclapp][1]'s time records. I wrote this
tool because I want to upload several time records at once that have been stored in an Excel
sheet. The web interface allows you to upload a time record once at a time and when you have
several time records to upload, this can take a lot of time.

## Features

- Display the projects and the project tasks (with their respective IDs) for which you can
book time records
- Display the time records that you have already booked
- Upload time records from a CSV file
- Allows to use a custom CSV exporter

## Installation

**Note** As of this moment, the project is still in development and has not been uploaded to
[PyPI][2] yet, so the `pip` command will fail.

```bash
pip install weclapp-cli
```

### Requirement

- Python3.x

## Usage

In order to have access to weclapp's public API, you need a **API Token**. You can get your
API Token from the *My settings* page of your weclapp installation. If you don't have an API
Token yet, then click on *Create new API token* to generate a new one. Please think of your
API Token as a password, keep it secret!

### Configuring the client

`weclapp-cli` needs to be configured before you can start using it.
The default configuration path is `${HOME}/.config/weclapp-cli/config.yml`.

You'll need the following values:

- the domain of you weclapp installation, usually *`yourcomapny.weclapp.com`*
- the API path, usually *`/webapp/api/v1`*
- your API Token

Also check whether you have to access the API via HTTPS. Once you have all these values,
open a terminal and type in:

```bash
$ weclapp-cli config
Generating a new configuration file /home/shaoran/.config/weclapp-cli/config.yml
Your weclapp domain []: yourcomapny.weclapp.com<ENTER>
The API path [/webapp/api/v1]: <ENTER>
Your API TOKEN []: YOUR-TOKEN<ENTER>
Use SSL [yes]: <ENTER>
```

### List projects, tasks and the last 100 time records

```bash
$ weclapp-cli projects
```

### List projects, tasks only

```bash
$ weclapp-cli projects -t
```

### Uploading time records

Prepare the CSV file, then execute

```bash
$ weclapp-cli upload my-records.csv
```

To get the options (like the separator character) for the default parse, execute

```bash
$ weclapp-cli upload --list-parser-options
```

You can pass these option with the `--po KEY=VAL` option.


## The CSV file

In order to upload a time record, you'll need to store your time records in a CSV-like file.

I store my time records in an Excel sheet that has the following format:

![][time-sheet]

**NOTE** Do not add empty lines and lines with comments (usually lines beginning with `#`).

### The header

The first 2 rows are the header. It contains the project ID and the task ID for which you want
to upload your time records.

In the example above the cells  `A1` and `A2` are ignored, you can have any string you like.

The next two columns (`B` and `C`) define the task for which you want to upload time records. The next
two columns (`D` and `E`) define another task, etc. You can have as many tasks as you want. For every
task you need two columns. In the example above `B1` and `B2` have the project ID and the task ID for the
first task. `D1` and `D2` have the project ID and the task ID for the next task.

### The time records

From the third row onward you'll define the time records. On the `A` column set the date of the day. The next
cell contains the number of hours you've worked on the project and the next column is the description of
the time record. The description may be empty. The next column is for the next number of hours and so on.

The date colum (`A`) is parsed using [`dateutil.parser.parse`][3], so you can have different date formats,
for example:

- Thursday, 01/Feb
- 2019.02.01
- 02-01-2019

are recognized as **1st of February 2019**. If you omit the year, the current year is assumed.

By default the time of day of the records is 09:00. You can set another time by passing the
`--po timeStart 08:00` option to `weclapp-cli upload` command. You have to use the 24 hour format.

If you need that a single entry has a different time of day than the default: instead of just passing
the duration (number of hours) as single number, you can pass **`time/duration`**. For example: you want
a single entry in the `B` column to have a time of day of 08:30 with a duration of 3 hours. Then enter the
value **`08:30/5.00`**. Here you have to use the 24 hour format as well.

The default CSV will ignore time record that have an empty duration, in the image above `D5` is empty, so
that time record is ignored. The description can always be empty.

### Example

The resulting CSV file from the image above would be

    PROJECT ID;12345;;323234;
    TASK ID;6789;;11232;
    Tuesday, 01/ Jan;;;;
    Wednesday, 02/ Jan;4.00;some desc;4.00;something else
    Thursday, 03/ Jan;8.00;;;
    Friday, 04/ Jan;3.00;;5.00;wiki stuff
    Saturday, 05/ Jan;;;;
    Friday, 11/ Jan;;;;


## Custom CSV files

If you want to use a different CSV parser, then you can write your own and let `weclapp-cli` use it
instead of the default one.

Create a file `csv_exporter.py` in the same directory where the configuration file is stored
(by default in `${HOME}/.config/weclapp-cli`).


```python
# ${HOME}/.config/weclapp-cli/csv_exporter.py
from weclapp import Parser

class MyCustomCSV(Parser):
    """
    implement your parser here
    """
    pass

parsers = [
    { "name": "custom", "parser": MyCustomCSV },
]
```

The `csv_exporter.py` file **must** have a variable called `parsers`. This variable is used by
`weclapp-cli` to import your custom parser. And since it is a list, you *can* export more than
one custom parser. If you want to mark a custom parser as the new default, then add
`"default": True`

```
parsers = [
    { "name": "matrix", "parser": MyCustomCSV, "default": True },
]
```

To display the list of parsers, execute

```bash
$ weclapp-cli upload -l
csv
matrix
```

The first entry is the default parser.

To use the "*matrix*" parser:

```bash
$ weclapp-cli upload -p matrix file.csv
```

See [Custom Parsers][5] for information about custom parsers

# Contributions

I don't intend to keep adding features, because it already does everything **I** need. But hey,
this is a open source project, so you are welcome to fork it. If you have bug fixes, new features
or new parsers, then please send me pull request.

# Disclaimer

I do not own, develop [weclapp][1] and don't claim any copyright. weclapp is a product owned and
developed by [weclapp GmbH][4]. Any questions you have about weclapp, please go their website
[https://www.weclapp.com/][1], don't ask me.

**Use this tool at your own risk, I am not responsible for any data losses or damages
as a result of using this tool.**


**LICENSE**: GPL-2

[1]: https://www.weclapp.com/
[2]: https://pypi.org/
[3]: https://dateutil.readthedocs.io/en/stable/parser.html#dateutil.parser.parse
[time-sheet]: wiki/images/time-sheet.png
[4]: https://www.weclapp.com/de/impressum/
[5]: https://github.com/shaoran/weclapp-cli/wiki/Custom-Parsers
