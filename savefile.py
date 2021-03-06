import os.path
import logging

logger = logging.getLogger()


class Save(object):
    """docstring for Save"""

    def __init__(self, claimid=None, est=None, filetype=None, env=None):
        self.claimid = claimid
        self.est = est
        self.filetype = filetype
        self.env = env

    def save_input(self, data):
        path = self._create_path('input')
        logger.info('Saving input file - {}'.format(path))
        with open(path, 'wb') as f:
            f.write(data)

    def save_response(self, data):
        path = self._create_path('response')
        logger.info('Saving response - {}'.format(path))
        with open(path, 'w') as f:
            f.write(data)

    def _create_path(self, locationtype):
        base_path = 'target/{}/{}/{}'.format(self.claimid,
                                             self.env, locationtype)
        if self.est:
            base_path = os.path.join(base_path, self.est)
            filename = self.est + '_' + self.filetype + '_' + locationtype + '.xml'
        else:
            filename = self.filetype + '_' + locationtype + '.xml'

        os.makedirs(base_path, exist_ok=True)
        return os.path.join(base_path, filename)
