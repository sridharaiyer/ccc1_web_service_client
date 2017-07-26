from xmlbase import XMLBase


class EstimatePrintImage(XMLBase):

    def __init__(self, **params):
        super().__init__(**params)

    def edit_xml(self):
        super().edit_xml()
        super().edit_descriptor()
        super().edit_reference()
