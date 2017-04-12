from xmlbase import CreateXML


class Workfile(CreateXML):
    """docstring for Workfile"""

    def __init__(self, filename):
        _filename = filename
        _uuid = str(uuid.uuid4())
        super(Workfile, self).__init__()

    @property
    def uuid(self):
        return self._uuid
