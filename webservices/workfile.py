from xmlbase import XMLBase
from xmlutils import XMLUtils
import json
import pdb
import re


class Workfile(XMLBase):
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

        self.xml.edit_tag(Password='Password1')
        self.xml.edit_tag(SourceTimeStamp=super().time_iso)
        self.xml.edit_tag(PublishTimeStamp=super().time_iso)
        self.xml.edit_tag(ClaimReferenceID=self.claimid)

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

    def send_xml(self):
        print('Sending the {} XML file to endpoint'.format(self.clsname))

    def verify_db(self):
        print('Verifying the DB after posting the {} XML file'.format(self.clsname))
