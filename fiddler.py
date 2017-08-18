from bs4 import BeautifulSoup
import re
from collections import defaultdict
import json
import pdb
from xmlutils import XMLUtils
from zipfileutils import ZipFileUtils
import copy
import logging

logger = logging.getLogger()


class FiddlerSession(object):
    """docstring for FiddlerSession"""

    def __init__(self, session_path):
        self.session_path = session_path
        self._files = None
        self._zipfile = ZipFileUtils(session_path)
        self._estdict = {'E01': {}}
        self._oldrefdict = {'E01': {}}

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

        logger.debug('Raw Files before removing ignore list: \n{}'.format(json.dumps(self._files, indent=4)))

        ignore_list = [
            'GatewayService.asmx',
            'AdvisorService',
            'HitTest.aspx',
            'TokenService.aspx?sv=69',
            'Login',
            'ProfileService',
            'ValuescopeProfileService',
            'getdocuments?licensenumber=302800',
            'RPS',
            'Event',
            'Worklist',
        ]
        for s in ignore_list:
            if s in self._files:
                del self._files[s]

        self._del_statuschange_dups()

        logger.debug('Raw Files after removing ignore list: \n{}'.format(json.dumps(self._files, indent=4)))

        return self._files

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

        self._oldrefdict = copy.deepcopy(self._estdict)

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
                    self._oldrefdict[est_type][file_type] = xml.gettext('Reference').split("/")[-1]
            elif file_type == 'PrintImage':
                for path in files:
                    xml = XMLUtils(self._zipfile.filexml(path))
                    est_type = xml.gettext('DocumentExt')
                    ftype = xml.gettext('MsgType').replace(" ", "")
                    self._estdict[est_type][ftype] = path
                    self._oldrefdict[est_type][ftype] = xml.gettext('Reference').split("/")[-1]
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
                    self._oldrefdict[est_type][file_type] = xml.gettext('Reference').split("/")[-1]
            elif file_type == 'StatusChange':
                for path in files:
                    xml = XMLUtils(self._zipfile.filexml(path))
                    est_type = xml.gettext('DocumentExt')
                    self._estdict[est_type][file_type] = path

        return self._estdict

    @property
    def oldrefdict(self):
        return self._oldrefdict


if __name__ == '__main__':
    f = FiddlerSession('Fiddler_Captures/S0208182017.saz')
    print(json.dumps(f.files, indent=4))
    print(json.dumps(f.estdict, indent=4))
