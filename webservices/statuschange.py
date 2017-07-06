from xmlbase import XMLBase
from savefile import Save


class StatusChange(XMLBase):

    def __init__(self, **params):
        super().__init__(**params)

    def edit_xml(self):
        super().edit_xml()
        super().edit_descriptor()

    def verify_db(self):
        print('Verifying the DB after posting the {} {} XML file'.format(self.est, self._type))
