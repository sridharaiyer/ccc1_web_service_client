from abc import ABC
from abc import abstractmethod
import os.path
import datetime
import pytz
import enum
import pdb
import json
from httpclient import HttpClient
from properties import Properties
from xmlutils import XMLUtils
import re
from savefile import Save


class FileType(enum.Enum):
    inputXML = 'input'
    outputXML = 'output'


class IncorrectXMLFiletype(Exception):

    def __str__(self):
        return ('Incorrect XML file type. Specify either FileType.inputXML or FileType.outputXML')


class XMLBase(ABC):

    def __init__(self, **params):
        self.__dict__.update(params)
        self.properties = Properties(self.env)
        self._xml = XMLUtils.fromZipFile(zipfilename=self.filename, xmlpath=self.path)
        self._type = self.__class__.__name__
        self.savefile = Save(claimid=self.claimid, est=self.est, filetype=self._type, env=self.env)

    now = datetime.datetime.now(pytz.timezone('US/Central'))
    time_iso = now.isoformat()
    time_ymdhms = now.strftime('%Y-%m-%dT%H:%M:%S')
    time_ymd = now.strftime('%Y-%m-%d')

    time_utc = datetime.datetime.utcnow()
    time_utc = time_utc.replace(tzinfo=pytz.timezone('US/Central')).isoformat()
    time_zulu = time_utc + 'Z'

    def __repr__(self):
        return('Webservice: {}, Env: {}, Est_Type: {}, Path: {}'.format(self.clsname, self.env, self.est, self.path))

    @abstractmethod
    def create_xml(self):
        pass

    @property
    def xml(self):
        return self._xml

    def send_xml(self):
        print('Saving input:')
        self.savefile.save_input(bytes(self))
        # url = self.web_service_url
        print('Posting XML to web service: {}'.format(self.properties.ws[self._type]))
        # self.response = HttpClient().post(url, bytes(self))
        print('Assignment XML successfully posted to web service')
        print('Saving output file')
        # self._save_xml(FileType.outputXML)

    @abstractmethod
    def verify_db(self):
        pass


class Workfile(XMLBase):
    def __init__(self, **params):
        super().__init__(**params)

    def create_xml(self):
        print('Preparing the {} XML file located in {} in the fiddler session'.format(self._type, self.path))

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

        tempsavefile = Save(claimid=self.claimid, est=self.est, filetype='WorkfilePayload', env=self.env)
        tempsavefile.save_input(bytes(payload_xml))

        encoded_gzipped_data = XMLUtils.gzip_encodebase64(bytes(payload_xml))

        self.xml.edit_tag(Data=encoded_gzipped_data)

        for elem in self.xml.root.iterfind('.//{*}Reference'):
            elem.text = re.sub(
                '[^/]*$', self.ref_dict[self.est][self._type], elem.text)

    def __bytes__(self):
        return bytes(self.xml)

    def verify_db(self):
        print('Verifying the DB after posting the {} {} XML file'.format(self.est, self._type))


class UnrelatedPriorDamage(XMLBase):

    def __init__(self, **params):
        super().__init__(**params)

    def create_xml(self):
        print('Preparing the {} {} XML file located in {} in the fiddler session'.format(self.est, self._type, self.path))

    def __bytes__(self):
        return bytes(self.xml)

    def send_xml(self):
        print('Sending the {} {} XML file to endpoint'.format(self.est, self._type))

    def verify_db(self):
        print('Verifying the DB after posting the {} {} XML file'.format(self.est, self._type))


class StatusChange(XMLBase):

    def __init__(self, **params):
        super().__init__(**params)

    def create_xml(self):
        print('Preparing the {} {} XML file located in {} in the fiddler session'.format(self.est, self._type, self.path))

    def __bytes__(self):
        return bytes(self.xml)

    def send_xml(self):
        print('Sending the {} {} XML file to endpoint'.format(self.est, self._type))

    def verify_db(self):
        print('Verifying the DB after posting the {} {} XML file'.format(self.est, self._type))


class RelatedPriorDamagereport(XMLBase):

    def __init__(self, **params):
        super().__init__(**params)

    def create_xml(self):
        print('Preparing the {} {} XML file located in {} in the fiddler session'.format(self.est, self._type, self.path))

    def __bytes__(self):
        return bytes(self.xml)

    def send_xml(self):
        print('Sending the {} {} XML file to endpoint'.format(self.est, self._type))

    def verify_db(self):
        print('Verifying the DB after posting the {} {} XML file'.format(self.est, self._type))


class EstimatePrintImage(XMLBase):

    def __init__(self, **params):
        super().__init__(**params)

    def create_xml(self):
        print('Preparing the {} {} XML file located in {} in the fiddler session'.format(self.est, self._type, self.path))

    def __bytes__(self):
        return bytes(self.xml)

    def send_xml(self):
        print('Sending the {} {} XML file to endpoint'.format(self.est, self._type))

    def verify_db(self):
        print('Verifying the DB after posting the {} {} XML file'.format(self.est, self._type))


class DigitalImage(XMLBase):

    def __init__(self, **params):
        super().__init__(**params)

    def create_xml(self):
        print('Preparing the {} {} XML file located in {} in the fiddler session'.format(self.est, self._type, self.path))

    def __bytes__(self):
        return bytes(self.xml)

    def send_xml(self):
        print('Sending the {} {} XML file to endpoint'.format(self.est, self._type))

    def verify_db(self):
        print('Verifying the DB after posting the {} {} XML file'.format(self.est, self._type))


XML_TYPE = {
    'Workfile': Workfile,
    'EstimatePrintImage': EstimatePrintImage,
    'DigitalImage': DigitalImage,
    'UnrelatedPriorDamage': UnrelatedPriorDamage,
    'RelatedPriorDamagereport': RelatedPriorDamagereport,
    'StatusChange': StatusChange,
}


class XMLFactory(object):
    @staticmethod
    def factory(cls, **params):
        return XML_TYPE[cls](**params)
