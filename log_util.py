import logging


class Singleton(object):
    """
    Singleton interface:
    http://www.python.org/download/releases/2.2.3/descrintro/#__new__
    """
    def __new__(cls, *args, **kwds):
        it = cls.__dict__.get("__it__")
        if it is not None:
            return it
        cls.__it__ = it = object.__new__(cls)
        it.init(*args, **kwds)
        return it

    def init(self, *args, **kwds):
        pass


class LoggerManager(Singleton):
    def init(self, loglevel):
        self.logger = logging.getLogger()
        self.logger.handlers = []
        handler = logging.StreamHandler()

        self.logger.setLevel(loglevel)
        formatter = logging.Formatter(
            fmt='[%(asctime)s] [%(levelname)s] %(message)s',
            datefmt='%F %H:%M:%S'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def debug(self, msg):
        self.logger.debug(msg)

    def error(self, msg):
        self.logger.error(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)


class Logger(Singleton):
    """
    Logger object.
    """

    def __init__(self, loglevel):
        self.lm = LoggerManager(loglevel)  # LoggerManager instance

    def debug(self, msg):
        self.lm.debug(msg)

    def error(self, msg):
        self.lm.error(msg)

    def info(self, msg):
        self.lm.info(msg)

    def warning(self, msg):
        self.lm.warning(msg)
