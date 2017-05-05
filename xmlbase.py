import abc
from bs4 import BeautifulSoup
import re
import zipfile
from collections import defaultdict
import json
import os
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


class CreateXML(abc.ABC):

    _time_iso = datetime.datetime.now(pytz.timezone('US/Central')).isoformat()
    _time = datetime.datetime.now(pytz.timezone('US/Central')).strftime('%Y-%m-%dT%H:%M:%S')

    _name = {
        'owner_first_name': names.get_first_name(),
        'owner_last_name': names.get_last_name()
    }
    _file_loc = None
    _uuid = None
    _claim_id = None
    _envelope = None

    @property
    @classmethod
    def envelope(cls):
        return cls._envelope

    @property
    @classmethod
    def claim_id(cls):
        return cls._claim_id

    @property
    @classmethod
    def name(cls):
        return cls._name

    @property
    @staticmethod
    def get_root(data):
        return ET.fromstring(data)

    @property
    def root(self):
        return CreateXML.get_root(CreateXML.envelope)

    @property
    def payload_root(self):
        payload = self.root.xpath('//*[local-name() = "Data"]')[0].text
        return self.get_root(self.decode_ungzip(payload))

    def replace(self, root=None, tag=None, value=None):
        for elem in root.iterfind(tag):
            elem.text = value

    def replace_tag(self, root=root, tag=None, value=None, **tag_dict):
        if not tag_dict:
            self.replace(root=root, tag=tag, value=value)
        else:
            for tag, value in tag_dict.iteritems():
                self.replace(root=root, tag=tag, value=value)

    @abc.abstractmethod
    def modifyXML(self, root=root):
        tag_dict = {}
        tag_dict['.//{*}SourceTimeStamp'] = self._time_iso
        tag_dict['.//{*}PublishTimeStamp'] = self._time_iso
        tag_dict['.//{*}ClaimNumber'] = CreateXML.claim_id
        tag_dict['.//{*}ClaimReferenceID'] = self.claim_id
        tag_dict['.//{*}clm_num'] = self.claim_id
        tag_dict['.//{*}Party//{*}FirstName'] = self.name['owner_first_name']
        tag_dict['.//{*}Party//{*}LastName'] = self.name['owner_last_name']
        tag_dict['.//{*}owner_info//{*}owner_first_name'] = self.name['owner_first_name']
        tag_dict['.//{*}owner_info//{*}owner_last_name'] = self.name['owner_last_name']

        self.replace_tag(root=root, **tag_dict)

    def decode_ungzip(self, data):
        decoded_base64 = base64.b64decode(data)
        gzcontent = gzip.GzipFile(fileobj=BytesIO(
            decoded_base64)).read().decode('UTF-8')
        return gzcontent

    def gzip_encode(self, data):
        gzip_compressed = gzip.compress(data)
        encoded_payload = (base64.b64encode(gzip_compressed)).decode('UTF-8')
        return encoded_payload

    @property
    def root_to_string(self, root=root):
        return ET.tostring(root, pretty_print=True)

    @abc.abstractmethod
    def change_reference(self, root=root, ref=None):
        for elem in root.iterfind('.//{*}Reference'):
            elem.text = re.sub('[^/]*$', ref, elem.text)

    def base64_decode():
        pass

    def base64_encode():
        pass

    @classmethod
    def save_xml(cls):
        pass
