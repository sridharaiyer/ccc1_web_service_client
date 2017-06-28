import importlib
import pdb
from references import References


class NoEstimateDictError(Exception):
    def __str__(self):
        return ('The estimate_dict property has not been assigned.')


class WebServiceEngine(object):
    """docstring for WebServiceFiles"""

    def __init__(self, **params):
        self.params = params
        self._estimate_dict = None

    @property
    def ref_dict(self):
        return References(self.estimate_dict).ref_dict

    @property
    def estimate_dict(self):
        return self._estimate_dict

    @estimate_dict.setter
    def estimate_dict(self, est_dict):
        self._estimate_dict = est_dict

    @property
    def generate(self):
        if self._estimate_dict is None:
            raise NoEstimateDictError
        for est, files in self.estimate_dict.items():
            for classname, path in files.items():
                my_module = importlib.import_module('webservices.' + classname.lower())
                yield getattr(my_module, classname).from_kwargs(est=est, path=path, ref_dict=self.ref_dict, **self.params)

    def run(self):
        for ws in self.generate:
            ws.create_xml()
            ws.send_xml()
            ws.verify_db()
