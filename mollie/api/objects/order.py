from ..resources.order_refunds import OrderRefunds
from .base import Base
from .list import List
from .order_line import OrderLine


class Order(Base):

    STATUS_CREATED = 'created'
    STATUS_PAID = 'paid'
    STATUS_AUTHORIZED = 'authorized'
    STATUS_CANCELED = 'canceled'
    STATUS_REFUNDED = 'refunded'
    STATUS_SHIPPING = 'shipping'
    STATUS_COMPLETED = 'completed'
    STATUS_EXPIRED = 'expired'

    def __init__(self, data, resource=None, client=None):
        """
        Override the super __init__ to assign the Client to the result object, which is more flexible since it's
        not tied to a single API resource type
        """
        super(Order, self).__init__(data, resource)
        self.client = client

    @property
    def id(self):
        return self._get_property('id')

    @property
    def profile_id(self):
        return self._get_property('profileId')

    @property
    def method(self):
        return self._get_property('method')

    @property
    def mode(self):
        return self._get_property('mode')

    @property
    def amount(self):
        return self._get_property('amount')

    @property
    def amount_captured(self):
        return self._get_property('amountCaptured')

    @property
    def amount_refunded(self):
        return self._get_property('amountRefunded')

    @property
    def status(self):
        return self._get_property('status')

    @property
    def is_cancelable(self):
        return self._get_property('isCancelable')

    @property
    def billing_address(self):
        return self._get_property('billingAddress')

    @property
    def consumer_date_of_birth(self):
        return self._get_property('consumerDateOfBirth')

    @property
    def order_number(self):
        return self._get_property('orderNumber')

    @property
    def shipping_address(self):
        return self._get_property('shippingAddress')

    @property
    def locale(self):
        return self._get_property('locale')

    @property
    def metadata(self):
        return self._get_property('metadata')

    @property
    def redirect_url(self):
        return self._get_property('redirectUrl')

    @property
    def webhook_url(self):
        return self._get_property('webhookUrl')

    @property
    def created_at(self):
        return self._get_property('createdAt')

    @property
    def expires_at(self):
        return self._get_property('expiresAt')

    @property
    def expired_at(self):
        return self._get_property('expiredAt')

    @property
    def paid_at(self):
        return self._get_property('paidAt')

    @property
    def authorized_at(self):
        return self._get_property('authorizedAt')

    @property
    def canceled_at(self):
        return self._get_property('canceledAt')

    @property
    def completed_at(self):
        return self._get_property('completedAt')

    # documented _links

    @property
    def checkout_url(self):
        return self._get_link('checkout')

    # additional methods

    def is_created(self):
        return self._get_property('status') == self.STATUS_CREATED

    def is_paid(self):
        return self._get_property('status') == self.STATUS_PAID

    def is_authorized(self):
        return self._get_property('status') == self.STATUS_AUTHORIZED

    def is_canceled(self):
        return self._get_property('status') == self.STATUS_CANCELED

    def is_refunded(self):
        return self._get_property('status') == self.STATUS_REFUNDED

    def is_shipping(self):
        return self._get_property('status') == self.STATUS_SHIPPING

    def is_completed(self):
        return self._get_property('status') == self.STATUS_COMPLETED

    def is_expired(self):
        return self._get_property('status') == self.STATUS_EXPIRED

    def create_refund(self, data, **params):
        refund = OrderRefunds(self.client).on(self).create(data, **params)
        return refund

    @property
    def refunds(self):
        refunds = OrderRefunds(self.client).on(self).list()
        return refunds

    @property
    def order_lines(self):
        lines = self._get_property('lines') or []
        result = {
            '_embedded': {
                'lines': lines,
            },
            'count': len(lines),
        }
        return List(result, OrderLine, client=self.client)

    # TODO: Addresses
