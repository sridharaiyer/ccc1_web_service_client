import uuid
import pdb
from collections import defaultdict


class References(object):
    """docstring for References"""

    def __init__(self, est_dict):
        self.est_dict = est_dict
        self._ref_dict = defaultdict(dict)

    @property
    def ref_dict(self):
        for est, files in self.est_dict.items():
            for classname, path in files.items():
                self._ref_dict[est][classname] = str(uuid.uuid4())
        return self._ref_dict
