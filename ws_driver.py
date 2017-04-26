class RunService(object):
    """Executes the web service calls for the file"""

    def __init__(self, filename):
        self._filename = filename

    @property
    def filename(self):
        return self._filename

    @property
    def execute(self):
        print('Running the web service for: {}'.format(self.filename))
