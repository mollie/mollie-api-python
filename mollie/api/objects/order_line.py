from .base import Base


class OrderLine(Base):

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
