from ..error import RequestError
from .base import ResourceCreateMixin, ResourceDeleteMixin
from .methods import Methods


class ProfileMethods(Methods, ResourceCreateMixin, ResourceDeleteMixin):
    RESOURCE_REQUIRED_METHODS = ["giftcard", "voucher"]

    profile_id = None
    method_id = None
    resource_id = None

    def get_resource_path(self):
        path = f"profiles/{self.profile_id}/methods/{self.method_id}"
        if self.method_id in self.RESOURCE_REQUIRED_METHODS:
            path += f"/issuers/{self.resource_id}"
        return path

    def list(self, **params):
        return self.client.methods.list(profileId=self.profile_id)

    def delete(self, resource_id=None, *args, **kwargs):
        if self.method_id in self.RESOURCE_REQUIRED_METHODS and resource_id is None:
            raise RequestError(f"resource_id is required when disabling a {self.method_id}.")
        self.resource_id = resource_id
        path = self.get_resource_path()
        return self.perform_api_call(self.REST_DELETE, path, None)

    def create(self, resource_id=None, data=None, **params):
        if self.method_id in self.RESOURCE_REQUIRED_METHODS and resource_id is None:
            raise RequestError(f"resource_id is required when enabling a {self.method_id}.")
        self.resource_id = resource_id

        return super().create(data, **params)

    def with_parent_id(self, profile_id, method=None):
        self.method_id = method
        self.profile_id = profile_id
        return self

    def on(self, profile, method=None):
        return self.with_parent_id(profile.id, method)
