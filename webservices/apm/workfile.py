from xmlbase import XMLBase
from xmlutils import XMLUtils
import json
import pdb
import re
from savefile import Save


class Workfile(XMLBase):
    def __init__(self, **params):
        super().__init__(**params)

    def edit_xml(self):
        super().edit_xml()
        super().edit_descriptor()
        super().edit_reference()

        payload = self.xml.gettext(tag='Data')
        payload_xml = XMLUtils(XMLUtils.decodebase64_ungzip(payload))
        payload_xml.edit_tag(ClaimNumber=self.claimid)
        payload_xml.edit_tag(ClaimReferenceID=self.claimid)
        payload_xml.edit_tag(clm_num=self.claimid)

        for elem in payload_xml.root.iterfind('.//{*}Party//{*}FirstName'):
            elem.text = self.fname

        for elem in payload_xml.root.iterfind('.//{*}Party//{*}LastName'):
            elem.text = self.lname

        for elem in payload_xml.root.iterfind('.//{*}owner_info//{*}owner_first_name'):
            elem.text = self.fname

        for elem in payload_xml.root.iterfind('.//{*}owner_info//{*}owner_last_name'):
            elem.text = self.lname

        for elem in payload_xml.root.iterfind('.//{*}ImageReference'):
            elem.text = re.sub(
                '[^/]*$', self.ref_dict[self.est]['DigitalImage'], elem.text)
        # --------------------------------------------------------------------
        # Modifying the ref of previous images for S01 Workfile and above
        est_id = None
        if self.est != 'E01':
            for elem in payload_xml.root.iterfind('.//{*}Image'):
                for estid_elem in elem.iterfind('.//{*}EstID'):
                    est_id = estid_elem.text
                for r_elem in elem.iterfind('.//{*}ImageReference'):
                    if int(est_id) == 51:
                        est = 'E01'
                    else:
                        est = 'S' + str(est_id)[-2:]
                    dig_img_ref = self.ref_dict[est]['DigitalImage']
                    r_elem.text = re.sub('[^/]*$', dig_img_ref, r_elem.text)
        # --------------------------------------------------------------------

        tempsavefile = Save(claimid=self.claimid, est=self.est, filetype='WorkfilePayload', env=self.env)
        tempsavefile.save_input(bytes(payload_xml))

        encoded_gzipped_data = XMLUtils.gzip_encodebase64(bytes(payload_xml))

        self.xml.edit_tag(Data=encoded_gzipped_data)
