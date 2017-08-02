# import logging

# logger = logging.getLogger()
# logger.handlers = []
# handler = logging.StreamHandler()
# formatter = logging.Formatter('[%(asctime)s]   %(message)-30s', datefmt='%Y-%m-%d %H:%M:%S')
# handler.setFormatter(formatter)
# logger.addHandler(handler)
# logger.setLevel(logging.INFO)


# logger.info('Hello world!')

import logging
import pdb


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
    def init(self):
        self.logger = logging.getLogger()
        self.logger.handlers = []
        handler = logging.StreamHandler()

        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter(
            fmt='[%(asctime)s] [%(levelname)s] %(message)s',
            datefmt='%F %H:%M:%S'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def debug(self, msg):
        self.logger = logging.getLogger()
        self.logger.debug(msg)

    def error(self, msg):
        self.logger = logging.getLogger()
        self.logger.error(msg)

    def info(self, msg):
        self.logger = logging.getLogger()
        self.logger.info(msg)

    def warning(self, msg):
        self.logger = logging.getLogger()
        self.logger.warning(msg)


class Logger(object):
    """
    Logger object.
    """

    def __init__(self):
        self.lm = LoggerManager()  # LoggerManager instance

    def debug(self, msg):
        self.lm.debug(msg)

    def error(self, msg):
        self.lm.error(msg)

    def info(self, msg):
        self.lm.info(msg)

    def warning(self, msg):
        self.lm.warning(msg)


if __name__ == '__main__':

    logger = Logger()
    logger.debug("this testname.")
    pdb.set_trace()
    logger.info('Hello world!')
