from bs4 import BeautifulSoup
import re
from collections import defaultdict
import json
import pdb
from xmlutils import XMLUtils
from zipfileutils import ZipFileUtils


class FiddlerSession(object):
    """docstring for FiddlerSession"""

    def __init__(self, session_path):
        self.session_path = session_path
        self._files = None
        self._zipfile = ZipFileUtils(session_path)
        self._estdict = {'E01': {}}

    @property
    def files(self):
        indexfile = self._zipfile.filestr('_index.htm')
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
            value = row.a.get('href').replace("\\\\", "/")
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

        return json.dumps(self._files, indent=4)

    def _del_statuschange_dups(self):
        '''Removes duplicate files and the xml which does not contain a worfile
        '''
        status_change_list = self._files['StatusChange']
        for i in range(0, len(status_change_list) - 2):
            for j in range(i, len(status_change_list) - 1):
                if self._zipfile.filestr(status_change_list[i]) == self._zipfile.filestr(status_change_list[j]):
                    status_change_list.pop(j)

        for i in range(0, len(status_change_list) - 1):
            xml = XMLUtils(self._zipfile.filexml(status_change_list[i]))
            expression = '//*[local-name()="Reference"][contains(text(),"Workfile")]'
            if len(xml.root.xpath(expression)) == 0:
                status_change_list.pop(i)

    def _basedict(self):
        """Creates a base place holder dict for E01, S01 etc
        """
        if self._files is None:
            self.files
        highest_estimate = len(self._files['Workfile'])
        if highest_estimate > 1:
            for i in range(highest_estimate - 1):
                e = ''
                if i < 9:
                    e = 'S0' + str(i + 1)
                else:
                    e = 'S' + str(i + 1)
                self._estdict[e] = {}

    @property
    def estdict(self):
        """Identifying the different files belonging to different estimates such as E01, S01 etc

        Returns:
            dict: The estimate dict.
        """
        self._basedict()
        for file_type, files in self._files.items():
            if file_type == 'Workfile':
                for path in files:
                    xml = XMLUtils(self._zipfile.filexml(path))
                    est_type = xml.gettext('DocumentExt')
                    self._estdict[est_type][file_type] = path
            elif file_type == 'PrintImage':
                for path in files:
                    xml = XMLUtils(self._zipfile.filexml(path))
                    est_type = xml.gettext('DocumentExt')
                    ftype = xml.gettext('MsgType').replace(" ", "")
                    self._estdict[est_type][ftype] = path
            elif file_type == 'DigitalImage':
                for path in files:
                    xml = XMLUtils(self._zipfile.filexml(path))
                    est_id = re.search('EstID&gt;(.*)&lt;/EstID', str(xml)).group(1)
                    if int(est_id) == 51:
                        est_type = 'E01'
                    else:
                        est_type = 'S' + str(est_id)[-2:]
                    ftype = xml.gettext('MsgType').replace(" ", "")
                    self._estdict[est_type][file_type] = path
            elif file_type == 'StatusChange':
                for path in files:
                    xml = XMLUtils(self._zipfile.filexml(path))
                    est_type = xml.gettext('DocumentExt')
                    self._estdict[est_type][file_type] = path

        return self._estdict


if __name__ == '__main__':
    f = FiddlerSession('Fiddler_Captures/RF-TESTRFS02APR17-S02.saz')
    print(f.files)
    print(f.estdict)
