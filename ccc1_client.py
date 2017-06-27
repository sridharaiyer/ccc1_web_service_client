import argparse
from ws_driver import RunService
from fiddler import FiddlerSession


parser = argparse.ArgumentParser(
    description='Process APM web service calls from saved fiddler request file(s)')

parser.add_argument('-i',
                    '--input',
                    dest='filename',
                    help='.saz fiddler request file to re-execute the SOAP requests')

parser.add_argument('-s',
                    '--show',
                    dest='show',
                    action='store_true',
                    help='Show the different estimate files in the .saz file')

parser.add_argument('--environment',
                    dest='env',
                    action='store_true',
                    required=True,
                    help='Show the different estimate files in the .saz file')


args = parser.parse_args()

files = FiddlerSession(args.filename)

if args.show:
    print(files.estdict)
