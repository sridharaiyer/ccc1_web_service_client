import requests
from io import BytesIO
from requests.packages.urllib3.exceptions import InsecureRequestWarning

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
