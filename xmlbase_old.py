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
import names
from hamcrest import assert_that, equal_to
import uuid
from collections.abc import Mapping


# class ShapeFactory:
#     factories = {}

#     def addFactory(id, shapeFactory):
#         ShapeFactory.factories.put[id] = shapeFactory
#     addFactory = staticmethod(addFactory)
#     # A Template Method:

#     def createShape(id):
#         if not ShapeFactory.factories.has_key(id):
#             ShapeFactory.factories[id] = \
#                 eval(id + '.Factory()')
#         return ShapeFactory.factories[id].create()
#     createShape = staticmethod(createShape)


class TagValue(Mapping):
    def __init__(self, *args, **kw):
        _storage = dict(*args, **kw)

    def __getitem__(self, key):
        return self._storage[key]

    def __iter__(self):
        return iter(self._storage)

    def __len__(self):
        return len(self._storage)


class ModifyXML(abc.ABC):
    """docstring for ModifyXML"""

    def __init__(self, envelope, claim_id):
        self.envelope = envelope
        self.root = ET.fromstring(envelope)
        self.tv = TagValue()
        self.claim_id = claim_id
        super(AbstractOperation, self).__init__()

    def assign_uuids(ref_list):
        uuids = {}
        [uuids.append(str(uuid.uuid4())) for i in ref_list]
        return(dict(zip(ref_list, uuids)))

    @property
    def ref(self):
        ref_list = []
        ref_list.append(u'Workfile')
        ref_list.append(u'Digitalimage')
        ref_list.append(u'Printimage')
        ref_list.append(u'RPD')
        ref_list.append(u'UPD')
        _ref = assign_uuids(ref_list)
        return self._ref

    @property
    def name(self):
        _owner_name = {}
        _owner_name['owner_first_name'] = names.get_first_name()
        _owner_name['owner_last_name'] = names.get_last_name()
        return self._owner_name

    dict_owner_name = {'owner_first_name': names.get_first_name(), 'owner_last_name': names.get_last_name()}

    def decode_ungzip(self, data):
        decoded_base64 = base64.b64decode(data)
        gzcontent = gzip.GzipFile(fileobj=BytesIO(
            decoded_base64)).read().decode('UTF-8')
        return gzcontent

    def gzip_encode(self, xml):
        gzip_compressed = gzip.compress(xml)
        encoded_payload = (base64.b64encode(gzip_compressed)).decode('UTF-8')
        return encoded_payload

    @property
    def uuid(self):
        return str(uuid.uuid4())
    
    def gzip_data():
        pass

    def ungzip_data():
        pass

    def base64_decode():
        pass

    def base64_encode():
        pass

    @abc.abstractmethod
    def prepareXML():
        pass

    @abc.abstractmethod
    def verifyXML():
        pass

    # @classmethod
    # @abc.abstractmethod
    # def factory(cls, *args):
    #     return cls()

    @abc.abstractmethod
    def modifyXML(self):
        # edit all timestamps
        # edit ClaimReferenceID
        # edit Reference last segment UUID
        pass

    @property
    def modifiedXML(self):
        return ET.tostring(root, pretty_print=True)

    def change_single_tag_value(self, root=self.root, **xpath_value):
        for xpath, value in xpath_value.iteritems():
            root.xpath(xpath)[0].text = value

    def change_tag_value_all_occurrences(self, root=self.root, **xpath_value):
        for xpath, value in xpath_value.iteritems():
            for elem in root.iterfind(xpath):
                elem.text = value

    def change_reference(self, root=self.root, ref_tag_xpath, value):
        ref_text = root.xpath(ref_tag_xpath)[0].text
        root.xpath(ref_tag_xpath)[0].text = re.sub('[^/]*$', value, ref_text)
