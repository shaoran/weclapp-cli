from argparse import Namespace

class Parser(object):
    """
    The basic parser class

    Every parser class has a static variable __options__ that contains
    the class options like CSV separator and others.

    __options__ is a list of tuples with this format:

        (name, default value, help string)

    The __init__ function of the base class will take or creating an
    argparse.Namespace object out of __options__ and the options passed
    to __init__()

    Override the setup() method to do custom initialization. See the
    documentation of setup for more information.
    """

    # (name, default value, help string)
    __options__ = []

    def __init__(self, options={}):
        """
        creates a new parser instance.

        params:

          options   a dictionary with user options. The options are
                    determined by the static variable __options__ of the
                    class

        The __init__ function calls setup()
        """

        def_opts = { o[0]: o[1] for o in type(self).__options__ }
        def_opts.update(options)
        self.options = Namespace(**def_opts)
        self.setup()

    def setup(self):
        """
        Do your custom initialization here.

        Override this class in your parser implementation
        """
        pass

    def parseFile(self, filename):
        """
        parse the file and return a weclapp.WeclappTimeRecord object.

        params:

          filename_or_fp   a filename

        If the file cannot be parsed, raise weclapp.FailedToParse

        Override this class in your parser implementation
        """
        pass

    @classmethod
    def parse_parse_options(cls, pos):
        """
        Parse parser options from argparse namespace
        """
        kwargs = {}

        for po in pos:
            try:
                idx = po.index('=')
            except:
                raise InvalidParserOptionFormat('Parser argument %s has wrong format' % po)

            key = po[0:idx].strip()
            val = po[idx+1:].strip()

            kwargs[key] = val

        return kwargs
