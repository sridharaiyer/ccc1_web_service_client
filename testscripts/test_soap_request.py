import requests
import lxml.etree as etree
from lxml.etree import fromstring
from lxml.etree import tostring


def get_root(xml=None):
    utf8_parser = etree.XMLParser(encoding='utf-8')
    return fromstring(xml.encode('utf-8'), parser=utf8_parser)


def prettyfy_xml(xml=None):
    return(tostring(get_root(xml), pretty_print=True, encoding='unicode'))


request = u"""<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetQuote xmlns="http://www.webserviceX.NET/">
      <symbol>MSFT</symbol>
    </GetQuote>
  </soap:Body>
</soap:Envelope>"""

print('\nRequest Quote for Microsoft: \n', prettyfy_xml(request))
encoded_request = request.encode('utf-8')

headers = {
    "Host": "www.webservicex.net",
    "Content-Type": "text/xml; charset=UTF-8",
    "SOAPAction": "http://www.webserviceX.NET/GetQuote"
}

response = requests.post(url="http://www.webservicex.net/stockquote.asmx", headers=headers, data=encoded_request, verify=False)


quote = get_root(response.text).xpath('//*[local-name() = "GetQuoteResult"]')[0].text

print('\nResponse Quote:\n')
print(tostring(fromstring(quote), pretty_print=True, encoding='unicode'))
