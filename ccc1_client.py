import argparse
from fiddler import FiddlerSession
from webserviceengine import WebServiceEngine
from uniqueid import UniqueID
import names
import pdb
import json


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

parser.add_argument('--environment',
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


args = parser.parse_args()

files = FiddlerSession(args.filename)
estimate_dict = files.estdict

if args.show:
    print(json.dumps(estimate_dict, indent=4))
    exit(1)

# Removing the 'show' keyword from the dict as this is not required for further webservice processing.
vars(args).pop('show')

wsengine = WebServiceEngine(estimate_dict, **vars(args))
wsengine.run()
