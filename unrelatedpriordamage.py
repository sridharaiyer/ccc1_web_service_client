from xmlbase import XMLBase


class UnrelatedPriorDamage(XMLBase):

    def __init__(self, **params):
        super().__init__(self, **params)
        self.clsname = self.__class__.__name__

    @classmethod
    def from_kwargs(cls, **kwargs):
        obj = cls()
        for (field, value) in kwargs.items():
            setattr(cls, field, value)
        return obj

    def create_xml(self):
        print('Preparing the {} XML file located in {} in the fiddler session'.format(self.clsname, self.path))

    def send_xml(self):
        print('Sending the {} XML file to endpoint'.format(self.clsname))

    def verify_db(self):
        print('Verifying the DB after posting the {} XML file'.format(self.clsname))
