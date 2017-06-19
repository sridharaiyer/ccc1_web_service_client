from bs4 import BeautifulSoup
import re
import zipfile
from collections import defaultdict
import json
import pdb
import os
from xmlutils import XMLUtils


class FiddlerSession(object):
    """docstring for FiddlerSession"""

    def __init__(self, session_path):
        self.session_path = session_path
        self._files = None

    @property
    def files(self):
        with zipfile.ZipFile(self.session_path, 'r') as zf:
            with zf.open('_index.htm') as indexfile:
                soup = BeautifulSoup(indexfile, "html.parser")
                pattern = re.compile('servicesqa(.*?.)mycccportal.com')
                ccc1_rows = []

                for row in soup.findAll('table')[0].tbody.findAll('tr'):
                    cell = row.findAll('td')[4].text
                    if pattern.match(cell):
                        ccc1_rows.append(row)

                self._files = defaultdict(list)

                for row in ccc1_rows:
                    key = row.findAll('td')[5].text.rsplit('/', 1)[1]
                    value = row.a.get('href').replace("\\", "/")
                    self._files[key].append(value)

                del self._files['GatewayService.asmx']
                del self._files['AdvisorService']
                del self._files['HitTest.aspx']
                del self._files['TokenService.aspx?sv=69']
                del self._files['Login']
                del self._files['ProfileService']
                del self._files['ValuescopeProfileService']
                del self._files['getdocuments?licensenumber=302800']
                del self._files['RPS']
                del self._files['Event']
                del self._files['Worklist']
                self._del_statuschange_dups()

        return self._files

    def _del_statuschange_dups(self):
        status_change_list = self._files['StatusChange']
        for i in range(0, len(status_change_list) - 2):
            for j in range(i, len(status_change_list) - 1):
                if self.get_file(status_change_list[i]) == self.get_file(status_change_list[j]):
                    status_change_list.pop(j)

        for i in range(0, len(status_change_list) - 1):
            xml = XMLUtils(self.get_xml(status_change_list[i]))
            xpath_expression = '//*[local-name()="Reference"][contains(text(),"Workfile")]'
            if len(xml.root.xpath(xpath_expression)) == 0:
                status_change_list.pop(i)

    @property
    def print_files(self):
        print(json.dumps(self.files, indent=4))

    @property
    def estimate_dict(self):
        last_supplement_file = self.files['Workfile'][-1]
        last_supplement_xml = XMLUtils(self.get_xml(last_supplement_file))
        highest_supplement = last_supplement_xml.gettext('DocumentExt')
        print(highest_supplement)

    def get_file(self, path):
        with zipfile.ZipFile(self.session_path, 'r') as zf:
            with zf.open(os.path.join(path), 'r') as wf:
                return str(wf.read())

    def get_xml(self, path):
        s = self.get_file(path)
        return [re.search(r'<s:Envelope.*\/s:Envelope>', s).group()][0]


if __name__ == '__main__':
    f = FiddlerSession('Fiddler_Captures/RF-TESTRFS02APR17-S02.saz')
    f.print_files
    # f.estimate_dict
