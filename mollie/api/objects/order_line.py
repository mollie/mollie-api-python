from .base import ObjectBase


class OrderLine(ObjectBase):
    @classmethod
    def get_resource_class(cls, client):
        from ..resources import OrderLines

        return OrderLines(client)

    STATUS_CREATED = "created"
    STATUS_AUTHORIZED = "authorized"
    STATUS_PAID = "paid"
    STATUS_SHIPPING = "shipping"
    STATUS_CANCELED = "canceled"
    STATUS_COMPLETED = "completed"

    @classmethod
    def get_object_name(cls):
        return "lines"

    @property
    def id(self):
        return self._get_property("id")

    @property
    def resource(self):
        return self._get_property("resource")

    @property
    def order_id(self):
        return self._get_property("orderId")

    @property
    def type(self):
        return self._get_property("type")

    @property
    def name(self):
        return self._get_property("name")

    @property
    def status(self):
        return self._get_property("status")

    @property
    def is_cancelable(self):
        return self._get_property("isCancelable")

    @property
    def quantity(self):
        return self._get_property("quantity")

    @property
    def quantity_shipped(self):
        return self._get_property("quantityShipped")

    @property
    def amount_shipped(self):
        return self._get_property("amountShipped")

    @property
    def quantity_refunded(self):
        return self._get_property("quantityRefunded")

    @property
    def amount_refunded(self):
        return self._get_property("amountRefunded")

    @property
    def quantity_canceled(self):
        return self._get_property("quantityCanceled")

    @property
    def amount_canceled(self):
        return self._get_property("amountCanceled")

    @property
    def shippable_quantity(self):
        return self._get_property("shippableQuantity")

    @property
    def refundable_quantity(self):
        return self._get_property("refundableQuantity")

    @property
    def cancelable_quantity(self):
        return self._get_property("cancelableQuantity")

    @property
    def unit_price(self):
        return self._get_property("unitPrice")

    @property
    def discount_amount(self):
        return self._get_property("discountAmount")

    @property
    def total_amount(self):
        return self._get_property("totalAmount")

    @property
    def vat_rate(self):
        return self._get_property("vatRate")

    @property
    def vat_amount(self):
        return self._get_property("vatAmount")

    @property
    def sku(self):
        return self._get_property("sku")

    @property
    def image_url(self):
        return self._get_link("imageUrl")

    @property
    def product_url(self):
        return self._get_link("productUrl")

    @property
    def created_at(self):
        return self._get_property("createdAt")

    @property
    def metadata(self):
        return self._get_property("metadata")

    # additional methods

    def is_created(self):
        return self._get_property("status") == self.STATUS_CREATED

    def is_authorized(self):
        return self._get_property("status") == self.STATUS_AUTHORIZED

    def is_paid(self):
        return self._get_property("status") == self.STATUS_PAID

    def is_shipping(self):
        return self._get_property("status") == self.STATUS_SHIPPING

    def is_canceled(self):
        return self._get_property("status") == self.STATUS_CANCELED

    def is_completed(self):
        return self._get_property("status") == self.STATUS_COMPLETED
