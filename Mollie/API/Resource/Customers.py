from .Base import *
from Mollie.API.Object import Customer


class Customers(Base):
    def getResourceObject(self, result):
        return Customer(result)

    def mandates(self, customer):
        return self.client.customer_mandates.on(customer)

    def subscriptions(self, customer):
        return self.client.customer_subscriptions.on(customer)
