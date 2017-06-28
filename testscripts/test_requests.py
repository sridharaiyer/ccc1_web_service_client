import requests
import os
import urllib3
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# http = urllib3.PoolManager(
#     cert_reqs='CERT_REQUIRED',
#     ca_certs='certificates/cacerts')
# os.environ['SSL_CERT_DIR'] = os.path.join(os.getcwd(), 'certificates/cacerts')

requests.get('https://interfacesqa.aws.mycccportal.com/gateway/services/ExternalAssignmentWS?wsdl', verify=False)
