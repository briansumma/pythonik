from typing import (
    Any,
    Dict,
    Union,
)

from pythonik.models.base import Response
from pythonik.models.settings import (
    CORSHostSchema,
    CORSHostsSchema,
    GroupSettingPublicSchema,
    KubernetesSettingSchema,
    MergedSettingsSchema,
    SystemSettingPublicSchema,
    UserSettingRemoveAttributesSchema,
    UserSettingSchema,
)
from pythonik.specs._internal_utils import is_pydantic_model
from pythonik.specs.base import Spec


class SettingsSpec(Spec):
    server = "API/settings/"

    def fetch_cors_hosts(self, **kwargs) -> Response:
        """
        List of CORS hosts

        Args:
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=CORSHostsSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 Realm does not exist
        """
        url = self.gen_url("cors_hosts/")
        resp = self._get(url, **kwargs)
        return self.parse_response(resp, CORSHostsSchema)

    def create_cors_host(
        self,
        host: str,
        exclude_defaults: bool = True,
        **kwargs,
    ) -> Response:
        """
        Create a new CORS host

        Args:
            host: Host name
            exclude_defaults: Whether to exclude default values when dumping
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=CORSHostSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
        """
        model = CORSHostSchema(host=host)
        body = model.model_dump(exclude_defaults=exclude_defaults)
        url = self.gen_url("cors_hosts/")
        resp = self._post(url, json=body, **kwargs)
        return self.parse_response(resp, CORSHostSchema)

    def get_cors_host(self, cors_host_id: str, **kwargs) -> Response:
        """
        Returns a particular CORS host by id

        Args:
            cors_host_id: ID of the CORS host
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=CORSHostSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 CORS host does not exist
        """
        url = self.gen_url(f"cors_hosts/{cors_host_id}/")
        resp = self._get(url, **kwargs)
        return self.parse_response(resp, CORSHostSchema)

    def delete_cors_host(self, cors_host_id: str, **kwargs) -> Response:
        """
        Delete a particular CORS host by id

        Args:
            cors_host_id: ID of the CORS host to delete
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=None)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
        """
        url = self.gen_url(f"cors_hosts/{cors_host_id}/")
        resp = self._delete(url, **kwargs)
        return self.parse_response(resp, None)

    def get_group_settings(self, group_id: str, **kwargs) -> Response:
        """
        Group settings

        Args:
            group_id: ID of the group
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=GroupSettingPublicSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 Realm does not exist
        """
        url = self.gen_url(f"group/{group_id}/")
        resp = self._get(url, **kwargs)
        return self.parse_response(resp, GroupSettingPublicSchema)

    def update_group_settings(
        self,
        group_id: str,
        settings: Union[GroupSettingPublicSchema, Dict[str, Any]],
        exclude_defaults: bool = True,
        **kwargs,
    ) -> Response:
        """
        Change group settings

        Args:
            group_id: ID of the group
            settings: Group settings (either as GroupSettingPublicSchema
                or dict)
            exclude_defaults: Whether to exclude default values when dumping
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=GroupSettingPublicSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
        """
        body = (settings.model_dump(exclude_defaults=exclude_defaults)
                if is_pydantic_model(settings) else settings)
        url = self.gen_url(f"group/{group_id}/")
        resp = self._put(url, json=body, **kwargs)
        return self.parse_response(resp, GroupSettingPublicSchema)

    def partial_update_group_settings(
        self,
        group_id: str,
        settings: Union[GroupSettingPublicSchema, Dict[str, Any]],
        exclude_defaults: bool = True,
        **kwargs,
    ) -> Response:
        """
        Change group settings partially

        Args:
            group_id: ID of the group
            settings: Group settings to update (either as
                GroupSettingPublicSchema or dict)
            exclude_defaults: Whether to exclude default values when dumping
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=GroupSettingPublicSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
        """
        body = (settings.model_dump(exclude_defaults=exclude_defaults,
                                    exclude_unset=True)
                if is_pydantic_model(settings) else settings)
        url = self.gen_url(f"group/{group_id}/")
        resp = self._patch(url, json=body, **kwargs)
        return self.parse_response(resp, GroupSettingPublicSchema)

    def delete_group_settings(self, group_id: str, **kwargs) -> Response:
        """
        Delete group settings

        Args:
            group_id: ID of the group
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=None)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
        """
        url = self.gen_url(f"group/{group_id}/")
        resp = self._delete(url, **kwargs)
        return self.parse_response(resp, None)

    def get_kubernetes_settings(
        self,
        realm: str,
        page: int = 1,
        per_page: int = 10,
        **kwargs,
    ) -> Response:
        """
        List of settings for Kubernetes

        Args:
            realm: Realm name
            page: Which page number to fetch (default: 1)
            per_page: The number of items for each page (default: 10)
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=KubernetesSettingSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 Realm does not exist
        """
        params = {
            "page": page,
            "per_page": per_page,
        }
        url = self.gen_url(f"kubernetes/{realm}/")
        resp = self._get(url, params=params, **kwargs)
        return self.parse_response(resp, KubernetesSettingSchema)

    def partial_update_kubernetes_settings(
        self,
        realm: str,
        settings: Union[KubernetesSettingSchema, Dict[str, Any]],
        exclude_defaults: bool = True,
        **kwargs,
    ) -> Response:
        """
        Change Kubernetes settings

        Args:
            realm: Realm name
            settings: Kubernetes settings (either as KubernetesSettingSchema
                or dict)
            exclude_defaults: Whether to exclude default values when dumping
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=KubernetesSettingSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
        """
        body = (settings.model_dump(exclude_defaults=exclude_defaults,
                                    exclude_unset=True)
                if is_pydantic_model(settings) else settings)
        url = self.gen_url(f"kubernetes/{realm}/")
        resp = self._patch(url, json=body, **kwargs)
        return self.parse_response(resp, KubernetesSettingSchema)

    def get_kubernetes_setting(
        self,
        realm: str,
        setting_name: str,
        **kwargs,
    ) -> Response:
        """
        Returns value for a specific Kubernetes setting

        Args:
            realm: Realm name
            setting_name: Name of the setting
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=KubernetesSettingSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
        """
        url = self.gen_url(f"kubernetes/{realm}/{setting_name}/")
        resp = self._get(url, **kwargs)
        return self.parse_response(resp, KubernetesSettingSchema)

    def delete_kubernetes_setting(
        self,
        realm: str,
        setting_name: str,
        **kwargs,
    ) -> Response:
        """
        Delete a particular Kubernetes setting by name

        Args:
            realm: Realm name
            setting_name: Name of the setting to delete
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=None)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
        """
        url = self.gen_url(f"kubernetes/{realm}/{setting_name}/")
        resp = self._delete(url, **kwargs)
        return self.parse_response(resp, None)

    def get_merged_settings(
        self,
        ignore_logo_url: bool = False,
        **kwargs,
    ) -> Response:
        """
        Get merged settings for current user

        Args:
            ignore_logo_url: Whether to ignore the logo URL (default: False)
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=MergedSettingsSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 Realm does not exist
        """
        params = {"ignore_logo_url": ignore_logo_url}
        url = self.gen_url("merged/current/")
        resp = self._get(url, params=params, **kwargs)
        return self.parse_response(resp, MergedSettingsSchema)

    def get_user_merged_settings(
        self,
        user_id: str,
        ignore_logo_url: bool = False,
        **kwargs,
    ) -> Response:
        """
        Get merged settings for a specific user

        Args:
            user_id: ID of the user
            ignore_logo_url: Whether to ignore the logo URL (default: False)
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=MergedSettingsSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 Realm does not exist
        """
        params = {"ignore_logo_url": ignore_logo_url}
        url = self.gen_url(f"merged/{user_id}/")
        resp = self._get(url, params=params, **kwargs)
        return self.parse_response(resp, MergedSettingsSchema)

    def get_system_settings(
        self,
        ignore_logo_url: bool = False,
        **kwargs,
    ) -> Response:
        """
        System settings for current system domain

        Args:
            ignore_logo_url: Whether to ignore the logo URL (default: False)
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=SystemSettingPublicSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 Realm does not exist
        """
        params = {"ignore_logo_url": ignore_logo_url}
        url = self.gen_url("system/current/")
        resp = self._get(url, params=params, **kwargs)
        return self.parse_response(resp, SystemSettingPublicSchema)

    def update_system_settings(
        self,
        settings: Union[SystemSettingPublicSchema, Dict[str, Any]],
        exclude_defaults: bool = True,
        **kwargs,
    ) -> Response:
        """
        Change system settings for current system domain

        Args:
            settings: System settings (either as SystemSettingPublicSchema
                or dict)
            exclude_defaults: Whether to exclude default values when dumping
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=SystemSettingPublicSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
        """
        body = (settings.model_dump(exclude_defaults=exclude_defaults)
                if is_pydantic_model(settings) else settings)
        url = self.gen_url("system/current/")
        resp = self._put(url, json=body, **kwargs)
        return self.parse_response(resp, SystemSettingPublicSchema)

    def partial_update_system_settings(
        self,
        settings: Union[SystemSettingPublicSchema, Dict[str, Any]],
        exclude_defaults: bool = True,
        **kwargs,
    ) -> Response:
        """
        Partially update system settings for current system domain

        Args:
            settings: System settings to update (either as
                SystemSettingPublicSchema or dict)
            exclude_defaults: Whether to exclude default values when dumping
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=SystemSettingPublicSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
        """
        body = (settings.model_dump(exclude_defaults=exclude_defaults,
                                    exclude_unset=True)
                if is_pydantic_model(settings) else settings)
        url = self.gen_url("system/current/")
        resp = self._patch(url, json=body, **kwargs)
        return self.parse_response(resp, SystemSettingPublicSchema)

    def get_domain_system_settings(
        self,
        system_domain_id: str,
        ignore_logo_url: bool = False,
        **kwargs,
    ) -> Response:
        """
        System settings for a specific system domain

        Args:
            system_domain_id: ID of the system domain
            ignore_logo_url: Whether to ignore the logo URL (default: False)
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=SystemSettingPublicSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 Realm does not exist
        """
        params = {"ignore_logo_url": ignore_logo_url}
        url = self.gen_url(f"system/{system_domain_id}/")
        resp = self._get(url, params=params, **kwargs)
        return self.parse_response(resp, SystemSettingPublicSchema)

    def update_domain_system_settings(
        self,
        system_domain_id: str,
        settings: Union[SystemSettingPublicSchema, Dict[str, Any]],
        exclude_defaults: bool = True,
        **kwargs,
    ) -> Response:
        """
        Change system settings for a specific system domain

        Args:
            system_domain_id: ID of the system domain
            settings: System settings (either as SystemSettingPublicSchema
                or dict)
            exclude_defaults: Whether to exclude default values when dumping
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=SystemSettingPublicSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
        """
        body = (settings.model_dump(exclude_defaults=exclude_defaults)
                if is_pydantic_model(settings) else settings)
        url = self.gen_url(f"system/{system_domain_id}/")
        resp = self._put(url, json=body, **kwargs)
        return self.parse_response(resp, SystemSettingPublicSchema)

    def partial_update_domain_system_settings(
        self,
        system_domain_id: str,
        settings: Union[SystemSettingPublicSchema, Dict[str, Any]],
        exclude_defaults: bool = True,
        **kwargs,
    ) -> Response:
        """
        Partially update system settings for a specific system domain

        Args:
            system_domain_id: ID of the system domain
            settings: System settings to update (either as
            SystemSettingPublicSchema or dict)
            exclude_defaults: Whether to exclude default values when dumping
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=SystemSettingPublicSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
        """
        body = (settings.model_dump(exclude_defaults=exclude_defaults,
                                    exclude_unset=True)
                if is_pydantic_model(settings) else settings)
        url = self.gen_url(f"system/{system_domain_id}/")
        resp = self._patch(url, json=body, **kwargs)
        return self.parse_response(resp, SystemSettingPublicSchema)

    def remove_user_settings_attributes(
        self,
        attributes: Union[UserSettingRemoveAttributesSchema, Dict[str, Any]],
        exclude_defaults: bool = True,
        **kwargs,
    ) -> Response:
        """
        Remove attributes from user settings

        Args:
            attributes: Attributes to remove (either as
                UserSettingRemoveAttributesSchema or dict)
            exclude_defaults: Whether to exclude default values when dumping
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=None)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
        """
        body = (attributes.model_dump(exclude_defaults=exclude_defaults)
                if is_pydantic_model(attributes) else attributes)
        url = self.gen_url("user/attributes/")
        resp = self._delete(url, json=body, **kwargs)
        return self.parse_response(resp, None)

    def get_user_settings(self, user_id: str, **kwargs) -> Response:
        """
        User settings for a specific user

        Args:
            user_id: ID of the user
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=UserSettingSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 Realm does not exist
        """
        url = self.gen_url(f"user/{user_id}/")
        resp = self._get(url, **kwargs)
        return self.parse_response(resp, UserSettingSchema)

    def update_user_settings(
        self,
        user_id: str,
        settings: Union[UserSettingSchema, Dict[str, Any]],
        exclude_defaults: bool = True,
        **kwargs,
    ) -> Response:
        """
        Change user settings for a specific user

        Args:
            user_id: ID of the user
            settings: User settings (either as UserSettingSchema or dict)
            exclude_defaults: Whether to exclude default values when dumping
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=UserSettingSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
        """
        body = (settings.model_dump(exclude_defaults=exclude_defaults)
                if is_pydantic_model(settings) else settings)
        url = self.gen_url(f"user/{user_id}/")
        resp = self._put(url, json=body, **kwargs)
        return self.parse_response(resp, UserSettingSchema)

    def partial_update_user_settings(
        self,
        user_id: str,
        settings: Union[UserSettingSchema, Dict[str, Any]],
        exclude_defaults: bool = True,
        **kwargs,
    ) -> Response:
        """
        Partially update user settings for a specific user

        Args:
            user_id: ID of the user
            settings: User settings to update (either as UserSettingSchema
                or dict)
            exclude_defaults: Whether to exclude default values when dumping
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=UserSettingSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
        """
        body = (settings.model_dump(exclude_defaults=exclude_defaults,
                                    exclude_unset=True)
                if is_pydantic_model(settings) else settings)
        url = self.gen_url(f"user/{user_id}/")
        resp = self._patch(url, json=body, **kwargs)
        return self.parse_response(resp, UserSettingSchema)

    def delete_user_settings(self, user_id: str, **kwargs) -> Response:
        """
        Delete user settings for a specific user

        Args:
            user_id: ID of the user
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=None)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
        """
        url = self.gen_url(f"user/{user_id}/")
        resp = self._delete(url, **kwargs)
        return self.parse_response(resp, None)
