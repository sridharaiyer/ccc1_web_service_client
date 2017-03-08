from bs4 import BeautifulSoup
import re
import zipfile
import pprint
from collections import defaultdict
import json
import os
from lxml import etree as ET
from lxml import objectify
import base64
import zlib
import tempfile
import gzip
from io import BytesIO, StringIO
import datetime
import names
from hamcrest import assert_that, equal_to

i = datetime.datetime.now()

owner_first_name = names.get_first_name()
owner_last_name = names.get_last_name()

claim_Id = 'eqa' + i.strftime('%Y%m%d%H%M%S')
os.makedirs(claim_Id)

print('ClaimReferenceID = {}'.format(claim_Id))
print('Owner First Name and Last Name = {} {}'.format(owner_first_name, owner_last_name))

with zipfile.ZipFile('Fiddler_Captures/cwf_testcase29_EO1.saz', 'r') as zf:
    # print(zf.namelist())
    index_file = '_index.htm'
    # try:
    #     data = zf.read(index_file)
    # except KeyError as e:
    #     print('ERROR: Did not find {} in zip file'.format(
    #         index_file))
    # else:
    #     print(index_file, ':')
    #     print(data)
    with zf.open(index_file) as indexfile:
        soup = BeautifulSoup(indexfile, "html.parser")
        table = soup.findChildren('table')[0]

        ccc1_cells = [t.parent for t in table.findAll(
            text='servicesqa.aws.mycccportal.com')]

        ccc1_rows = [r.parent for r in ccc1_cells]

        files = defaultdict(list)

        for row in ccc1_rows:
            key = row.findAll('td')[5].text.rsplit('/', 1)[1]
            value = row.a.get('href').replace("\\", "/")
            if key != 'Worklist':
                files[key].append(value)

        # print('Files and their locations:')
        # print(json.dumps(files, indent=4))

        print('Extracting workfile from indexfile')

        with zf.open(os.path.join(files['Workfile'][0]), 'r') as wf:
            s = str(wf.read())
            # Retrieving the workfile XML block from the text file
            envelope = [re.search(r'<s:Envelope.*\/s:Envelope>', s).group()][0]

            root = ET.fromstring(envelope)

            encoded_gzipped_payload = None

            print('Extracting the encoded and gzipped payload')

            encoded_gzipped_payload = root.xpath('//*[local-name() = "Data"]')[0].text

            print('Decoding and un-gzipping the payload')

            decoded_base64 = base64.b64decode(encoded_gzipped_payload)
            gzcontent = gzip.GzipFile(fileobj=BytesIO(
                decoded_base64)).read().decode('UTF-8')

            payload_root = ET.fromstring(gzcontent)

            print('Replacing claim IDs and party first name last name in the payload XML')

            for elem in payload_root.iterfind('.//{*}ClaimNumber'):
                elem.text = claim_Id  

            for elem in payload_root.iterfind('.//{*}ClaimReferenceID'):
                elem.text = claim_Id 

            for elem in payload_root.iterfind('.//{*}clm_num'):
                elem.text = claim_Id            

            for elem in payload_root.iterfind('.//{*}Party//{*}FirstName'):
                elem.text = owner_first_name

            for elem in payload_root.iterfind('.//{*}Party//{*}LastName'):
                elem.text = owner_last_name

            for elem in payload_root.iterfind('.//{*}owner_info//{*}owner_first_name'):
                elem.text = owner_first_name

            for elem in payload_root.iterfind('.//{*}owner_info//{*}owner_last_name'):
                elem.text = owner_last_name

            modified_payload_xml = ET.tostring(payload_root, pretty_print=True)

            gzip_compressed = gzip.compress(modified_payload_xml)
            encoded_payload = (base64.b64encode(gzip_compressed)).decode('UTF-8')

            for elem in root.iterfind('.//{*}ClaimReferenceID'):
                elem.text = claim_Id            

            for elem in root.iterfind('.//{*}Payload//{*}Data'):
                elem.text = encoded_payload

            print('Saving the PutPendingWorkfile.xml')

            with open(os.path.join(claim_Id, 'PutPendingWorkfile.xml'), 'wb') as p:
                p.write(ET.tostring(root, pretty_print=True))

print('Verifying changes in PutPendingWorkfile.xml')

with open(os.path.join(claim_Id, 'PutPendingWorkfile.xml')) as xmlfile:
    xmldata = xmlfile.read()
    soup = BeautifulSoup(xmldata, 'xml')

    assert_that(soup.find('ClaimReferenceID').text, equal_to(claim_Id))

    encoded_gzipped_payload = soup.find('Data').text

    decoded_base64 = base64.b64decode(encoded_gzipped_payload)
    gzcontent = gzip.GzipFile(fileobj=BytesIO(
        decoded_base64)).read().decode('UTF-8')

    payload_soup = BeautifulSoup(gzcontent, 'xml')

    assert_that(payload_soup.find('Party').find('FirstName').text, equal_to(owner_first_name))
    assert_that(payload_soup.find('Party').find('LastName').text, equal_to(owner_last_name))
    assert_that(payload_soup.find('owner_info').find('owner_first_name').text, equal_to(owner_first_name))
    assert_that(payload_soup.find('owner_info').find('owner_first_name').text, equal_to(owner_first_name))
    assert_that(payload_soup.find('ClaimNumber').text, equal_to(claim_Id))
    assert_that(payload_soup.find('ClaimReferenceID').text, equal_to(claim_Id))
    assert_that(payload_soup.find('clm_num').text, equal_to(claim_Id))
