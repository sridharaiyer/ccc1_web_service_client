from bs4 import BeautifulSoup
import re
import zipfile
from collections import defaultdict
import json
import os
from lxml import etree as ET
import base64
import gzip
from io import BytesIO
import datetime
import names
from hamcrest import assert_that, equal_to
import uuid


tree = ET.parse('status_change_all.xml')

# print('Get all events normalized message nodes.')

# for elem in tree.xpath('//*[local-name()="NormalizedMessage" and not(descendant::*[local-name()="DocumentDescriptor"])]'):
#     print(elem.tag)

# print('\nGet all workfile (E01, S01, S02 .. S099), Printimage and DigitalImage normalized message nodes.')

# for elem in tree.xpath('//*[local-name()="NormalizedMessage" and descendant::*[local-name()="DocumentDescriptor"]]'):
#     print(elem.tag)

print('\nGet the payload/data of wotkfile. (DocumentName = PathwaysXML)')

# for elem in tree.xpath('//text()[contains(.,"PathwaysXML")]/ancestor::*[local-name()="DocumentDescriptor"]/following-sibling::*[local-name()="Payload"]/*[local-name()="Data"]'):
#     print(elem.tag)

print(tree.xpath(
    '//text()[contains(.,"PathwaysXML")]/ancestor::*[local-name()="DocumentDescriptor"]/following-sibling::*[local-name()="Payload"]/*[local-name()="Data"]')[0].text)

print('Get the NormalizedMessage block for PathwaysXML')

print(tree.xpath(
    '//text()[contains(.,"PathwaysXML")]/ancestor::*[local-name()="NormalizedMessage"]')[0].tag)

# //text()[contains(.,'abc')]

# for elem in root.xpath('//*[local-name()!="NormalizedMessage"]'):
#     print(elem.tag)

# for elem in root.findall('.//{*}NormalizedMessage//[not(child::DocumentDescriptor)]'):
# 	print(elem.tag)
