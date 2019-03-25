import os
import yaml

from .exceptions import *

def_config=os.path.join(os.path.expanduser('~'), ".config", "weclapp-cli", "config.yml")

class Config(object):
    """
    Handles reading and writing the configuration
    """

    # (key, help, default)
    config_values = (
        ('domain', 'Your weclapp domain', None),
        ('path', 'The API path', '/webapp/api/v1'),
        ('apitoken', 'Your API TOKEN', None),
    )

    def __init__(self, path=def_config):
        self.path = path
        self.config = None

    def parse(self):
        """
        Returns if the config file is parsed
        """

        if not os.path.exists(self.path):
            raise ConfigNotFound("Config file cannot be found", path=self.path)

        try:
            fp = open(self.path, "r")
            self.config = yaml.load(fp)
        except Exception as e:
            raise ConfigParsedFailed("Could not open config file: %s" % str(e), path=self.path)


    def interactive_config(self, verbose=True, **kwargs):
        """
        Ask interactively for config values

        If verbose is set to True and a config value is not None, then this function
        will still ask with a default value. If the user enters an empty string, then
        this function will assume the default value. If verbose is set to False,
        then this function will use the passed value without asking the user.

        Valid kwargs can be determined by executing

            from weclapp import Config
            print(Config.config_values)

        from the python console

        On success returns the a new config
        """
        config = {}

        for key, helptext, default in self.config_values:
            val = kwargs.get(key, None)

            if val is not None and verbose is False:
                config[key] = val
                continue

            if val is not None:
                default = val

            msg = helptext
            if default is not None:
                msg = "%s [%s]" % (msg,default)

            keep_reading = True

            while keep_reading:
                try:
                    newval = input("%s: " % msg).strip()
                except Exception as e:
                    raise ConfigUnableToRead("Unable to read from user: %s" % str(e))

                if newval == '' and default is None:
                    continue # keep asking
                elif newval == '':
                    newval = default

                keep_reading = False

            config[key] = newval

        return config

    def set_new_config(self, config):
        self.config = config

    def save(self):
        pass
