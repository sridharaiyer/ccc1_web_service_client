import argparse
from fiddler import FiddlerSession
from webserviceengine import WebServiceEngine
from uniqueid import UniqueID
import names
import pdb
import json
from externalassignmentws import ExternalAssignmentWS
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


# ---------------- Get estimate & supplement file paths --------------------
files = FiddlerSession(args.filename)
estimate_dict = files.estdict
old_ref_dict = files.oldrefdict

# ---------------------- Obtain basic info from payload ---------------------
payload = Payload(fiddler_file=args.filename, estimate_dict=estimate_dict)
payload.summary()

# ------------------------------ Placeholder ------------------------------
# This place holder is for cleaning up the estimate dictionary to have the relevant files for the appraiser type. For example, have Worklist only for STAFF and IA and not have it for DRP types such as Repair Facility, Open Shop and Drive-In

logger.info('Location of the estimate and supplement files in the fiddler session: \n{}'.format(json.dumps(estimate_dict, indent=4)))

if args.show:
    exit(1)

logger.info('Args = \n{}'.format(json.dumps(vars(args), indent=4)))

# Removing the 'show' keyword from the dict as this is not required for
# further webservice processing.
vars(args).pop('show')

# ---------------- Setting assignment creation parameters ----------------
assignment_params = {
    'env': args.env,
    'claimid': args.claimid,
    'lname': args.lname,
    'fname': args.fname,
    'PrimaryInsuranceCompanyID': payload.company_code,
    'ClaimOffice': payload.office_id,
    'AssignmentRecipientID': payload.mailboxid
}

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
