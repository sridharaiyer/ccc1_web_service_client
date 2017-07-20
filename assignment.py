import argparse
import pdb
from xmlutils import XMLUtils
from uniqueid import UniqueID
import names
from xmlbase import XMLBase
from dateutil.relativedelta import relativedelta
import json
from db import DB
from savefile import Save

# SQL to get a random ADJ code from a list of
# valid ADJ codes for a Company - Claim Office combination

sql = """
SELECT FROM_CUST_ALIAS AS ADJCODE FROM
(
SELECT FROM_CUST_ALIAS FROM CUSTOMER_RELATIONSHIP
WHERE FROM_DL_CUST_ID =
(
SELECT DL_CUST_ID FROM CUSTOMER_REGISTERED WHERE CUST_OFCE_ID = '{}' AND CORP_OFCE_DL_CUST_ID =
(SELECT DL_CUST_ID FROM CUSTOMER_REGISTERED WHERE CUST_OFCE_ID = '{}' AND CUST_OFCE_TYP = 'HO')
)
AND ALIAS_TYP_CD = 'ADJ'
AND FROM_CUST_ALIAS NOT LIKE 'xxx%'
ORDER BY DBMS_RANDOM.VALUE
)
WHERE ROWNUM = 1
"""


class ExternalAssignmentWS(XMLBase):

    def __init__(self, **params):
        super().__init__(env=params.pop('env'),
                         claimid=params.pop('claimid'),
                         lname=params.pop('lname'),
                         fname=params.pop('fname'))

        self.params = params
        print('The assignment params: \n{}'.format(json.dumps(params, indent=4)))

    def edit_xml(self):
        super().edit_xml()
        super().edit_descriptor()
        self.xml.edit_tag(multiple=True, **self.params)
        self.xml.edit_tag(Password='Password1')
        self.xml.edit_tag(UniqueTransactionID=self.claimid)
        self.xml.edit_tag(LossReferenceID=self.claimid)
        self.xml.edit_tag(LossReferenceId=self.claimid)  # Note the difference in Id and ID

        for elem in self.xml.root.iterfind('.//{*}ClaimPartyContact//{*}FirstName'):
            elem.text = self.fname

        for elem in self.xml.root.iterfind('.//{*}ClaimPartyContact//{*}LastName'):
            elem.text = self.lname

        claimoffice = self.params['ClaimOffice']
        insID = self.params['PrimaryInsuranceCompanyID']
        newsql = sql.format(claimoffice, insID)
        adjustercode = self.db.claimfolder.execute(newsql)[0][0]
        self.xml.edit_tag(multiple=True, AdjusterCode=adjustercode)

        self.xml.edit_tag(Created=super().time_zulu)
        self.xml.edit_tag(TransactionDateTime=super().time_iso)
        self.xml.edit_tag(DateAssigned=super().time_utc)
        self.xml.edit_tag(ReportedDateTime=super().time_utc)
        self.xml.edit_tag(DriversLicenseExpirationDate=(super().now + relativedelta(years=3)).strftime('%Y-%m-%d'))
        self.xml.edit_tag(AppointmentDate=super().time_utc)
        self.xml.edit_tag(RequestDate=super().time_utc)
        self.xml.edit_tag(LossReportedDateTime=super().time_utc)
        self.xml.edit_tag(PolicyStartDate=(super().now + relativedelta(months=-6)).strftime('%Y-%m-%d'))
        self.xml.edit_tag(PolicyExpirationDate=(super().now + relativedelta(months=6)).strftime('%Y-%m-%d'))

    def verify_db(self):
        print('Assignment creation verified in DB')


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

    assignment = ExternalAssignmentWS(**vars(args))
    assignment.edit_xml()
    assignment.send_xml()
    assignment.verify_db()
