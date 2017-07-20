import os.path


class Save(object):
    """docstring for Save"""

    def __init__(self, claimid=None, est=None, filetype=None, env=None):
        self.claimid = claimid
        if est is None:
            self.est = 'Assignment'
        else:
            self.est = est
        self.filetype = filetype
        self.env = env

    def save_input(self, data):
        path = self._create_path('input')
        print('Saving input file - {}'.format(path))
        with open(path, 'wb') as f:
            f.write(data)

    def save_response(self, data):
        path = self._create_path('response')
        print('Saving response - {}'.format(path))
        with open(path, 'w') as f:
            f.write(data)

    def _create_path(self, locationtype):
        base_path = 'target/{}/{}/{}'.format(self.claimid, self.env, locationtype)
        base_path = os.path.join(base_path, self.est)
        filename = self.est + '_' + self.filetype + '_' + locationtype + '.xml'

        os.makedirs(base_path, exist_ok=True)
        return os.path.join(base_path, filename)
