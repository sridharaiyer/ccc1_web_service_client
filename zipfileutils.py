import re
import zipfile
import os


class ZipFileUtils(object):
    """docstring for ZipFileUtils"""

    def __init__(self, filepath):
        self.filepath = filepath
        self.filestring = None

    def filestr(self, path):
        """Get the string data from a file inside the zip file

        Args:
            path (String): path to the file in the zip file

        Returns:
            String: String data
        """
        with zipfile.ZipFile(self.filepath, 'r') as zf:
            with zf.open(os.path.join(path), 'r') as wf:
                self.filestring = str(wf.read())

        return self.filestring

    def filestr_decoded(self, path):
        """Get the string data from a file inside the zip file

        Args:
            path (String): path to the file in the zip file

        Returns:
            String: String data
        """
        str_decoded = None
        with zipfile.ZipFile(self.filepath, 'r') as zf:
            with zf.open(os.path.join(path), 'r') as wf:
                str_decoded = str(wf.read(), 'utf-8')

        return str_decoded

    def filexml(self, path):
        """Get the first xml block from a file inside the zip file

        Args:
            path (String): path to the file in the zip file

        Returns:
            String: XML data from file
        """
        s = self.filestr(path)
        return [re.search(r'<s:Envelope.*\/s:Envelope>', s).group()][0]
