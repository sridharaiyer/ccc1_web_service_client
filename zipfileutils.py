from bs4 import BeautifulSoup
import re
import zipfile
import os


class ZipFileUtils(object):
    """docstring for ZipFileUtils"""

    def __init__(self, filepath):
        self.filepath = filepath

    def filestr(self, path):
        """Get the string data from a file inside the zip file

        Args:
            path (String): path to the file in the zip file

        Returns:
            String: String data
        """
        with zipfile.ZipFile(self.filepath, 'r') as zf:
            with zf.open(os.path.join(path), 'r') as wf:
                return str(wf.read())

    def filexml(self, path):
        """Get the first xml block from a file inside the zip file

        Args:
            path (String): path to the file in the zip file

        Returns:
            String: XML data from file
        """
        s = self.filestr(path)
        return [re.search(r'<s:Envelope.*\/s:Envelope>', s).group()][0]
