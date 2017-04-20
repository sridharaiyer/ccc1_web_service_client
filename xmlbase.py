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
    """docstring for CreateXML"""

    def __init__(self, envelope, claim_id):
        self._envelope = envelope
        self._claim_id = claim_id
        self._name = {'owner_first_name': names.get_first_name(), 'owner_last_name': names.get_last_name()}
        self._time_iso = datetime.datetime.now(pytz.timezone('US/Central')).isoformat()
        self._time = datetime.datetime.now(pytz.timezone('US/Central')).strftime('%Y-%m-%dT%H:%M:%S')
        super(AbstractOperation, self).__init__()

    @property
    def claim_id(self):
        return self._claim_id

    @property
    def name(self):
        return self._name

    @property
    def root(self):
        return get_root(self.envelope)

    @property
    def get_root(self, data):
        return ET.fromstring(data)

    @property
    def payload_root(self):
        payload = self.root.xpath('//*[local-name() = "Data"]')[0].text
        return self.get_root(self.decode_ungzip(payload))

    @abc.abstractmethod
    def modifyXML(self, root=self.root):
        tag_dict = {}
        tag_dict['.//{*}SourceTimeStamp'] = self._time_iso
        tag_dict['.//{*}PublishTimeStamp'] = self._time_iso
        tag_dict['.//{*}ClaimNumber'] = claim_id
        tag_dict['.//{*}ClaimReferenceID'] = claim_id
        tag_dict['.//{*}clm_num'] = claim_id
        tag_dict['.//{*}Party//{*}FirstName'] = name['owner_first_name']
        tag_dict['.//{*}Party//{*}LastName'] = name['owner_last_name']
        tag_dict['.//{*}owner_info//{*}owner_first_name'] = name['owner_first_name']
        tag_dict['.//{*}owner_info//{*}owner_last_name'] = name['owner_last_name']

        replace_tag(root=root, tag_dict)

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
    def root_to_string(self, root=self.root):
        return ET.tostring(root, pretty_print=True)

    @abc.abstractmethod
    def change_reference(self, root=self.root, ref):
        for elem in root.iterfind('.//{*}Reference'):
            elem.text = re.sub('[^/]*$', ref, elem.text)

    def base64_decode():
        pass

    def base64_encode():
        pass

    # @classmethod
    # @abc.abstractmethod
    # def factory(cls, *args):
    #     return cls()

    def replace(self, root=None, tag=None, value=None):
        for elem in root.iterfind(tag):
            elem.text = value

    def replace_tag(self, root=self.root, tag=None, value=None, **tag_dict):
        if not tag_dict:
            replace(root=root, tag=tag, value=value)
        else:
            for tag, value in tag_dict.iteritems():
                replace(root=root, tag=tag, value=value)

    def change_reference(self, root=self.root, ref_tag_xpath, value):
        ref_text = root.xpath(ref_tag_xpath)[0].text
        root.xpath(ref_tag_xpath)[0].text = re.sub('[^/]*$', value, ref_text)

    def save_xml(self):
        pass
