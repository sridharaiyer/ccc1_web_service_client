from abc import ABCMeta, abstractmethod


class WebServiceBase(object):
    """docstring for WebServiceBase"""

    def __init__(self, arg):
        super(WebServiceBase, self).__init__()
        self.arg = arg

    __metaclass__ = ABCMeta
