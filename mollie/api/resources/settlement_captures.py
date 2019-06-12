from .captures import Captures


class SettlementCaptures(Captures):
    settlementt_id = None

    def get_resource_name(self):
        return 'settlements/{id}/captures'.format(id=self.settlement_id)

    def with_parent_id(self, settlement_id):
        self.settlement_id = settlement_id
        return self

    def on(self, settlement):
        return self.with_parent_id(settlement.id)
