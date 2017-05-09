import http.client
from lxml import etree as ET
from uniqueid import UniqueID

assignment_xml_path = 'xmltemplates/xmlrequests/assignment_apm1_qacerritos.xml'
claim_id = UniqueID.random_id()
HOST = 'http://eznet-qa0.aws.cccis.com'
PORT = '9821'
API_URL = '/soa-infra/services/apm/DeliverAssignment/client'

with open(assignment_xml_path, 'w') as assignment_xml:
    print('File opened successfully')
    body = assignment_xml.read()
    root = ET.fromstring(body)

    # Parameterizing xml data
    root.xpath('//*[local-name() = "Password"]')[0].text = 'Password1'
    root.xpath('//*[local-name() = "UniqueTransactionID"]')[0].text = claim_id

    for elem in root.iterfind('.//{*}LossReferenceId'):
        elem.text = claim_id

    headers = {"Content-type": "application/xml"}
    with http.client.HTTPConnection(HOST, PORT) as conn:
        conn.request("POST", API_URL, body, headers)
        response = conn.getresponse()
        print(response.status)
        print(response.read())
