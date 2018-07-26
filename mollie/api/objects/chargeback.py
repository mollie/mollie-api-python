from .base import Base


class Chargeback(Base):
    @property
    def id(self):
        return self._get_property('id')

    @property
    def amount(self):
        return self._get_property('amount')

    @property
    def settlement_amount(self):
        return self._get_property('settlementAmount')

    @property
    def created_at(self):
        return self._get_property('createdAt')

    @property
    def reversed_at(self):
        return self._get_property('reversedAt')

    @property
    def payment_id(self):
        return self._get_property('paymentId')
