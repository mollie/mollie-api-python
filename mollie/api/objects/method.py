from .base import Base
from .issuer import Issuer
from .list import List


class Method(Base):
    @classmethod
    def get_resource_class(cls, client):
        from ..resources.methods import Methods
        return Methods(client)

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
    KLARNAPAYLATER = 'klarnapaylater'
    KLARNASLICEIT = 'klarnasliceit'

    @property
    def description(self):
        return self._get_property('description')

    @property
    def id(self):
        return self._get_property('id')

    @property
    def image_svg(self):
        try:
            images = self._get_property('image')
            return images['svg']
        except KeyError:
            return None

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
        """Return the list of available issuers for this payment method."""
        issuers = self._get_property('issuers') or []
        result = {
            '_embedded': {
                'issuers': issuers,
            },
            'count': len(issuers),
        }
        return List(result, Issuer)
