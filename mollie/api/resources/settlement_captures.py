from .captures import Captures


class SettlementCaptures(Captures):
    settlement_id = None

    def get_resource_name(self):
        return f"settlements/{self.settlement_id}/captures"

    def with_parent_id(self, settlement_id):
        self.settlement_id = settlement_id
        return self

    def on(self, settlement):
        return self.with_parent_id(settlement.id)
