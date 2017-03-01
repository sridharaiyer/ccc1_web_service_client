from bs4 import BeautifulSoup
import re

# with open('Fiddler_Captures/E01/_index.htm') as fp:
#     soup = BeautifulSoup(fp)

# for row in soup.find_all('tr'):
#     print(row)

import zipfile

with zipfile.ZipFile('Fiddler_Captures/S02.saz', 'r') as zf:
    # print(zf.namelist())
    index_file = '_index.htm'
    # try:
    #     data = zf.read(index_file)
    # except KeyError as e:
    #     print('ERROR: Did not find {} in zip file'.format(
    #         index_file))
    # else:
    #     print(index_file, ':')
    #     print(data)
    with zf.open(index_file) as indexfile:
        soup = BeautifulSoup(indexfile, "html.parser")
        table = soup.findChildren('table')[0]

        ccc1_cells = [t.parent for t in table.findAll(text='servicesqa.aws.mycccportal.com')]

        ccc1_rows = [r.parent for r in ccc1_cells]

        ws_files_dict = {}

        for row in ccc1_rows:
            print('{!s:20s}:  {}'.format(row.findAll('td')[5].text.rsplit('/', 1)[1], row.a.get('href')))
