import re
import json
from zipfileutils import ZipFileUtils
import pdb


class Header(object):
    def __init__(self, filetext):
        self._filetext = str(filetext)
        self._header_dict = {}
        self._header_dict['Content-Type'] = re.findall(r'[\n\r].*Content-Type:\s*([^\n\r]*)', filetext)[0].strip()
        self._header_dict['SOAPAction'] = re.findall(r'[\n\r].*SOAPAction:\s*([^\n\r]*)', filetext)[0].strip().replace('"', '')
        self._header_dict['Host'] = re.findall(r'[\n\r].*Host:\s*([^\n\r]*)', filetext)[0].strip()

    @property
    def get_url(self):
        return re.findall(r'POST\s*([^\n\r]*)', self._filetext)[0].split()[0].strip()

    @property
    def header_dict(self):
        return self._header_dict


if __name__ == '__main__':
    zipfilename = 'Fiddler_Captures/RF-TESTRFS02APR17-S02.saz'
    z = ZipFileUtils(zipfilename)
    filetext = z.filestr_decoded('raw/091_c.txt')

    h = Header(filetext)
    print(h.get_url)
    print(json.dumps(h.header_dict, indent=4))
