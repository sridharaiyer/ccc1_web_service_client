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
        self
        payload = self.xml.gettext(tag='Data')
        payload_xml = XMLUtils(XMLUtils.decodebase64_ungzip(payload))
        company_code = payload_xml.gettext('CompanyCode')
        company_name = payload_xml.gettext('CompanyName')
        office_name = payload_xml.gettext('OfficeName')
        office_id = payload_xml.gettext('ClaimOfficeID')

        rf = None
        for elem in payload_xml.root.iterfind('.//{*}RepairFacility//{*}Name'):
            rf = elem.text

        costs = []
        for elem in payload_xml.root.iterfind('.//{*}NetRepairCost'):
            costs.append(float(elem.text))

        print('Summary:')
        print('Creating a claim worth ${} of total cost of repair including the estimate and all supplements (if any),'.format(max(costs)))
        print('From an assignment sent from the {} ({}) company\'s {} ({}) claim office to the {} shop'.format(company_name, company_code, office_name, office_id, rf))
        print()
