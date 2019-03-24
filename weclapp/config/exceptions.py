class ConfigError(Exception):
    """Base class for config exceptions"""

    def __init__(self, *args, path=None):
        if path is not None:
            cfg = 'config path: %s' % path
            print(len(args))
            if len(args) == 1:
                args = ("%s -- %s" % (args[0], cfg),)
            else:
                args = list(args)
                args.append(cfg)
                args = tuple(args)

        super().__init__(*args)



class ConfigNotFound(ConfigError):
    """
    Configuration file was not found
    """
    pass

class ConfigCannotWrite(ConfigError):
    """
    Configuration file cannot be written
    """
    pass

class ConfigParsedFailed(ConfigError):
    """
    Configurattion cannot be parsed
    """
    pass

class ConfigUnableToRead(ConfigError):
    """
    unable to read interactively from user
    """
    pass


__all__ = [ 'ConfigNotFound', 'ConfigCannotWrite', 'ConfigParsedFailed', 'ConfigUnableToRead' ]
