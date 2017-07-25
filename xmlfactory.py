from webservices.apm.workfile import Workfile
from webservices.apm.estimateprintimage import EstimatePrintImage
from webservices.apm.digitalimage import DigitalImage
from webservices.apm.unrelatedpriordamage import UnrelatedPriorDamage
from webservices.apm.relatedpriordamagereport import RelatedPriorDamagereport
from webservices.apm.statuschange import StatusChange

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
