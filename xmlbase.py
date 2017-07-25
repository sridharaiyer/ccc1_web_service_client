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
from db import DB
from timeutils import Time
from zipfileutils import ZipFileUtils


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
        self._type = self.__class__.__name__
        z = ZipFileUtils(self.filename)
        self._xml = XMLUtils(z.filexml(self.path))
        filestr = z.filestr(self.path)
        self.soapaction = re.compile('SOAPAction: (.*)$').search(filestr).group(1)
        print(self.soapaction)
        pdb.set_trace()
        self.savefile = Save(claimid=self.claimid,
                             est=self.est,
                             filetype=self._type,
                             env=self.env)
        self._db = DB(self.env)
        self.time = Time()

    def __repr__(self):
        return('Webservice: {}, Env: {}, Est_Type: {}, Path: {}'.format(self.clsname, self.env, self.est, self.path))

    def _init_message(self):
        print('Preparing the {} {} XML file located in {} in the fiddler session'.format(
            self.est, self._type, self.path))

    def edit_descriptor(self):
        self.xml.edit_tag(Password='Password1')

        for elem in self.xml.root.iterfind('.//{*}SourceTimeStamp'):
            elem.text = self.time.iso
        for elem in self.xml.root.iterfind('.//{*}PublishTimeStamp'):
            elem.text = self.time.iso
        for elem in self.xml.root.iterfind('.//{*}ClaimReferenceID'):
            elem.text = self.time.iso

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

    @property
    def db(self):
        return self._db

    def __bytes__(self):
        return bytes(self.xml)

    def send_xml(self):
        print('Saving input:')
        self.savefile.save_input(bytes(self))

        if self._type in ['EstimatePrintImage', 'UnrelatedPriorDamage', 'RelatedPriorDamagereport']:
            filetype = 'PrintImage'
        else:
            filetype = self._type

        url = self.properties.ws[filetype]
        print('Posting XML to web service: {}'.format(url))
        self.response = HttpClient().post(url, bytes(self))
        print('Response for {} {} - {}'.format(self.env, self.est, self.response))
        pdb.set_trace()
        response_xml = XMLUtils(self.response.text)

        print('XML successfully posted to web service')
        print('Saving output file')
        self.savefile.save_response(str(response_xml))

    @abstractmethod
    def verify_db(self):
        pass
