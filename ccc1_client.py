import argparse
from ws_driver import RunService


parser = argparse.ArgumentParser(
    description='Process APM web service calls from saved fiddler request file(s)')

parser.add_argument(dest='filenames', metavar='filename', nargs='+',
                    help='List of .saz fiddler request files to re-execute the SOAP requests')

parser.add_argument('-c', '--check', dest='check', action='store_true',
                    help='check if the .saz files have all the XML files necessary to run the request')

parser.add_argument('-v', '--view', dest='view', action='store_true',
                    help='view and print the details of the .saz file')

parser.add_argument('-e', '--execute', dest='execute', action='store_true',
                    help='run the web service calls on the .saz file(s)')

# parser.add_argument('-o', dest='outfile', action='store',
#                     help='output file')

# parser.add_argument('--speed', dest='speed', action='store',
#                     choices={'slow', 'fast'}, default='slow',
#                     help='search speed')

args = parser.parse_args()

if True not in [args.check, args.view, args.execute]:
    parser.print_help()
    parser.exit()


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

if args.execute:
    check_integrity(True)
    view_info(True)
    [RunService(filename).execute for filename in args.filenames]
