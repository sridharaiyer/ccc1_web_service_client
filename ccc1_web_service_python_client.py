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


workfile_ref = str(uuid.uuid4())
digitalimage_ref = str(uuid.uuid4())
printimage_ref = str(uuid.uuid4())
rpd_ref = str(uuid.uuid4())
upd_ref = str(uuid.uuid4())

print('workfile_ref = : {}'.format(workfile_ref))
print('digitalimage_ref = : {}'.format(digitalimage_ref))
print('printimage_ref = : {}'.format(printimage_ref))
print('rpd_ref = : {}'.format(rpd_ref))
print('upd_ref = : {}'.format(upd_ref))


i = datetime.datetime.now()

owner_first_name = names.get_first_name()
owner_last_name = names.get_last_name()

claim_Id = 'eqa' + i.strftime('%Y%m%d%H%M%S')
os.makedirs(claim_Id)

print('ClaimReferenceID = {}'.format(claim_Id))
print('Owner First Name and Last Name = [{}. {}]'.format(owner_first_name, owner_last_name))

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

        files_json = json.dumps(files, indent=4)

        print(files_json)

        print('Assign ref IDs to events:')

        num_of_events = len(files['Event'])

        print('Num of events - {}'.format(num_of_events))

        events_list = []

        [events_list.append(str(uuid.uuid4())) for e in range(num_of_events)]

        events_ref_dict = dict(zip(range(num_of_events), events_list))

        print(events_ref_dict)

        print('Extract events and modify:')

        for event in range(num_of_events):
            print('Modifying and saving event file # : {}'.format(event + 1))
            with zf.open(os.path.join(files['Event'][event]), 'r') as ef:
                s = str(ef.read())
                # Retrieving the workfile XML block from the text file
                envelope = [re.search(r'<s:Envelope.*\/s:Envelope>', s).group()][0]

                root = ET.fromstring(envelope)
                for elem in root.iterfind('.//{*}ClaimReferenceID'):
                    elem.text = claim_Id
                for elem in root.iterfind('.//{*}Reference'):
                    elem.text = re.sub('[^/]*$', events_ref_dict[event], elem.text)

                encoded_payload_data = root.xpath('//*[local-name() = "Data"]')[0].text
                payload_root = ET.fromstring(base64.b64decode(encoded_payload_data).decode('UTF-8'))
                for elem in payload_root.iterfind('.//{*}ClaimRefID'):
                    elem.text = claim_Id

                for elem in payload_root.iterfind('.//{*}ClaimNumber'):
                    elem.text = claim_Id

                for elem in payload_root.iterfind('.//{*}OwnerFirstName'):
                    elem.text = owner_first_name

                for elem in payload_root.iterfind('.//{*}OwnerLastName'):
                    elem.text = owner_last_name

                modified_payload_xml = ET.tostring(payload_root)
                encoded_payload_data = base64.b64encode(modified_payload_xml).decode('UTF-8')

                for elem in root.iterfind('.//{*}Payload//{*}Data'):
                    elem.text = encoded_payload_data

                with open(os.path.join(claim_Id, 'event' + '_' + str(event + 1) + '_' + 'file.xml'), 'wb') as p:
                    p.write(ET.tostring(root, pretty_print=True))

        # print('Extracting workfile from indexfile')

        # with zf.open(os.path.join(files['Workfile'][0]), 'r') as wf:
        #     s = str(wf.read())
        #     # Retrieving the workfile XML block from the text file
        #     envelope = [re.search(r'<s:Envelope.*\/s:Envelope>', s).group()][0]

        #     root = ET.fromstring(envelope)

        #     encoded_gzipped_payload = None

        #     print('Extracting the encoded and gzipped payload')

        #     encoded_gzipped_payload = root.xpath('//*[local-name() = "Data"]')[0].text

        #     print('Decoding and un-gzipping the payload')

        #     decoded_base64 = base64.b64decode(encoded_gzipped_payload)
        #     gzcontent = gzip.GzipFile(fileobj=BytesIO(
        #         decoded_base64)).read().decode('UTF-8')

        #     payload_root = ET.fromstring(gzcontent)

        #     print('Replacing claim IDs and party first name last name in the payload XML')

        #     for elem in payload_root.iterfind('.//{*}ClaimNumber'):
        #         elem.text = claim_Id

        #     for elem in payload_root.iterfind('.//{*}ClaimReferenceID'):
        #         elem.text = claim_Id

        #     for elem in payload_root.iterfind('.//{*}clm_num'):
        #         elem.text = claim_Id

        #     for elem in payload_root.iterfind('.//{*}Party//{*}FirstName'):
        #         elem.text = owner_first_name

        #     for elem in payload_root.iterfind('.//{*}Party//{*}LastName'):
        #         elem.text = owner_last_name

        #     for elem in payload_root.iterfind('.//{*}owner_info//{*}owner_first_name'):
        #         elem.text = owner_first_name

        #     for elem in payload_root.iterfind('.//{*}owner_info//{*}owner_last_name'):
        #         elem.text = owner_last_name

        #     modified_payload_xml = ET.tostring(payload_root, pretty_print=True)

        #     gzip_compressed = gzip.compress(modified_payload_xml)
        #     encoded_payload = (base64.b64encode(gzip_compressed)).decode('UTF-8')

        #     for elem in root.iterfind('.//{*}ClaimReferenceID'):
        #         elem.text = claim_Id

        #     for elem in root.iterfind('.//{*}Payload//{*}Data'):
        #         elem.text = encoded_payload

        #     for elem in root.iterfind('.//{*}Reference'):
        #         elem.text = re.sub('[^/]*$', workfile_ref, elem.text)

        #     print('Saving the PutPendingWorkfile.xml')

        #     with open(os.path.join(claim_Id, 'PutPendingWorkfile.xml'), 'wb') as p:
        #         p.write(ET.tostring(root, pretty_print=True))

        # print('Extracting PrintImage file from the indexfile')

        # with zf.open(os.path.join(files['PrintImage'][0]), 'r') as printimg:
        #     s = str(printimg.read())
        #     # Retrieving the PrintImage XML block from the text file
        #     envelope = [re.search(r'<s:Envelope.*\/s:Envelope>', s).group()][0]
        #     root = ET.fromstring(envelope)

        #     for elem in root.iterfind('.//{*}ClaimReferenceID'):
        #         elem.text = claim_Id

        #     for elem in root.iterfind('.//{*}Reference'):
        #         elem.text = re.sub('[^/]*$', printimage_ref, elem.text)

        #     print('Saving the PrintImage.xml')

        #     with open(os.path.join(claim_Id, 'PrintImage.xml'), 'wb') as p:
        #         p.write(ET.tostring(root, pretty_print=True))

        # print('Extracting RelatedPriorDamage file from the indexfile')

        # with zf.open(os.path.join(files['PrintImage'][1]), 'r') as rpd:
        #     s = str(rpd.read())
        #     # Retrieving the RelatedPriorDamage XML block from the text file
        #     envelope = [re.search(r'<s:Envelope.*\/s:Envelope>', s).group()][0]
        #     root = ET.fromstring(envelope)

        #     for elem in root.iterfind('.//{*}ClaimReferenceID'):
        #         elem.text = claim_Id

        #     for elem in root.iterfind('.//{*}Reference'):
        #         elem.text = re.sub('[^/]*$', rpd_ref, elem.text)

        #     print('Saving the RelatedPriorDamage.xml')

        #     with open(os.path.join(claim_Id, 'RelatedPriorDamage.xml'), 'wb') as p:
        #         p.write(ET.tostring(root, pretty_print=True))

        # print('Extracting UnrelatedPriorDamage file from the indexfile')

        # with zf.open(os.path.join(files['PrintImage'][2]), 'r') as upd:
        #     s = str(upd.read())
        #     # Retrieving the RelatedPriorDamage XML block from the text file
        #     envelope = [re.search(r'<s:Envelope.*\/s:Envelope>', s).group()][0]
        #     root = ET.fromstring(envelope)

        #     for elem in root.iterfind('.//{*}ClaimReferenceID'):
        #         elem.text = claim_Id

        #     for elem in root.iterfind('.//{*}Reference'):
        #         elem.text = re.sub('[^/]*$', upd_ref, elem.text)

        #     print('Saving the UnrelatedPriorDamage.xml')

        #     with open(s.path.join(claim_Id, 'UnrelatedPriorDamage.xml'), 'wb') as p:
        #         p.write(ET.tostring(root, pretty_print=True))

        # print('Extracting DigitalImage file from the indexfile')

        # with zf.open(os.path.join(files['DigitalImage'][0]), 'r') as di:
        #     s = str(di.read())
        #     # Retrieving the RelatedPriorDamage XML block from the text file
        #     envelope = [re.search(r'<s:Envelope.*\/s:Envelope>', s).group()][0]
        #     root = ET.fromstring(envelope)

        #     for elem in root.iterfind('.//{*}ClaimReferenceID'):
        #         elem.text = claim_Id

        #     for elem in root.iterfind('.//{*}Reference'):
        #         elem.text = re.sub('[^/]*$', digitalimage_ref, elem.text)

        #     print('Saving the DigitalImage.xml')

        #     with open(s.path.join(claim_Id, 'DigitalImage.xml'), 'wb') as p:
        #         p.write(ET.tostring(root, pretty_print=True))
