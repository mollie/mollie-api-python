from .base import Base


class OrderLine(Base):

    STATUS_CREATED = 'created'
    STATUS_AUTHORIZED = 'authorized'
    STATUS_PAID = 'paid'
    STATUS_SHIPPING = 'shipping'
    STATUS_CANCELED = 'canceled'
    STATUS_REFUNDED = 'refunded'
    STATUS_COMPLETED = 'completed'

    def __init__(self, data, resource=None, client=None):
        """
        Override the super __init__ to assign the Client to the result object, which is more flexible since it's
        not tied to a single API resource type
        """
        super(OrderLine, self).__init__(data, None)
        self.client = client

    @classmethod
    def get_object_name(cls):
        return 'lines'

    @property
    def id(self):
        return self._get_property('id')

    @property
    def resource(self):
        return self._get_property('resource')

    @property
    def order_id(self):
        return self._get_property('orderId')

    @property
    def type(self):
        return self._get_property('type')

    @property
    def name(self):
        return self._get_property('name')

    @property
    def status(self):
        return self._get_property('status')

    @property
    def is_cancelable(self):
        return self._get_property('isCancelable')

    @property
    def quantity(self):
        return self._get_property('quantity')

    @property
    def quantity_shipped(self):
        return self._get_property('quantityShipped')

    @property
    def amount_shipped(self):
        return self._get_property('amountShipped')

    @property
    def quantity_refunded(self):
        return self._get_property('quantityRefunded')

    @property
    def amount_refunded(self):
        return self._get_property('amountRefunded')

    @property
    def quantity_canceled(self):
        return self._get_property('quantityCanceled')

    @property
    def amount_canceled(self):
        return self._get_property('amountCanceled')

    @property
    def unit_price(self):
        return self._get_property('unitPrice')

    @property
    def discount_amount(self):
        return self._get_property('discountAmount')

    @property
    def total_amount(self):
        return self._get_property('totalAmount')

    @property
    def vat_rate(self):
        return self._get_property('vatRate')

    @property
    def vat_amount(self):
        return self._get_property('vatAmount')

    @property
    def sku(self):
        return self._get_property('sku')

    @property
    def image_url(self):
        return self._get_property('imageUrl')

    @property
    def product_url(self):
        return self._get_property('productUrl')

    @property
    def created_at(self):
        return self._get_property('createdAt')

    def cancel(self):
        """Cancel order line.

        Deleting an order line causes the order line status to change to canceled.
        """
        # Import OrderLines locally to avoid circular import
        from ..resources.order_lines import OrderLines

        return OrderLines(self.client).with_parent_id(self.order_id).delete(self.id)

    # additional methods

    def is_created(self):
        return self._get_property('status') == self.STATUS_CREATED

    def is_authorized(self):
        return self._get_property('status') == self.STATUS_AUTHORIZED

    def is_paid(self):
        return self._get_property('status') == self.STATUS_PAID

    def is_shipping(self):
        return self._get_property('status') == self.STATUS_SHIPPING

    def is_canceled(self):
        return self._get_property('status') == self.STATUS_CANCELED

    def is_refunded(self):
        return self._get_property('status') == self.STATUS_REFUNDED

    def is_completed(self):
        return self._get_property('status') == self.STATUS_COMPLETED
