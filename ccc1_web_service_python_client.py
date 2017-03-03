from bs4 import BeautifulSoup
import re
import zipfile
import pprint
from collections import defaultdict
import json
import xmltodict
import os
from lxml import etree as ET
import base64
import tempfile
import gzip
# from xml.etree import ElementTree as ET

# from xml.dom.minidom import parse
# import xml.dom.minidom

putPendingWorkfileXML = ''

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

        ccc1_cells = [t.parent for t in table.findAll(text='servicesqa.aws.mycccportal.com')]

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
            envelope = [re.search(r'<s:Envelope.*\/s:Envelope>', s).group()][0]

            root = ET.fromstring(envelope)

            encoded_gzipped_payload = None

            for elem in root.getiterator():
                if elem.tag == '{http://services.mycccportal.com/SOA/normalizedmessage/v1}Data':
                    encoded_gzipped_payload = elem.text

            decoded_base64 = base64.b64decode(encoded_gzipped_payload)
            # with tempfile.TemporaryFile(mode='w+b') as temp:
            #     temp.write(bytes(decoded_base64))
            #     print(temp.read())
            #     with gzip.open(temp, 'rb') as f:
            #         file_content = f.read()
            #         print(file_content)

            with open('decoded_base64.txt.gz', 'wb') as f:
                f.write(decoded_base64)

            with gzip.open('decoded_base64.txt.gz', 'rb') as f:
                file_content = f.read()
                print(file_content)

            # envelope = ET.tostring(root)

            # soup = BeautifulSoup(envelope, 'xml')
            # print(soup.find('ClaimReferenceID'))
