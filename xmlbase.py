from abc import ABC
from abc import abstractmethod
from bs4 import BeautifulSoup
import re
import zipfile
from collections import defaultdict
import json
import os.path
from lxml import etree as ET
import base64
import gzip
from io import BytesIO
import datetime
import pytz
import names
from hamcrest import assert_that, equal_to
import uuid
from collections.abc import Mapping
import enum
import pdb
from httpclient import HttpClient


class FileType(enum.Enum):
    inputXML = 'input'
    outputXML = 'output'


class IncorrectXMLFiletype(Exception):
    def __str__(self):
        return ('Incorrect XML file type. Specify either FileType.inputXML or FileType.outputXML')


# class SaveXML(object):
#     """docstring for SaveXML"""

#     def __init__(self, filetype, path):
#         path =

#     def save(self):
#         pass


class XMLBase(ABC):

    now = datetime.datetime.now(pytz.timezone('US/Central'))
    time_iso = now.isoformat()
    time_ymdhms = now.strftime('%Y-%m-%dT%H:%M:%S')
    time_ymd = now.strftime('%Y-%m-%d')

    time_utc = datetime.datetime.utcnow()
    time_utc = time_utc.replace(tzinfo=pytz.timezone('US/Central')).isoformat()
    time_zulu = time_utc + 'Z'

    @abstractmethod
    def create_xml(self):
        pass

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
        base_path = 'target/{}/{}/{}'.format(self.claimid, filetype.value, self.env)
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
        # self._save_file(path)

    # _time_iso = datetime.datetime.now(pytz.timezone('US/Central')).isoformat()
    # _time = datetime.datetime.now(pytz.timezone('US/Central')).strftime('%Y-%m-%dT%H:%M:%S')

    # _name = {
    #     'owner_first_name': names.get_first_name(),
    #     'owner_last_name': names.get_last_name()
    # }
    # _file_loc = None
    # _uuid = None
    # _claim_id = None
    # _envelope = None

    # @classmethod
    # def envelope(cls):
    #     return cls._envelope

    # @classmethod
    # def claim_id(cls):
    #     return cls._claim_id

    # @classmethod
    # def name(cls):
    #     return cls._name

    # @staticmethod
    # def get_root(data):
    #     '''Converts the data XML block into an etree root'''
    #     return ET.fromstring(data)

    # @staticmethod
    # def root():
    #     return CreateXML.get_root(CreateXML.envelope)

    # @staticmethod
    # def payload_root():
    #     payload = CreateXML.root.xpath('//*[local-name() = "Data"]')[0].text
    #     return CreateXML.get_root(CreateXML.decode_ungzip(payload))

    # @staticmethod
    # def replace(root=None, tag=None, value=None):
    #     for elem in root.iterfind(tag):
    #         elem.text = value

    # @staticmethod
    # def replace_tag(root=root, tag=None, value=None, **tag_dict):
    #     if not tag_dict:
    #         CreateXML.replace(root=root, tag=tag, value=value)
    #     else:
    #         for tag, value in tag_dict.iteritems():
    #             CreateXML.replace(root=root, tag=tag, value=value)

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
