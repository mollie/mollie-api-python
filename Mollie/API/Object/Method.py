from .Base import Base
from .Issuer import Issuer


class Method(Base):
    IDEAL = 'ideal'
    CREDITCARD = 'creditcard'
    MISTERCASH = 'mistercash'
    SOFORT = 'sofort'
    BANKTRANSFER = 'banktransfer'
    DIRECTDEBIT = 'directdebit'
    BITCOIN = 'bitcoin'
    PAYPAL = 'paypal'
    BELFIUS = 'belfius'
    PAYSAFECARD = 'paysafecard'
    PODIUMCADEAUKAART = 'podiumcadeaukaart'
    KBC = 'kbc'
    GIFTCARD = 'giftcard'
    INGHOMEPAY = 'inghomepay'

    @property
    def description(self):
        return self.getProperty('description')

    @property
    def id(self):
        return self.getProperty('id')

    @property
    def image_size1x(self):
        images = self.getProperty('image')
        if 'size1x' not in images:
            return None
        return images['size1x']

    @property
    def image_size2x(self):
        images = self.getProperty('image')
        if 'size2x' not in images:
            return None
        return images['size2x']

    @property
    def issuers(self):
        issuers = self.getProperty('issuers')
        if issuers:
            return [Issuer(x) for x in issuers]

    def getMinimumAmount(self):
        if not self['amount'] or 'minimum' not in self['amount']:
            return None
        return float(self['amount']['minimum'])

    def getMaximumAmount(self):
        if not self['amount'] or 'maximum' not in self['amount']:
            return None
        return float(self['amount']['maximum'])
