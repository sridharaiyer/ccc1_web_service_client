from lxml import etree
from lxml.etree import tostring
import argparse
import os
import pdb
import requests
from xmlutils import XMLUtils
from uniqueid import UniqueID
import names
from httpclient import HttpClient
from xmlbase import XMLBase
import pytz


class Assignment(XMLBase):

    def __init__(self, xml, **params):
        self.xml = XMLUtils(self.xml)
        self.params = params

    def create_xml(self):
        self.xml.edit_tag(**self.params)
        self.xml.edit_tag(Password='Password1')
        self.xml.edit_tag(UniqueTransactionID=self.params['claimid'])
        self.xml.edit_tag(LossReferenceID=self.params['claimid'])
        self.xml.edit_tag(LossReferenceId=self.params['claimid'])

    def send_xml(self):
        print('Assignment XML posted to web service')

    def verify_db(self):
        print('Assignment creation verified in DB')

    def save_xml(self):
        print('Assignment input and output XML saved')

    @property
    def claimid(self):
        return self.params['claimid']

    @property
    def lastname(self):
        return self.params['lname']

    @property
    def firstname(self):
        return self.params['fname']

    def __str__(self):
        return(str(self.xml))


if not os.path.exists('input'):
    os.makedirs('input')

url = 'https://interfacesqa.aws.mycccportal.com/gateway/services/ExternalAssignmentWS'


assignment_xml = XMLUtils(assignment_xml_path)
assignment_xml


# def send_assignment(claimid=None, output=False, company_id=None, claimoffice_id=None, adjuster_id=None, recepient_id=None, lname=None, fname=None):
def send_assignment(args):

    tag_dict = {
        'Password': 'Password1',
        'UniqueTransactionID'	: ''
    }


# Parameterizing xml data to every request
root.xpath('//*[local-name() = "Password"]')[0].text = 'Password1'
root.xpath('//*[local-name() = "UniqueTransactionID"]')[0].text = claimid
root.xpath('//*[local-name() = "LossReferenceID"]')[0].text = claimid
root.xpath('//*[local-name() = "LossReferenceId"]')[0].text = claimid

xml_data = tostring(root, pretty_print=True)


input_xml_path = os.path.join('input', claim_id + '.xml')

# with open(input_xml_path, 'wb') as p:
#     p.write(xml_data)

# xml_data = BytesIO(xml_data).read()

# headers = {
#     "Content-Type": "text/xml; charset=UTF-8"
# }

# response = requests.post(url=url, headers=headers, data=xml_data, verify=False)

# print(response)
# print(XMLUtils.prettyfy_xml(response.text))

if __name__ == '__main__':

    time_iso = datetime.datetime.now(pytz.timezone('US/Central')).isoformat()
    time = datetime.datetime.now(pytz.timezone('US/Central')).strftime('%Y-%m-%dT%H:%M:%S')

    xmlpath = {
        'assignment_dir'		: 'xmltemplates/xmlrequests/Assingnment',
        'assignment_template'	: 'AssignmentRequest.xml'
    }

    default_params = {
        'SourceTimeStamp'		: time_iso,
        'PublishTimeStamp'		: time_iso,
        'company_id'			: 'APM1',
        'claimoffice_id'		: 'APMC',
        'adjuster_id'			: 'CDAN',
        'recepient_id'			: '62668',
        'recepient_type'		: 'DRP'
    }

    parser = argparse.ArgumentParser(
        description='Create Interface Assignment')

    parser.add_argument('--claimid',
                        dest='claimid',
                        action='store',
                        default=UniqueID.random_id(),
                        help='Unique claim ID')

    parser.add_argument('-o',
                        '--output',
                        dest='output',
                        action='store_true',
                        help='print web service response XML')

    parser.add_argument('--company_id',
                        dest='company_id',
                        action='store',
                        default=default_params['company_id'],
                        help='Insurance company ID')

    parser.add_argument('--claimoffice_id',
                        dest='claimoffice_id',
                        action='store',
                        default=default_params['claimoffice_id'],
                        help='Insurance company claim office ID')

    parser.add_argument('--adjuster_id',
                        dest='adjuster_id',
                        action='store',
                        default=default_params['adjuster_id'],
                        help='Adjuster code')

    parser.add_argument('--recepient_id',
                        dest='recepient_id',
                        action='store',
                        default=default_params['recepient_id'],
                        help='Assignment recepient mail box ID')

    parser.add_argument('--lname',
                        dest='lname',
                        action='store',
                        default=names.get_last_name(),
                        help='Owner last name')

    parser.add_argument('--fname',
                        dest='fname',
                        action='store',
                        default=names.get_first_name(),
                        help='Owner first name')

    args = parser.parse_args()

    assignment_xml_path = os.path.join(xmlpath['assignment_dir'], xmlpath['assignment_template'])

    assignment = Assignment(assignment_xml_path, vars(args))
    assignment.create_xml()
    assignment.send_xml()
    assignment.verify_db()
    assignment.save_xml()
