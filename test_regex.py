import re

text = """
POST https://servicesqa.aws.mycccportal.com/gateway/services/Workfile HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: "PutPendingWorkfile"
Host: servicesqa.aws.mycccportal.com
Content-Length: 47811
Expect: 100-continue
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" xmlns:u="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd"><s:Header><o:Security s:mustUnderstand="1"
"""

# m = re.compile('SOAPAction(\w+)', text)
# print(m.groups(0))

# pattern = r'(?:SOAPAction\: ).+\b'
print(re.findall(r'(?:SOAPAction\: ).+\b', text)[0].split('\"')[1].strip())
