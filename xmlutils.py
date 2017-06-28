from lxml.etree import parse
from lxml.etree import tostring
from lxml.etree import fromstring
from lxml.etree import XMLParser
from lxml.etree import XMLSyntaxError
import pdb
import os.path
import base64
import gzip
from io import BytesIO


class IncorrectXMLError(Exception):
    def __str__(self):
        return ('Incorrect XML file or invalid XML data')


class NoTagError(Exception):
    """docstring for NoTagError"""

    def __init__(self, tag):
        self.tag = tag

    def __str__(self):
        return ('No such tag - {} - in the XML'.format(self.tag))


class XMLUtils(object):
    def __init__(self, xml):
        utf8_parser = XMLParser(encoding='utf-8')
        try:
            self.root = fromstring(xml.encode('utf-8'), parser=utf8_parser)
        except XMLSyntaxError:
            if not os.path.isfile(xml):
                raise IncorrectXMLError
            else:
                self.root = parse(xml)

    def _edit_tag_multiple_occurences(self, **tag_dict):
        try:
            for tag, value in tag_dict.items():
                if tag.startswith('/'):
                    for node in self.root.xpath(tag):
                        node.text = value
                else:
                    for elem in self.root.iterfind(tag):
                        elem.text = value
        except IndexError as e:
            raise NoTagError(tag)

    def _edit_tag_single_occurence(self, **tag_dict):
        try:
            for tag, value in tag_dict.items():
                if tag.startswith('/'):
                    self.root.xpath(tag)[0].text = value
                else:
                    self.root.xpath('//*[local-name() = \"{}\"]'.format(tag))[0].text = value
        except IndexError as e:
            raise NoTagError(tag)

    def edit_tag(self, multiple=False, **tag_dict):
        if multiple:
            self._edit_tag_multiple_occurences(**tag_dict)
        else:
            self._edit_tag_single_occurence(**tag_dict)

    def gettext(self, tag):
        if tag.startswith('/'):
            return self.root.xpath(tag)[0].text
        else:
            return self.root.xpath('//*[local-name() = \"{}\"]'.format(tag))[0].text

    @staticmethod
    def decodebase64(data):
        return base64.b64decode(data)

    @staticmethod
    def encodebase64(data):
        return base64.b64encode(data).decode('UTF-8')

    @staticmethod
    def decodebase64_ungzip(data):
        decoded_base64 = XMLUtils.decodebase64(data)
        gzcontent = gzip.GzipFile(fileobj=BytesIO(
            decoded_base64)).read().decode('UTF-8')
        return gzcontent

    @staticmethod
    def gzip_encodebase64(data):
        gzip_compressed = gzip.compress(data)
        return XMLUtils.encodebase64(gzip_compressed)

    def __bytes__(self):
        """Return a byte object

        Returns:
            bytes: tostring method from etree returns a byte object
        """
        return tostring(self.root, pretty_print=True)

    def __str__(self):
        return bytes(self).decode('utf-8')


if __name__ == '__main__':
    xml = XMLUtils('117_c.xml')

    print(len(xml.root.xpath('//*[local-name()="Reference"][contains(text(),"Events")]/ancestor::*[local-name()="NormalizedMessage"]')))

    for element in xml.root.xpath('//*[local-name()="Reference"][contains(text(),"Events")]/ancestor::*[local-name()="NormalizedMessage"]'):
        element.getparent().remove(element)

    print(len(xml.root.xpath('//*[local-name()="Reference"][contains(text(),"Events")]/ancestor::*[local-name()="NormalizedMessage"]')))
