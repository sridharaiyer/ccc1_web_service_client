from wsbase import WebServiceBase
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


class Workfile(WebServiceBase):
    """docstring for Workfile"""

    def __init__(self, envelope, claim_id):
        super(WebServiceBase, self).__init__(self, envelope, claim_Id)


    def prepareXML(self):
        self.all_occurrence['//{*}ClaimReferenceID'] = self.claim_id
        change_tag_value_all_occurrences(self.all_occurrence)

        encoded_payload_data = root.xpath(
            '//*[local-name() = "Data"]')[0].text
        payload_root = ET.fromstring(decode_ungzip(encoded_payload_data))

        payload_all_occurrence - {}
        payload_all_occurrence['.//{*}ClaimRefID'] = self.claim_id
        payload_all_occurrence['.//{*}ClaimNumber'] = self.claim_id
        payload_all_occurrence['.//{*}clm_num'] = self.claim_id
        payload_all_occurrence['.//{*}Party//{*}FirstName'] = self.names['owner_first_name']
        payload_all_occurrence['.//{*}Party//{*}LastName'] = self.names['owner_last_name']
        payload_all_occurrence['.//{*}owner_info//{*}owner_first_name'] = self.names['owner_last_name']
        payload_all_occurrence['.//{*}owner_info//{*}owner_last_name'] = self.names['owner_last_name']

        change_tag_value_all_occurrences(root=payload_root, payload_all_occurrence)

        gzipped_encoded_payload = gzip_encode(ET.tostring(payload_root))

        self.single_occurrence['//*[local-name() = "Data"]'] = gzipped_encoded_payload

        change_single_tag_value(self.single_occurrence)

        change_reference(ref_tag_xpath=self.ref_tag_xpath, value=self.ref[self.__class__.__name__.upper()])

        with open(os.path.join(self.claim_Id, self.__class__.__name__ + '.xml'), 'wb') as p:
            p.write(ET.tostring(root, pretty_print=True))
