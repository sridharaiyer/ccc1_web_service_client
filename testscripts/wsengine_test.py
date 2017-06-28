import pytest
from webserviceengine import WebServiceEngine


# Shared data
test_params = {
    'claimid': 'testclaim',
    'env': 'qa',
    'appr': 'staff',
    'lname': 'Smith',
    'fname': 'Peter'
}

test_est_dict = {
    "E01": {
        "Workfile": "raw/091_c.txt",
        "EstimatePrintImage": "raw/092_c.txt",
        "UnrelatedPriorDamage": "raw/094_c.txt",
        "RelatedPriorDamagereport": "raw/095_c.txt",
        "DigitalImage": "raw/093_c.txt",
        "StatusChange": "raw/117_c.txt"
    },
    "S01": {
        "Workfile": "raw/158_c.txt",
        "EstimatePrintImage": "raw/159_c.txt",
        "UnrelatedPriorDamage": "raw/161_c.txt",
        "RelatedPriorDamagereport": "raw/162_c.txt",
        "DigitalImage": "raw/160_c.txt",
        "StatusChange": "raw/172_c.txt"
    },
    "S02": {
        "Workfile": "raw/211_c.txt",
        "EstimatePrintImage": "raw/212_c.txt",
        "UnrelatedPriorDamage": "raw/214_c.txt",
        "RelatedPriorDamagereport": "raw/215_c.txt",
        "DigitalImage": "raw/213_c.txt",
        "StatusChange": "raw/225_c.txt"
    }
}
if __name__ == '__main__':
    wsengine = WebServiceEngine(**test_params)
    wsengine.estimate_dict = test_est_dict
    for obj in wsengine.generate:
        print(str(obj))
        obj.create_xml()
        obj.send_xml()
        obj.verify_db()
