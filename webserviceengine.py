import pdb
from xmlfactory import XMLFactory
from collections import defaultdict
import uuid
import json
import logging

logger = logging.getLogger()


class NoEstimateDictError(Exception):
    def __str__(self):
        return ('The estimate_dict property has not been assigned.')


class WebServiceEngine(object):
    """docstring for WebServiceFiles"""

    def __init__(self, estimate_dict, old_ref_dict, **params):
        self.params = params
        self._estimate_dict = estimate_dict
        self._old_ref_dict = old_ref_dict
        self._create_ref_dict()

    def _create_ref_dict(self):
        self._ref_dict = defaultdict(dict)
        for est, files in self._estimate_dict.items():
            for file, path in files.items():
                if file != 'StatusChange':
                    self._ref_dict[est][file] = str(uuid.uuid4())

    @property
    def ref_dict(self):
        return self._ref_dict

    @property
    def estimate_dict(self):
        return self._estimate_dict

    @property
    def generate(self):
        logger.info('Reference IDs: \n{}'.format(json.dumps(self.ref_dict, indent=4)))
        if self._estimate_dict is None:
            raise NoEstimateDictError
        for est, files in self.estimate_dict.items():
            for classname, path in files.items():
                new_params = {
                    'estimate_dict': self._estimate_dict,
                    'est': est,
                    'path': path,
                    'ref_dict': self.ref_dict,
                    'old_ref_dict': self._old_ref_dict
                }
                param_dict = dict(new_params, **self.params)
                yield XMLFactory.factory(classname, **param_dict)

    def run(self):
        for ws in self.generate:
            ws.edit_xml()
            ws.send_xml()
