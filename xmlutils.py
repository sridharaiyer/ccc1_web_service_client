from lxml.etree import parse
from lxml.etree import tostring
from lxml.etree import fromstring
from lxml.etree import XMLParser
from lxml.etree import XMLSyntaxError
import pdb
import os.path
import pytest


class IncorrectXMLError(Exception):
    def __str__(self):
        return ('Incorrect XML file or invalid XML data')


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
        for tag, value in tag_dict.items():
            if tag.startswith('/'):
                for node in self.root.xpath(tag):
                    node.text = value
            else:
                for elem in self.root.iterfind(tag):
                    elem.text = value

    def _edit_tag_single_occurence(self, **tag_dict):
        for tag, value in tag_dict.items():
            if tag.startswith('/'):
                self.root.xpath(tag)[0].text = value
            else:
                self.root.xpath('//*[local-name() = \"{}\"]'.format(tag))[0].text = value

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

    def __str__(self):
        return tostring(self.root, pretty_print=True, encoding='unicode')