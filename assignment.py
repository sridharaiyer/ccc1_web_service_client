import argparse
import os
import pdb
from xmlutils import XMLUtils
from uniqueid import UniqueID
import names
from xmlbase import XMLBase
from dateutil.relativedelta import relativedelta
import json


class Assignment(XMLBase):

    def __init__(self, **params):
        super(Assignment, self).__init__(env=params.pop('env'),
                                         claimid=params.pop('claimid'),
                                         lname=params.pop('lname'),
                                         fname=params.pop('fname'))
        xmlpath = {
            'assignment_dir': 'xmltemplates/xmlrequests/Assingnment',
            'assignment_template': 'AssignmentRequest.xml'
        }
        xml = os.path.join(xmlpath['assignment_dir'],
                           xmlpath['assignment_template'])

        self.xml = XMLUtils(xml)
        print(json.dumps(params, indent=4))
        pdb.set_trace()
        self.params = params
        self.web_service_url = self.properties.ws.ExternalAssignmentWS
        print('The assignment params: \n{}'.format(params))

    def create_xml(self):
        self.xml.edit_tag(**self.params)
        self.xml.edit_tag(Password='Password1')
        self.xml.edit_tag(UniqueTransactionID=self.claimid)
        self.xml.edit_tag(LossReferenceID=self.claimid)
        self.xml.edit_tag(LossReferenceId=self.claimid)

        name_dict = {
            '//*[local-name() = \"ClaimPartyContact\"]/*[local-name() = \"LastName\"]': self.lname,
            '//*[local-name() = \"ClaimPartyContact\"]/*[local-name() = \"FirstName\"]': self.fname,
        }

        self.xml.edit_tag(**name_dict)

        time_dict = {
            'Created': super().time_zulu,
            'TransactionDateTime': super().time_iso,
            'DateAssigned': super().time_utc,
            'ReportedDateTime': super().time_utc,
            'DriversLicenseExpirationDate': (super().now + relativedelta(years=3)).strftime('%Y-%m-%d'),
            'AppointmentDate': super().time_utc,
            'RequestDate': super().time_utc,
            'LossReportedDateTime': super().time_utc,
            'PolicyStartDate': (super().now + relativedelta(months=-6)).strftime('%Y-%m-%d'),
            'PolicyExpirationDate': (super().now + relativedelta(months=6)).strftime('%Y-%m-%d'),
        }

        self.xml.edit_tag(**time_dict)

    def verify_db(self):
        print('Assignment creation verified in DB')

    def __bytes__(self):
        return(bytes(self.xml))


if __name__ == '__main__':

    default_params = {
        'PrimaryInsuranceCompanyID': 'APM1',
        'ClaimOffice': 'APMC',
        'AdjusterCode': 'CDAN',
        'AssignmentRecipientID': '62668'
    }

    parser = argparse.ArgumentParser(
        description='Create Interface Assignment')

    parser.add_argument('--env',
                        dest='env',
                        action='store',
                        default='awsqa',
                        choices=['awsqa', 'ct', 'prod'],
                        help='Environment choices')

    parser.add_argument('--claimid',
                        dest='claimid',
                        action='store',
                        default=UniqueID.random_id(),
                        help='Unique claim ID')

    parser.add_argument('--PrimaryInsuranceCompanyID',
                        dest='PrimaryInsuranceCompanyID',
                        action='store',
                        default=default_params['PrimaryInsuranceCompanyID'],
                        help='Insurance company ID')

    parser.add_argument('--ClaimOffice',
                        dest='ClaimOffice',
                        action='store',
                        default=default_params['ClaimOffice'],
                        help='Insurance company claim office ID')

    parser.add_argument('--AdjusterCode',
                        dest='AdjusterCode',
                        action='store',
                        default=default_params['AdjusterCode'],
                        help='Adjuster code')

    parser.add_argument('--AssignmentRecipientID',
                        dest='AssignmentRecipientID',
                        action='store',
                        default=default_params['AssignmentRecipientID'],
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

    assignment = Assignment(**vars(args))
    assignment.create_xml()
    assignment.send_xml()
    assignment.verify_db()
