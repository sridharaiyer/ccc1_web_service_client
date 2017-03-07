from bs4 import BeautifulSoup
import re
import zipfile
import pprint
from collections import defaultdict
import json
import os
from lxml import etree as ET
import base64
import zlib
import tempfile
import gzip
from io import BytesIO, StringIO
import datetime
i = datetime.datetime.now()

claim_Id = 'eqa' + i.strftime('%Y%m%d%H%M%S')
os.makedirs(claim_Id)

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
            envelope = [re.search(r'<s:Envelope.*\/s:Envelope>', s).group()][0]

            root = ET.fromstring(envelope)

            encoded_gzipped_payload = None

            print('Extracting the encoded and gzipped payload')

            encoded_gzipped_payload = root.xpath('//*[local-name() = "Payload"]')[0].xpath('//*[local-name() = "Data"]')[0].text

            print('Decoding and un-gzipping the payload')

            decoded_base64 = base64.b64decode(encoded_gzipped_payload)
            gzcontent = gzip.GzipFile(fileobj=BytesIO(decoded_base64)).read().decode('UTF-8')

            payload_root = ET.fromstring(gzcontent)

            print('Replacing claim IDs in the payload XML')

            payload_root.xpath('//*[local-name() = "ClaimNumber"]')[0].text = claim_Id
            payload_root.xpath('//*[local-name() = "ClaimReferenceID"]')[0].text = claim_Id
            payload_root.xpath('//*[local-name() = "clm_num"]')[0].text = claim_Id

            print('Saving the modified payload XML')

            with open(os.path.join(claim_Id, 'payload.xml'), 'w') as p:
                p.write(ET.tostring(payload_root))

            # envelope = ET.tostring(root)

            # soup = BeautifulSoup(envelope, 'xml')
            # print(soup.find('ClaimReferenceID'))
