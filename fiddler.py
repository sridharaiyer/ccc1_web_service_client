from bs4 import BeautifulSoup
import re
import zipfile
from collections import defaultdict
import json
import os
import pdb


class Files(object):
    """docstring for Files"""

    def __init__(self, session_path):
        self.session_path = session_path
        self.files = None

    def get_files_dict(self):
        with zipfile.ZipFile(self.session_path, 'r') as zf:
            with zf.open('_index.htm') as indexfile:
                # instantiate soup to parse the htm file as html
                soup = BeautifulSoup(indexfile, "html.parser")
                # get the first and the only table block which contains the session traffic
                table = soup.findChildren('table')[0]

                ccc1_cells = [t.parent for t in table.findAll(
                    text='servicesqa.aws.mycccportal.com')]

                ccc1_rows = [r.parent for r in ccc1_cells]

                self.files = defaultdict(list)

                for row in ccc1_rows:
                    key = row.findAll('td')[5].text.rsplit('/', 1)[1]
                    value = row.a.get('href').replace("\\", "/")
                    if key != 'Worklist':
                        if key == 'PrintImage':
                            self.files['PrintImage_All'].append(value)
                        else:
                            self.files[key].append(value)

                # Extract and properly name the print image files
                num_of_print_image = len(self.files['PrintImage_All'])

                for img in range(num_of_print_image):
                    img_path = self.files['PrintImage_All'][img]
                    with zf.open(os.path.join(img_path), 'r') as img_file:
                        s = str(img_file.read())
                        envelope = [
                            re.search(r'<s:Envelope.*\/s:Envelope>', s).group()][0]
                        soup = BeautifulSoup(envelope, 'xml')
                        print_image_type = soup.find('MsgType').text
                        if print_image_type == 'Estimate Print Image':
                            print_image_type = 'PrintImage'
                        elif print_image_type == 'Unrelated Prior Damage':
                            print_image_type = 'UnrelatedPriorDamage'
                        elif print_image_type == 'Related Prior Damage report':
                            print_image_type = 'RelatedPriorDamage'

                        self.files[print_image_type] = img_path

                del self.files['PrintImage_All']

                # Cleanup data for keys that require only 1 file
                self.files['Workfile'] = self.files['Workfile'][0]
                self.files['StatusChange'] = self.files['StatusChange'][0]

                return(self.files)

    def print_files_json(self):
        if self.files is None:
            self.get_files_dict()

        print(json.dumps(self.files, indent=4))


if __name__ == '__main__':
    f = Files('Fiddler_Captures/cwf_testcase29_EO1.saz')
    f.get_files()
