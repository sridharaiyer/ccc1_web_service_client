import requests
from io import BytesIO
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from xmlutils import XMLUtils

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class HttpClient(object):

    default_header = {
        "Content-Type": "text/xml; charset=UTF-8"
    }

    @classmethod
    def set_default_header(cls, **kwargs):
        for k, v in kwargs.items():
            cls.default_header[k] = v

    @staticmethod
    def post(url, xml, soapaction=None, headers=default_header):
        xml_byte_data = BytesIO(xml).read()
        return requests.post(url=url, headers=headers, data=xml_byte_data, verify=False)


if __name__ == '__main__':
    # client = HttpClient()
    headers = {'Content-Type': 'application/xml'}
    # client.set_default_header(headers)
    url = 'https://interfacesqa.aws.mycccportal.com/gateway/services/ExternalAssignmentWS'
    xml = 'temp_Assignment_input.xml'
    response = requests.post(url=url, headers=headers, data=xml, verify=False)
    print('Response code: {}'.format(response))
    response_xml = XMLUtils(response.text)
    print('Response XML: \n{}'.format(str(response_xml)))
