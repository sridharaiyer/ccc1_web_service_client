from xmlbase import XMLBase
from xmlutils import XMLUtils
import re
import pdb
import json


class StatusChange(XMLBase):

    def __init__(self, **params):
        super().__init__(**params)

    def edit_xml(self):
        super().edit_xml()
        super().edit_descriptor()

        for file, oldref in self.old_ref_dict[self.est].items():
            xpath = '//text()[contains(.,\"' + oldref + '\")]/ancestor::*[local-name()="Payload"]/*[local-name()="Data"]'
            payload_data = self.xml.root.xpath(xpath)[0].text

            decoded_decoded_payload_data = XMLUtils.decodebase64(payload_data).decode()
            payload_xml = XMLUtils(decoded_decoded_payload_data)
            for elem in payload_xml.root.iterfind('.//{*}Reference'):
                elem.text = re.sub(
                    '[^/]*$', self.ref_dict[self.est][file], elem.text)
            base64encoded_payload = XMLUtils.encodebase64(bytes(payload_xml))

            self.xml.root.xpath(xpath)[0].text = base64encoded_payload

            xpath = '//text()[contains(.,\"' + oldref + '\")]/ancestor::*[local-name()="Reference"]'

            old_reference = self.xml.root.xpath(xpath)[0].text
            new_reference = re.sub(
                '[^/]*$', self.ref_dict[self.est][file], old_reference)
            self.xml.root.xpath(xpath)[0].text = new_reference

    def verify_db(self):
        print('Verifying the DB after posting the {} {} XML file'.format(self.est, self._type))
