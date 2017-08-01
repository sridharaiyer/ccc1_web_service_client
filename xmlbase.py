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
from header import Header


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
        self.header = Header(z.filestr_decoded(self.path))
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
            elem.text = self.claimid

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
        self.savefile.save_input(bytes(self))

        print('Posting XML to web service: {}'.format(self.header.get_url))
        HttpClient.set_default_header(**self.header.header_dict)
        self.response = HttpClient().post(self.header.get_url, bytes(self))
        print('Response for {} {} - {}'.format(self.env, self.est, self.response))
        response_xml = XMLUtils(self.response.text)

        self.savefile.save_response(str(response_xml))

        if self._type == 'StatusChange':
            self.verify_db()

    def verify_db(self):
        print('Start DB verification after posting StatusChange successfully')
        match_file_type = {
            'Workfile': '2',
            'DigitalImage': '3',
            'EstimatePrintImage': '4',
            'RelatedPriorDamagereport': '52',
            'UnrelatedPriorDamage': '6',
        }
        sqls = (
            """SELECT * FROM CLAIM_FOLDER_DETAIL WHERE DL_CLM_FOLDER_ID IN (SELECT DL_CLM_FOLDER_ID FROM CLAIM_FOLDER WHERE CUST_CLM_REF_ID='{}') AND CLM_FOLDER_MATCH_FILE_TYP = '{}' AND EST_LINE_IND = '{}'""",
            """SELECT * FROM BILLING_MESSAGE WHERE CLAIM_REF_ID='{}' AND MATCH_FILE_TYP = '{}' AND EST_IND = '{}'"""
        )

        for ftype, value in match_file_type.items():
            for sql in sqls:
                self.db.claimfolder.wait_until_exists(
                    sql.format(self.claimid, value, self.est))
