from lxml import etree
from lxml.etree import tostring
import datetime
import os
import pdb
import requests
from io import BytesIO
from xmlutils import XMLUtils
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

if not os.path.exists('input'):
    os.makedirs('input')

assignment_xml_path = 'xmltemplates/xmlrequests/Assingnment/assignment_apm1_qacerritos.xml'

claim_id = 'eqa' + datetime.datetime.now().strftime('%Y%m%d%H%M%S')

url = 'https://interfacesqa.aws.mycccportal.com/gateway/services/ExternalAssignmentWS'

print(claim_id)

root = etree.parse(assignment_xml_path)

# Parameterizing xml data to every request
root.xpath('//*[local-name() = "Password"]')[0].text = 'Password1'
root.xpath('//*[local-name() = "UniqueTransactionID"]')[0].text = claim_id
root.xpath('//*[local-name() = "LossReferenceID"]')[0].text = claim_id
root.xpath('//*[local-name() = "LossReferenceId"]')[0].text = claim_id

xml_data = tostring(root, pretty_print=True)


input_xml_path = os.path.join('input', claim_id + '.xml')

with open(input_xml_path, 'wb') as p:
    p.write(xml_data)

xml_data = BytesIO(xml_data).read()

headers = {
    "Content-Type": "text/xml; charset=UTF-8"
}

response = requests.post(url=url, headers=headers, data=xml_data, verify=False)

print(response)
print(XMLUtils.prettyfy_xml(response.text))
