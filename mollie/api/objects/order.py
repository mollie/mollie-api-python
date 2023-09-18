from .base import ObjectBase


class Order(ObjectBase):
    def __init__(self, data, client):
        super().__init__(data, client)

    STATUS_CREATED = "created"
    STATUS_PAID = "paid"
    STATUS_AUTHORIZED = "authorized"
    STATUS_CANCELED = "canceled"
    STATUS_SHIPPING = "shipping"
    STATUS_COMPLETED = "completed"
    STATUS_EXPIRED = "expired"

    @property
    def id(self):
        return self._get_property("id")

    @property
    def resource(self):
        return self._get_property("resource")

    @property
    def profile_id(self):
        return self._get_property("profileId")

    @property
    def method(self):
        return self._get_property("method")

    @property
    def mode(self):
        return self._get_property("mode")

    @property
    def amount(self):
        return self._get_property("amount")

    @property
    def amount_captured(self):
        return self._get_property("amountCaptured")

    @property
    def amount_refunded(self):
        return self._get_property("amountRefunded")

    @property
    def status(self):
        return self._get_property("status")

    @property
    def is_cancelable(self):
        return self._get_property("isCancelable")

    @property
    def billing_address(self):
        return self._get_property("billingAddress")

    @property
    def consumer_date_of_birth(self):
        return self._get_property("consumerDateOfBirth")

    @property
    def order_number(self):
        return self._get_property("orderNumber")

    @property
    def shipping_address(self):
        return self._get_property("shippingAddress")

    @property
    def locale(self):
        return self._get_property("locale")

    @property
    def metadata(self):
        return self._get_property("metadata")

    @property
    def redirect_url(self):
        return self._get_property("redirectUrl")

    @property
    def webhook_url(self):
        return self._get_property("webhookUrl")

    @property
    def created_at(self):
        return self._get_property("createdAt")

    @property
    def expires_at(self):
        return self._get_property("expiresAt")

    @property
    def expired_at(self):
        return self._get_property("expiredAt")

    @property
    def paid_at(self):
        return self._get_property("paidAt")

    @property
    def authorized_at(self):
        return self._get_property("authorizedAt")

    @property
    def canceled_at(self):
        return self._get_property("canceledAt")

    @property
    def completed_at(self):
        return self._get_property("completedAt")

    @property
    def cancel_url(self):
        return self._get_property("cancelUrl")

    # documented _links

    @property
    def checkout_url(self):
        return self._get_link("checkout")

    # additional methods

    def is_created(self):
        return self.status == self.STATUS_CREATED

    def is_paid(self):
        return self.status == self.STATUS_PAID

    def is_authorized(self):
        return self.status == self.STATUS_AUTHORIZED

    def is_canceled(self):
        return self.status == self.STATUS_CANCELED

    def is_shipping(self):
        return self.status == self.STATUS_SHIPPING

    def is_completed(self):
        return self.status == self.STATUS_COMPLETED

    def is_expired(self):
        return self.status == self.STATUS_EXPIRED

    def has_refunds(self):
        return self.amount_refunded is not None

    @property
    def refunds(self):
        from ..resources import OrderRefunds

        return OrderRefunds(self.client, self)

    @property
    def lines(self):
        from ..resources import OrderLines

        return OrderLines(self.client, self)

    @property
    def shipments(self):
        from ..resources import OrderShipments

        return OrderShipments(self.client, self)

    @property
    def payments(self):
        from ..resources import OrderPayments

        return OrderPayments(self.client, self)
