from xmlbase import XMLBase


class DigitalImage(XMLBase):

    def __init__(self, **params):
        super().__init__(**params)
        self.cf = self.db.claimfolder

    def edit_xml(self):
        super().edit_xml()
        super().edit_descriptor()
        super().edit_reference()
