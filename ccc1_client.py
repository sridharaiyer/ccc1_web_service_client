import argparse


parser = argparse.ArgumentParser(description='Process APM web service calls from saved fiddler request file(s)')

subparsers = parser.add_subparsers(help='commands')

file_parser = subparsers.add_parser(dest='filenames', metavar='filename', nargs='+', help='List of .saz fiddler request files to re-execute the SOAP requests')

# parser.add_argument('-p', '--pat', metavar='pattern', required=True,
#                     dest='patterns', action='append',
#                     help='text pattern to search for')

file_parser.add_argument('-c', '--check', dest='check', action='store_true',
                         help='check if the .saz files have all the XML files necessary to run the request')

file_parser.add_argument('-v', '--view', dest='view', action='store_true',
                         help='view and print the details of the .saz file')

# parser.add_argument('-o', dest='outfile', action='store',
#                     help='output file')

# parser.add_argument('--speed', dest='speed', action='store',
#                     choices={'slow', 'fast'}, default='slow',
#                     help='search speed')

args = parser.parse_args()

print('{}'.format(args.filenames))
