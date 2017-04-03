import re
import uuid
import pprint
import json
from box import Box


# workfile_ref = str(uuid.uuid4())
# print(workfile_ref)
# string = 'http://services.mycccportal.com/Workfile/0ee3e306-667b-44a1-9248-e35be8e64c9d/d8a73f67-a8c7-4a49-b491-db4fbf37a725'
# print(re.sub('[^/]*$', workfile_ref, string))


# references = ['workfile_ref', 'digitalimage_ref', 'printimage_ref', 'rpd_ref', 'upd_ref']
# uuids = []
# [uuids.append(str(uuid.uuid4())) for i in references]
# dict_ref = dict(zip(references, uuids))
# print(json.dumps(dict_ref, indent=4))

# Reading data back

data = None
with open('properties.json', 'r') as f:
    data = json.load(f)

config_data = Box(data)

print(eval('{}.{}.{}.{}.{}'.format(config_data, 'awsqa', 'db', 'claimfolder', 'host')))