# print('Verifying changes in PutPendingWorkfile.xml')

# with open(os.path.join(claim_Id, 'PutPendingWorkfile.xml')) as xmlfile:
#     xmldata = xmlfile.read()
#     soup = BeautifulSoup(xmldata, 'xml')

#     assert_that(soup.find('ClaimReferenceID').text, equal_to(claim_Id))
#     assert_that(soup.find('Reference').text.split('/').pop(), equal_to(workfile_ref))

#     encoded_gzipped_payload = soup.find('Data').text

#     decoded_base64 = base64.b64decode(encoded_gzipped_payload)
#     gzcontent = gzip.GzipFile(fileobj=BytesIO(
#         decoded_base64)).read().decode('UTF-8')

#     payload_soup = BeautifulSoup(gzcontent, 'xml')

#     assert_that(payload_soup.find('Party').find('FirstName').text, equal_to(owner_first_name))
#     assert_that(payload_soup.find('Party').find('LastName').text, equal_to(owner_last_name))
#     assert_that(payload_soup.find('owner_info').find('owner_first_name').text, equal_to(owner_first_name))
#     assert_that(payload_soup.find('owner_info').find('owner_first_name').text, equal_to(owner_first_name))
#     assert_that(payload_soup.find('ClaimNumber').text, equal_to(claim_Id))
#     assert_that(payload_soup.find('ClaimReferenceID').text, equal_to(claim_Id))
#     assert_that(payload_soup.find('clm_num').text, equal_to(claim_Id))
