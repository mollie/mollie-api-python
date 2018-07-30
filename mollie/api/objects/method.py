from .base import Base
from .issuer import Issuer
from .list import List


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
    BANCONTACT = 'bancontact'
    EPS = 'eps'
    GIROPAY = 'giropay'

    @property
    def description(self):
        return self._get_property('description')

    @property
    def id(self):
        return self._get_property('id')

    @property
    def image_size1x(self):
        try:
            images = self._get_property('image')
            return images['size1x']
        except KeyError:
            return None

    @property
    def image_size2x(self):
        try:
            images = self._get_property('image')
            return images['size2x']
        except KeyError:
            return None

    @property
    def issuers(self):
        """Return the issuer list"""
        try:
            issuers = self._get_property('issuers')
            result = {
                '_embedded': {
                    'issuers': issuers,
                }}
            return List(result, Issuer)
        except KeyError:
            return None

    def getMinimumAmount(self):
        # TODO check for obsoletion
        try:
            return float(self['amount']['minimum'])
        except KeyError:
            return None

    def getMaximumAmount(self):
        # TODO check for obsoletion
        try:
            return float(self['amount']['maximum'])
        except KeyError:
            return None
