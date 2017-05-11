from lxml import etree
from lxml.etree import tostring
from lxml.etree import fromstring
import pdb


class XMLUtils(object):

    @staticmethod
    def get_root(xml):
        utf8_parser = etree.XMLParser(encoding='utf-8')
        return fromstring(xml.encode('utf-8'), parser=utf8_parser)

    @staticmethod
    def _edit_tag_multiple_occurences(root, **tag_dict):
        for tag, value in tag_dict.items():
            for elem in root.iterfind(tag):
                elem.text = value
        return XMLUtils._root_to_xml(root)

    @staticmethod
    def _edit_tag_single_occurence(root, **tag_dict):
        for tag, value in tag_dict.items():
            root.xpath('//*[local-name() = \"{}\"]'.format(tag))[0].text = value
        return XMLUtils._root_to_xml(root)

    @staticmethod
    def edit_tag(xml, multiple=False, **tag_dict):
        root = XMLUtils.get_root(xml)
        # print(root)
        # pdb.set_trace()
        if multiple:
            return XMLUtils._edit_tag_multiple_occurences(root, **tag_dict)
        else:
            return XMLUtils._edit_tag_single_occurence(root, **tag_dict)

    @staticmethod
    def edit_xpath_tag(xml, xpath, value):
        root = XMLUtils.get_root(xml)
        root.xpath(xpath)[0].text = value
        return XMLUtils._root_to_xml(root)

    @staticmethod
    def _root_to_xml(root):
        return tostring(root, pretty_print=True, encoding='unicode')

    @staticmethod
    def prettyfy_xml(xml):
        root = XMLUtils.get_root(xml)
        return XMLUtils._root_to_xml(root)


xml = u"""<soapenv:Envelope xmlns:env="http://schemas.xmlsoap.org/soap/envelope/" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"><soapenv:Header/><S:Body xmlns:S="http://schemas.xmlsoap.org/soap/envelope/"><ns1:CreateAssignmentResponse xmlns:ns1="http://services.mycccportal.com/SOA/ExternalAssignmentService"><ns3:CreateAssignmentResponse xmlns:ns3="http://services.mycccportal.com/CCC/assignment/v1" Version="1.0"><TransactionControlHeader xmlns="http://services.mycccportal.com/CCC/TransactionHeader" xmlns:ns2="http://services.mycccportal.com/SOA/normalizedmessage/v1" xmlns:ns3="http://services.mycccportal.com/SOA/commontypes" xmlns:ns4="http://services.mycccportal.com/SOA/fault/v1" xmlns:ns5="http://services.mycccportal.com/SOA/AssignmentValidationService" xmlns:ns6="http://services.mycccportal.com/CCC/assignment/v1" FileType="ASGN" FileVersion="1.0" HeaderVersion="1.0"><UniqueTransactionID>eqa20170511150536</UniqueTransactionID><PrimaryInsuranceCompanyID>APM1</PrimaryInsuranceCompanyID><CCCId code="039002951"/><LossReferenceID>eqa20170511150536</LossReferenceID><EstimatingSystem code="C"/><EchoField>testEchoField</EchoField><CCCActionCode>N</CCCActionCode><TransactionDateTime xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xs="http://www.w3.org/2001/XMLSchema" xsi:type="xs:dateTime">2012-08-28T10:51:49.082-05:00</TransactionDateTime></TransactionControlHeader><ns6:Code xmlns="http://services.mycccportal.com/CCC/TransactionHeader" xmlns:ns2="http://services.mycccportal.com/SOA/normalizedmessage/v1" xmlns:ns3="http://services.mycccportal.com/SOA/commontypes" xmlns:ns4="http://services.mycccportal.com/SOA/fault/v1" xmlns:ns5="http://services.mycccportal.com/SOA/AssignmentValidationService" xmlns:ns6="http://services.mycccportal.com/CCC/assignment/v1">000</ns6:Code><ns6:Description xmlns="http://services.mycccportal.com/CCC/TransactionHeader" xmlns:ns2="http://services.mycccportal.com/SOA/normalizedmessage/v1" xmlns:ns3="http://services.mycccportal.com/SOA/commontypes" xmlns:ns4="http://services.mycccportal.com/SOA/fault/v1" xmlns:ns5="http://services.mycccportal.com/SOA/AssignmentValidationService" xmlns:ns6="http://services.mycccportal.com/CCC/assignment/v1">Assignment Accepted</ns6:Description></ns3:CreateAssignmentResponse></ns1:CreateAssignmentResponse></S:Body></soapenv:Envelope>"""

if __name__ == '__main__':
    print('Original XML:\n')
    print(XMLUtils.prettyfy_xml(xml))

    # pdb.set_trace()
    modified_xml = XMLUtils.edit_tag(xml, UniqueTransactionID='SriSriSri')

    print('Modified XML:\n')
    print(XMLUtils.prettyfy_xml(modified_xml))

    print('Original XML:\n')
    print(XMLUtils.prettyfy_xml(xml))
