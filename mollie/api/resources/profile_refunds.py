from .refunds import Refunds


class ProfileRefunds(Refunds):
    profile_id = None

    def get_resource_name(self):
        return 'refunds?profileId={id}'.format(id=self.profile_id)

    def with_parent_id(self, profile_id):
        self.profile_id = profile_id
        return self

    def on(self, profile):
        return self.with_parent_id(profile.id)
