from .Base import *
from Mollie.API.Object import Mandate


class Mandates(Base):
    customer_id = None

    def getResourceObject(self, result):
        return Mandate(result)

    def getResourceName(self):
        return 'customers/%s/mandates' % self.customer_id

    def on(self, customer):
        self.customer_id = customer['id']
        return self
