import pdb
from references import References
from xmlfactory import XMLFactory


class NoEstimateDictError(Exception):
    def __str__(self):
        return ('The estimate_dict property has not been assigned.')


class WebServiceEngine(object):
    """docstring for WebServiceFiles"""

    def __init__(self, estimate_dict, **params):
        self.params = params
        self._estimate_dict = estimate_dict
        self._ref_dict = References(estimate_dict).ref_dict

    @property
    def ref_dict(self):
        return self._ref_dict

    @property
    def estimate_dict(self):
        return self._estimate_dict

    @property
    def generate(self):
        if self._estimate_dict is None:
            raise NoEstimateDictError
        for est, files in self.estimate_dict.items():
            for classname, path in files.items():
                yield XMLFactory.factory(classname, est=est, path=path, ref_dict=self.ref_dict, **self.params)

    def run(self):
        for ws in self.generate:
            ws.create_xml()
            ws.send_xml()
            ws.verify_db()
