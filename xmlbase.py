from abc import ABC
from abc import abstractmethod
import os.path
import datetime
import pytz
import uuid
import enum
import pdb
from httpclient import HttpClient
from properties import Properties
from xmlutils import XMLUtils
from workfile import Workfile
from estimateprintimage import EstimatePrintImage
from digitalimage import DigitalImage
from unrelatedpriordamage import UnrelatedPriorDamage
from relatedpriordamagereport import RelatedPriorDamagereport
from statuschange import StatusChange


class FileType(enum.Enum):
    inputXML = 'input'
    outputXML = 'output'


class IncorrectXMLFiletype(Exception):

    def __str__(self):
        return ('Incorrect XML file type. Specify either FileType.inputXML or FileType.outputXML')

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


class XMLBase(ABC):

    def __init__(self, **params):
        print('In the XMLBase __init__')
        self.properties = Properties(self.env)
        self._xml = XMLUtils(self.path)

    now = datetime.datetime.now(pytz.timezone('US/Central'))
    time_iso = now.isoformat()
    time_ymdhms = now.strftime('%Y-%m-%dT%H:%M:%S')
    time_ymd = now.strftime('%Y-%m-%d')

    time_utc = datetime.datetime.utcnow()
    time_utc = time_utc.replace(tzinfo=pytz.timezone('US/Central')).isoformat()
    time_zulu = time_utc + 'Z'

    # @property
    # def claimid(self):
    #     return self._claimid

    # @property
    # def env(self):
    #     return self._env

    # @property
    # def lname(self):
    #     return self._lname

    # @property
    # def fname(self):
    #     return self._fname

    def __repr__(self):
        return str(self.xml)
        pdb.set_trace()
        # return('Webservice: {}, Env: {}, Est_Type: {}, Path: {}'.format(self.clsname, self.env, self.est, self.path))

    @abstractmethod
    def create_xml(self):
        pass

    @property
    def xml(self):
        return self._xml

    def send_xml(self):
        url = self.web_service_url

        print('Saving input file')
        self._save_xml(FileType.inputXML)
        print('Posting XML to web service: {}'.format(url))
        self.response = HttpClient().post(url, bytes(self))
        print('Assignment XML successfully posted to web service')
        print('Saving output file')
        self._save_xml(FileType.outputXML)

    @abstractmethod
    def verify_db(self):
        pass

    # def _save_file(self, path):
    #     with open(path, 'wb') as f:
    #         f.write(bytes(self))

    def _save_xml(self, filetype):
        xml_type = self.__class__.__name__.lower()
        filename = None
        base_path = 'target/{}/{}/{}'.format(self.claimid,
                                             filetype.value, self.env)
        if xml_type == 'assignment':
            base_path = os.path.join(base_path, xml_type)
        else:
            base_path = os.path.join(base_path, self.estimate_type, xml_type)

        if xml_type == 'assignment':
            filename = xml_type + '.xml'
        elif xml_type == 'event':
            num_of_files = len(os.listdir(base_path))
            if num_of_files == 0:
                filename = xml_type + '_1' + '.xml'
            else:
                filename = xml_type + '_' + str(num_of_files + 1) + '.xml'
            if os.path.exists():
                pass

        os.makedirs(base_path, exist_ok=True)
        path = os.path.join(base_path, filename)
        print('Saving file - {}'.format(path))
        if filetype.value == 'input':
            with open(path, 'wb') as f:
                f.write(bytes(self))
        else:
            with open(path, 'w') as f:
                f.write(self.response.text)

    # @abc.abstractmethod
    # def modifyXML(self, root=root):
    #     tag_dict = {}
    #     tag_dict['.//{*}SourceTimeStamp'] = self._time_iso
    #     tag_dict['.//{*}PublishTimeStamp'] = self._time_iso
    #     tag_dict['.//{*}ClaimNumber'] = CreateXML.claim_id
    #     tag_dict['.//{*}ClaimReferenceID'] = self.claim_id
    #     tag_dict['.//{*}clm_num'] = self.claim_id
    #     tag_dict['.//{*}Party//{*}FirstName'] = self.name['owner_first_name']
    #     tag_dict['.//{*}Party//{*}LastName'] = self.name['owner_last_name']
    #     tag_dict['.//{*}owner_info//{*}owner_first_name'] = self.name['owner_first_name']
    #     tag_dict['.//{*}owner_info//{*}owner_last_name'] = self.name['owner_last_name']

    #     self.replace_tag(root=root, **tag_dict)

    # @staticmethod
    # def decode_ungzip(data):
    #     decoded_base64 = base64.b64decode(data)
    #     gzcontent = gzip.GzipFile(fileobj=BytesIO(
    #         decoded_base64)).read().decode('UTF-8')
    #     return gzcontent

    # @property
    # @staticmethod
    # def gzip_encode(data):
    #     gzip_compressed = gzip.compress(data)
    #     encoded_payload = (base64.b64encode(gzip_compressed)).decode('UTF-8')
    #     return encoded_payload

    # @staticmethod
    # def root_to_string(root=root):
    #     return ET.tostring(root, pretty_print=True)

    # @abc.abstractmethod
    # def change_reference(self, root=root, ref=None):
    #     for elem in root.iterfind('.//{*}Reference'):
    #         elem.text = re.sub('[^/]*$', ref, elem.text)

    # @staticmethod
    # def base64_decode():
    #     pass

    # @staticmethod
    # def base64_encode():
    #     pass

    # @classmethod
    # def save_xml(cls):
    #     pass
