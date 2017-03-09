import re
import uuid


workfile_ref = str(uuid.uuid4())
print(workfile_ref)
string = 'http://services.mycccportal.com/Workfile/0ee3e306-667b-44a1-9248-e35be8e64c9d/d8a73f67-a8c7-4a49-b491-db4fbf37a725'
print(re.sub('[^/]*$', workfile_ref, string))
