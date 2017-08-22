import argparse
from fiddler import FiddlerSession
from webserviceengine import WebServiceEngine
from uniqueid import UniqueID
import names
import pdb
import json
from xmlutils import XMLUtils
from externalassignmentws import ExternalAssignmentWS
from zipfileutils import ZipFileUtils
from payload import Payload
import logging
from log_util import Logger


parser = argparse.ArgumentParser(
    description='Process APM web service calls from saved fiddler request file(s)')

parser.add_argument('-i',
                    '--input',
                    dest='filename',
                    required=True,
                    help='.saz fiddler request file to re-execute the SOAP requests')

parser.add_argument('-s',
                    '--show',
                    dest='show',
                    action='store_true',
                    help='Show the different estimate files in the .saz file')

parser.add_argument('--env',
                    dest='env',
                    action='store',
                    type=str,
                    choices=['awsqa', 'awsint', 'ct', 'prod'],
                    default='awsqa',
                    help='Provide the environment to run the webservice in.')

parser.add_argument('--claimid',
                    dest='claimid',
                    action='store',
                    default=UniqueID.random_id(),
                    help='User provided claimid')

parser.add_argument('-a',
                    '--appraiser',
                    dest='appr',
                    action='store',
                    required=True,
                    choices=['rf', 'staff', 'ia', 'openshop'],
                    help='Provide the type of appraiser')

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

# ------------------------ Initialize LOGGING ------------------------------
numeric_level = getattr(logging, args.loglevel.upper(), None)
logger = Logger(numeric_level)
# ------------------------ Initialize LOGGING ------------------------------


# ---------------- Get estimate & supplement file paths --------------------
files = FiddlerSession(args.filename)
estimate_dict = files.estdict
old_ref_dict = files.oldrefdict
# ---------------- Get estimate & supplement file paths --------------------


Payload(fiddler_file=args.filename, estimate_dict=estimate_dict).summary()

# Get the location of the E01 Workfile
e01_file = estimate_dict['E01']['Workfile']

logger.debug(json.dumps(estimate_dict, indent=4))

logger.info('Location of the estimate and supplement files in the fiddler session: \n{}'.format(json.dumps(estimate_dict, indent=4)))

if args.show:
    exit(1)

logger.info('Args = \n{}'.format(json.dumps(vars(args), indent=4)))

# Removing the 'show' keyword from the dict as this is not required for
# further webservice processing.
vars(args).pop('show')

# ------------------ Get E01 XML to fetch assignment info ---------------------
e01_xml = XMLUtils(ZipFileUtils(args.filename).filexml(e01_file))
ins_company_code = e01_xml.gettext('VantiveCode')
claim_office_code = e01_xml.gettext('Code')
recepient_code = e01_xml.gettext('AppraiserMailboxID')

assignment_params = {
    'env': args.env,
    'claimid': args.claimid,
    'lname': args.lname,
    'fname': args.fname,
    'PrimaryInsuranceCompanyID': e01_xml.gettext('VantiveCode'),
    'ClaimOffice': e01_xml.gettext('Code'),
    'AssignmentRecipientID': e01_xml.gettext('AppraiserMailboxID')
}
# ------------------ Get E01 XML to fetch assignment info ---------------------

# ----------------------------- Process assignment ----------------------------
assignment = ExternalAssignmentWS(**assignment_params)
assignment.edit_xml()
assignment.send_xml()
assignment.verify_db()
# ----------------------------- Process assignment ----------------------------

# ------------- Process estimate and supplement web services ------------------
wsengine = WebServiceEngine(estimate_dict, old_ref_dict, **vars(args))
wsengine.run()
# ------------- Process estimate and supplement web services ------------------
