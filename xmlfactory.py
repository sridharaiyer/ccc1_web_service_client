from webservices.workfile import Workfile
from webservices.estimateprintimage import EstimatePrintImage
from webservices.digitalimage import DigitalImage
from webservices.unrelatedpriordamage import UnrelatedPriorDamage
from webservices.relatedpriordamagereport import RelatedPriorDamagereport
from webservices.statuschange import StatusChange

XML_TYPE = {
    'Workfile': Workfile,
    'EstimatePrintImage': EstimatePrintImage,
    'DigitalImage': DigitalImage,
    'UnrelatedPriorDamage': UnrelatedPriorDamage,
    'RelatedPriorDamagereport': RelatedPriorDamagereport,
    'StatusChange': StatusChange,
}


class XMLFactory(object):
    @staticmethod
    def factory(cls, **params):
        return XML_TYPE[cls](**params)
