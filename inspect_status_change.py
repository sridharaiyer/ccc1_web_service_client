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

for elem in tree.xpath('//*[local-name()="NormalizedMessage" and not(descendant::*[local-name()="DocumentDescriptor"])]'):
    print(elem.tag)

# for elem in root.xpath('//*[local-name()!="NormalizedMessage"]'):
#     print(elem.tag)

# for elem in root.findall('.//{*}NormalizedMessage//[not(child::DocumentDescriptor)]'):
# 	print(elem.tag)
