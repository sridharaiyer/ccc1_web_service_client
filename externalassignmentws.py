import argparse
import pdb
from xmlutils import XMLUtils
from uniqueid import UniqueID
import names
from dateutil.relativedelta import relativedelta
import json
from db import DB
from savefile import Save
from timeutils import Time
from httpclient import HttpClient
from properties import Properties
import logging
from log_util import Logger

logger = logging.getLogger()

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

mailbox_sql = """
SELECT FROM_CUST_ALIAS FROM CUSTOMER_RELATIONSHIP WHERE FROM_DL_CUST_ID IN
(
SELECT DL_CUST_ID FROM CUSTOMER
WHERE CUST_OFCE_ID = '{}'
AND CUST_OFCE_TYP = 'HO'
)
AND
TO_DL_CUST_ID =
(SELECT DL_CUST_ID FROM CUSTOMER WHERE DL_CUST_ID IN
(
SELECT TO_DL_CUST_ID FROM CUSTOMER_RELATIONSHIP WHERE FROM_CUST_ALIAS='{}'
)
)
"""


class ExternalAssignmentWS(object):

    def __init__(self, **params):
        self.env = params.pop('env')
        self.claimid = params.pop('claimid')
        self.lname = params.pop('lname')
        self.fname = params.pop('fname')
        self.params = params
        self.path = 'xmltemplates/sample_create_assignment.xml'
        self.xml = XMLUtils(self.path)
        self.time = Time()
        self.db = DB(self.env)
        self.savefile = Save(claimid=self.claimid,
                             est=None,
                             filetype='Assignment',
                             env=self.env)
        self.properties = Properties(self.env)

    def __bytes__(self):
        return bytes(self.xml)

    def edit_xml(self):
        logger.info('Preparing the {} {} XML file'.format(
            self.env, 'Assignment'))

        # Getting Adjustercode from database from office and company

        claimoffice = self.params['ClaimOffice']
        insID = self.params['PrimaryInsuranceCompanyID']
        newsql = sql.format(claimoffice, insID)
        adjustercode = self.db.claimfolder.execute(newsql)[0][0]
        self.params['AdjusterCode'] = adjustercode

        recp_id = self.params['AssignmentRecipientID']
        new_mailbox_sql = mailbox_sql.format(insID, recp_id)
        self.params['AssignmentRecipientID'] = self.db.claimfolder.execute(new_mailbox_sql)[0][0]

        logger.info('The assignment params: \n{}'.format(
            json.dumps(self.params, indent=4)))

        self.xml.edit_tag(multiple=True, **self.params)
        self.xml.edit_tag(Password='Password1')
        self.xml.edit_tag(UniqueTransactionID=self.claimid)
        self.xml.edit_tag(LossReferenceID=self.claimid)
        # Note the difference in Id and ID
        self.xml.edit_tag(LossReferenceId=self.claimid)

        for elem in self.xml.root.iterfind('.//{*}ClaimPartyContact//{*}FirstName'):
            elem.text = self.fname

        for elem in self.xml.root.iterfind('.//{*}ClaimPartyContact//{*}LastName'):
            elem.text = self.lname

        self.xml.edit_tag(multiple=True, AdjusterCode=adjustercode)

        self.xml.edit_tag(Created=self.time.zulu)
        self.xml.edit_tag(TransactionDateTime=self.time.iso)
        self.xml.edit_tag(DateAssigned=self.time.utc)
        self.xml.edit_tag(ReportedDateTime=self.time.utc)
        self.xml.edit_tag(multiple=True,
                          DriversLicenseExpirationDate=(
                              self.time.now + relativedelta(years=3)).strftime('%Y-%m-%d'))
        self.xml.edit_tag(AppointmentDate=self.time.utc)
        self.xml.edit_tag(RequestDate=self.time.utc)
        self.xml.edit_tag(LossReportedDateTime=self.time.utc)
        self.xml.edit_tag(PolicyStartDate=(
            self.time.now + relativedelta(months=-6)).strftime('%Y-%m-%d'))
        self.xml.edit_tag(PolicyExpirationDate=(
            self.time.now + relativedelta(months=6)).strftime('%Y-%m-%d'))

        self.savefile.save_input(bytes(self))

    def send_xml(self):
        url = self.properties.ws[self.__class__.__name__]
        self.response = HttpClient().post(url, bytes(self))
        response_xml = XMLUtils(self.response.text)
        self.savefile.save_response(str(response_xml))

        if self.response.status_code != 200:
            error_msg = response_xml.gettext('LogMessage')
            logger.error('Error response: \{}'.format(error_msg))
            exit(1)

    def verify_db(self):
        sql = """SELECT * FROM SERVICE_ORDER WHERE
                CUST_CLM_REF_ID = '{}' AND
                ASGN_MAINT_TYP_CD = 'A'""".format(self.claimid)
        logger.info('Start assignment creation DB verification:\n{}'.format(sql))
        self.db.claimfolder.wait_until_exists(sql)
        logger.info('The assignment was successfully created.')
        pdb.set_trace()


if __name__ == '__main__':

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
                        required=True,
                        help='Insurance company ID')

    parser.add_argument('--ClaimOffice',
                        dest='ClaimOffice',
                        action='store',
                        required=True,
                        help='Insurance company claim office ID')

    parser.add_argument('--AssignmentRecipientID',
                        dest='AssignmentRecipientID',
                        action='store',
                        required=True,
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

    parser.add_argument('--log',
                        dest='loglevel',
                        action='store',
                        type=str,
                        choices=['INFO', 'DEBUG'],
                        default='INFO',
                        help='print logs')

    args = parser.parse_args()

    # -------------  Initialize LOGGING -------------------
    numeric_level = getattr(logging, args.loglevel.upper(), None)
    logger = Logger(numeric_level)

    assignment = ExternalAssignmentWS(**vars(args))
    assignment.edit_xml()
    assignment.send_xml()
    assignment.verify_db()
