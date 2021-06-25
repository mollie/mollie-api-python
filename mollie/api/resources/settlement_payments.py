from .payments import Payments


class SettlementPayments(Payments):
    settlement_id = None

    def get_resource_name(self):
        return f"settlements/{self.settlement_id}/payments"

    def with_parent_id(self, settlement_id):
        self.settlement_id = settlement_id
        return self

    def on(self, settlement):
        return self.with_parent_id(settlement.id)
