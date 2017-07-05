from abc import ABC


class XMLBase(ABC):

    def __init__(self, **params):
        self.env = params['env']
        print(self.env)


class Workfile(XMLBase):
    def __init__(self, **params):
        super().__init__(**params)
        self.clsname = self.__class__.__name__
# further class methods


class EstimatePrintImage(XMLBase):
    def __init__(self, **params):
        super().__init__(self, **params)
        self.clsname = self.__class__.__name__
# further class methods


XML_TYPE = {
    'Workfile': Workfile,
    'EstimatePrintImage': EstimatePrintImage,
}


class XMLFactory(object):
    @staticmethod
    def factory(cls, **params):
        return XML_TYPE[cls](**params)


params = {
    "filename": "Fiddler_Captures/RF-TESTRFS02APR17-S02.saz",
    "env": "awsqa",
    "claimid": "eqa20170705115945",
    "appr": "rf",
    "lname": "Saucedo",
    "fname": "Dena"}

if __name__ == '__main__':
    XMLFactory.factory('Workfile', est='E01', path='path', **params)
