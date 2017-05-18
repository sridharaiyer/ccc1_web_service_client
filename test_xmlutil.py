import pytest
from xmlutils import XMLUtils
from lxml.etree import parse
from lxml.etree import tostring
from lxml.etree import fromstring
from lxml.etree import XMLParser

xml = u"""<soapenv:Envelope xmlns:env="http://schemas.xmlsoap.org/soap/envelope/" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"><soapenv:Header/><S:Body xmlns:S="http://schemas.xmlsoap.org/soap/envelope/"><ns1:CreateAssignmentResponse xmlns:ns1="http://services.mycccportal.com/SOA/ExternalAssignmentService"><ns3:CreateAssignmentResponse xmlns:ns3="http://services.mycccportal.com/CCC/assignment/v1" Version="1.0"><TransactionControlHeader xmlns="http://services.mycccportal.com/CCC/TransactionHeader" xmlns:ns2="http://services.mycccportal.com/SOA/normalizedmessage/v1" xmlns:ns3="http://services.mycccportal.com/SOA/commontypes" xmlns:ns4="http://services.mycccportal.com/SOA/fault/v1" xmlns:ns5="http://services.mycccportal.com/SOA/AssignmentValidationService" xmlns:ns6="http://services.mycccportal.com/CCC/assignment/v1" FileType="ASGN" FileVersion="1.0" HeaderVersion="1.0"><UniqueTransactionID>eqa20170511150536</UniqueTransactionID><PrimaryInsuranceCompanyID>APM1</PrimaryInsuranceCompanyID><CCCId code="039002951"/><LossReferenceID>eqa20170511150536</LossReferenceID><EstimatingSystem code="C"/><EchoField>testEchoField</EchoField><CCCActionCode>N</CCCActionCode><TransactionDateTime xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xs="http://www.w3.org/2001/XMLSchema" xsi:type="xs:dateTime">2012-08-28T10:51:49.082-05:00</TransactionDateTime></TransactionControlHeader><ns6:Code xmlns="http://services.mycccportal.com/CCC/TransactionHeader" xmlns:ns2="http://services.mycccportal.com/SOA/normalizedmessage/v1" xmlns:ns3="http://services.mycccportal.com/SOA/commontypes" xmlns:ns4="http://services.mycccportal.com/SOA/fault/v1" xmlns:ns5="http://services.mycccportal.com/SOA/AssignmentValidationService" xmlns:ns6="http://services.mycccportal.com/CCC/assignment/v1">000</ns6:Code><ns6:Description xmlns="http://services.mycccportal.com/CCC/TransactionHeader" xmlns:ns2="http://services.mycccportal.com/SOA/normalizedmessage/v1" xmlns:ns3="http://services.mycccportal.com/SOA/commontypes" xmlns:ns4="http://services.mycccportal.com/SOA/fault/v1" xmlns:ns5="http://services.mycccportal.com/SOA/AssignmentValidationService" xmlns:ns6="http://services.mycccportal.com/CCC/assignment/v1">Assignment Accepted</ns6:Description></ns3:CreateAssignmentResponse></ns1:CreateAssignmentResponse></S:Body></soapenv:Envelope>"""


tag_dict = {
    'UniqueTransactionID'					: 'SriSriSri',
    'PrimaryInsuranceCompanyID'				: 'GEICO',
    '//*[local-name() = \"CCCActionCode\"]'	: 'HEAVEN'
}


def test_xmlutil_edittag():
    file = 'sample_assignment_response.xml'
    root = parse(file)
    xmlfile1 = XMLUtils(file)
    xmlfile1.edit_tag(**tag_dict)
    assert xmlfile1.gettext('UniqueTransactionID') == 'SriSriSri'
    assert xmlfile1.gettext('PrimaryInsuranceCompanyID') == 'GEICO'
    assert root.xpath('//*[local-name() = \"CCCActionCode\"]')[0].text != xmlfile1.gettext('CCCActionCode')


def test_xmlutil_edittag_data():
    utf8_parser = XMLParser(encoding='utf-8')
    root = fromstring(xml.encode('utf-8'), parser=utf8_parser)
    xmlfile2 = XMLUtils(xml)
    xmlfile2.edit_tag(**tag_dict)
    assert xmlfile2.gettext('UniqueTransactionID') == 'SriSriSri'
    assert xmlfile2.gettext('PrimaryInsuranceCompanyID') == 'GEICO'
    assert root.xpath('//*[local-name() = \"CCCActionCode\"]')[0].text != xmlfile2.gettext('CCCActionCode')
