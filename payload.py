from xmlutils import XMLUtils
from zipfileutils import ZipFileUtils


class Payload(object):
    """Displays payload content"""

    def __init__(self, fiddler_file, estimate_dict):
        last_est_or_sup = sorted(estimate_dict.keys())[-1]
        last_workfile = estimate_dict[last_est_or_sup]['Workfile']
        z = ZipFileUtils(fiddler_file)
        self.xml = XMLUtils(z.filexml(last_workfile))

    def summary(self):
        payload = self.xml.gettext(tag='Data')
        payload_xml = XMLUtils(XMLUtils.decodebase64_ungzip(payload))
        self._company_code = payload_xml.gettext('CompanyCode')
        company_name = payload_xml.gettext('CompanyName')
        office_name = payload_xml.gettext('OfficeName')
        self._office_id = payload_xml.gettext('ClaimOfficeID')
        self._appr = self.xml.gettext('AppraiserType')

        appraiser_type = {
            'DRP': 'shop appraiser',
            'STA': 'staff appraiser'
        }[self._appr]

        rf = None
        for elem in payload_xml.root.iterfind('.//{*}RepairFacility//{*}Name'):
            rf = elem.text

        costs = []
        for elem in payload_xml.root.iterfind('.//{*}NetRepairCost'):
            costs.append(float(elem.text))

        self._mailboxid = self.xml.gettext('AppraiserMailboxID')

        print('Summary:')
        print('Creating a claim worth ${} of total cost of repair including the estimate and all supplements (if any),'.format(max(costs)))
        print('From an assignment sent from the {} ({}) company\'s {} ({}) claim office.'.format(company_name, self._company_code, office_name, self._office_id))
        print('To the {} {}'.format(rf, appraiser_type))
        print()

    @property
    def company_code(self):
        return self._company_code

    @property
    def office_id(self):
        return self._office_id

    @property
    def appr(self):
        return self._appr

    @property
    def mailboxid(self):
        return self._mailboxid
    
