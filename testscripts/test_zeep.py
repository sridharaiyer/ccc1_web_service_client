import requests
from requests import Session
import zeep
from zeep.transports import Transport
import os
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

session = Session()
session.verify = False
transport = Transport(session=session)
wsdl = 'https://interfacesqa.aws.mycccportal.com/gateway/services/ExternalAssignmentWS?wsdl'
client = zeep.Client(wsdl=wsdl, transport=transport)
