from .methods import Methods


class ProfileMethods(Methods):
    profile_id = None
    method_id = None

    def get_resource_name(self):
        return 'profiles/{id}/methods/{method}'.format(id=self.profile_id, method=self.method_id)

    def list(self, **params):
        return self.client.methods.list(profileId=self.profile_id)

    def delete(self, *args, **kwargs):
        path = self.get_resource_name()
        return self.perform_api_call(self.REST_DELETE, path, None)

    def with_parent_id(self, profile_id, method=None):
        self.method_id = method
        self.profile_id = profile_id
        return self

    def on(self, profile, method=None):
        return self.with_parent_id(profile.id, method)
