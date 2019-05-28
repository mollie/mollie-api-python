from .chargebacks import Chargebacks


class ProfileChargebacks(Chargebacks):
    profile_id = None

    def get_resource_name(self):
        return 'chargebacks?profileId={id}'.format(id=self.profile_id)

    def with_parent_id(self, profile_id):
        self.profile_id = profile_id
        return self

    def on(self, profile):
        return self.with_parent_id(profile.id)
