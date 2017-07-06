from abc import ABC
from abc import abstractmethod
import datetime
import pytz
import enum
import pdb
import json
from httpclient import HttpClient
from properties import Properties
from xmlutils import XMLUtils
from savefile import Save
import re


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

    def _init_message(self):
        print('Preparing the {} {} XML file located in {} in the fiddler session'.format(self.est, self._type, self.path))

    def edit_descriptor(self):
        self.xml.edit_tag(Password='Password1')

        for elem in self.xml.root.iterfind('.//{*}SourceTimeStamp'):
            elem.text = self.time_iso
        for elem in self.xml.root.iterfind('.//{*}PublishTimeStamp'):
            elem.text = self.time_iso
        for elem in self.xml.root.iterfind('.//{*}ClaimReferenceID'):
            elem.text = self.time_iso

    def edit_reference(self):
        for elem in self.xml.root.iterfind('.//{*}Reference'):
            elem.text = re.sub(
                '[^/]*$', self.ref_dict[self.est][self._type], elem.text)

    @abstractmethod
    def edit_xml(self):
        self._init_message()

    @property
    def xml(self):
        return self._xml

    def __bytes__(self):
        return bytes(self.xml)

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
