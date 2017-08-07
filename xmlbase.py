from abc import ABC
from abc import abstractmethod
from httpclient import HttpClient
from properties import Properties
from xmlutils import XMLUtils
from savefile import Save
import re
from db import DB
from timeutils import Time
from zipfileutils import ZipFileUtils
from header import Header
import pdb
import logging

logger = logging.getLogger()


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
        logger.INFO('Preparing the {} {} XML file located in {} in the fiddler session'.format(
            self.est, self._type, self.path))

        for elem in self.xml.root.iterfind('.//{*}TransformationHeader'):
            elem.text = elem.text.replace("\\n", "")

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
        logger.INFO('Posting XML to web service: {}'.format(self.header.get_url))
        HttpClient.set_default_header(**self.header.header_dict)
        self.response = HttpClient().post(self.header.get_url, bytes(self))
        logger.INFO('Response for {} {} - {}'.format(self.env, self.est, self.response))
        response_xml = XMLUtils(self.response.text)

        self.savefile.save_response(str(response_xml))

        if self._type == 'StatusChange':
            self.verify_db()

    def verify_db(self):
        logger.INFO('Start DB verification after posting StatusChange successfully')
        match_file_type = {
            'Workfile': '2',
            'DigitalImage': '3',
            'Estimatelogger.INFOImage': '4',
            'RelatedPriorDamagereport': '52',
            'UnrelatedPriorDamage': '6',
        }
        sqls = (
            """SELECT * FROM CLAIM_FOLDER_DETAIL WHERE DL_CLM_FOLDER_ID IN (SELECT DL_CLM_FOLDER_ID FROM CLAIM_FOLDER WHERE CUST_CLM_REF_ID='{}') AND CLM_FOLDER_MATCH_FILE_TYP = '{}' AND EST_LINE_IND = '{}'""",
            """SELECT * FROM BILLING_MESSAGE BILLING
                    INNER JOIN CLAIM_FOLDER_DETAIL CFD ON CFD.DL_CLM_FOLDER_MATCH_ID = BILLING.CLM_FOLDER_MATCH_FILE_ID
                    WHERE CFD.DL_CLM_FOLDER_ID IN (SELECT DL_CLM_FOLDER_ID FROM CLAIM_FOLDER WHERE CUST_CLM_REF_ID='{}')
                    AND CFD.CLM_FOLDER_MATCH_FILE_TYP={} AND CFD.EST_LINE_IND= '{}'"""
        )

        for ftype, value in match_file_type.items():
            for sql in sqls:
                logger.INFO('Executing query:')
                logger.INFO(sql.format(self.claimid, value, self.est))
                pdb.set_trace()
                self.db.claimfolder.wait_until_exists(
                    sql.format(self.claimid, value, self.est))
