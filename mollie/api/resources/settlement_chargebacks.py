from .chargebacks import Chargebacks


class SettlementChargebacks(Chargebacks):
    settlement_id = None

    def get_resource_path(self):
        return f"settlements/{self.settlement_id}/chargebacks"

    def with_parent_id(self, settlement_id):
        self.settlement_id = settlement_id
        return self

    def on(self, settlement):
        return self.with_parent_id(settlement.id)
