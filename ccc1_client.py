import argparse
from ws_driver import RunService
from fiddler import FiddlerSession


parser = argparse.ArgumentParser(
    description='Process APM web service calls from saved fiddler request file(s)')

# parser.add_argument(dest='filenames', metavar='filename', nargs='+',
#                     help='List of .saz fiddler request files to re-execute the SOAP requests')
parser.add_argument('-i', '--input', dest='filename',
                    help='.saz fiddler request file to re-execute the SOAP requests')

parser.add_argument('-c', '--check', dest='check', action='store_true',
                    help='check if the .saz files have all the XML files necessary to run the request')

parser.add_argument('-v', '--view', dest='view', action='store_true',
                    help='view and print the details of the .saz file')


# parser.add_argument('-o', dest='outfile', action='store',
#                     help='output file')

# parser.add_argument('--speed', dest='speed', action='store',
#                     choices={'slow', 'fast'}, default='slow',
#                     help='search speed')

args = parser.parse_args()


def check_integrity(flag):
    if flag:
        for filename in args.filenames:
            print('Checking file {} for integrity...'.format(filename))


def view_info(flag):
    if flag:
        for filename in args.filenames:
            print('Getting the details file {}...'.format(filename))


if args.check:
    check_integrity(True)

if args.view:
    view_info(True)

files = FiddlerSession(args.filename)
xml_files_dict = files.get_files_dict()
print(xml_files_dict)
