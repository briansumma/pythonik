from typing import (
    Any,
    Dict,
    Optional,
    Union,
)

from pythonik.models.base import Response
from pythonik.models.users import (
    GroupMappingSchema,
    GroupMappingsSchema,
    GroupSchema,
    GroupsSchema,
    OtpEditSchema,
    OtpSchema,
    ReindexGroupSchema,
    ReindexUserSchema,
    UserCreateSchema,
    UserRolesSchema,
    UserSamlIdpUpdateSchema,
    UserSchema,
    UsersSchema,
)
from pythonik.specs._internal_utils import is_pydantic_model
from pythonik.specs.base import Spec


class UsersSpec(Spec):
    server = "API/users/"

    # pylint: disable=too-many-positional-arguments
    def list_users(
        self,
        page: int = 1,
        per_page: int = 10,
        sort: Optional[str] = None,
        date_created: Optional[str] = None,
        date_modified: Optional[str] = None,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        groups: Optional[str] = None,
        hide_email: Optional[str] = None,
        hide_phone: Optional[str] = None,
        is_admin: Optional[str] = None,
        password_changed: Optional[str] = None,
        phone: Optional[str] = None,
        photo: Optional[str] = None,
        status: Optional[str] = None,
        query: Optional[str] = None,
        ids: Optional[str] = None,
        **kwargs,
    ) -> Response:
        """
        List of users with details

        Args:
            page: Which page number to fetch (default: 1)
            per_page: The number of items for each page (default: 10)
            sort: A comma separated list of fieldnames with order
                (e.g., first_name,asc;last_name,desc)
            date_created: Filter by date_created
            date_modified: Filter by date_modified
            email: Filter by email
            first_name: Filter by first_name
            last_name: Filter by last_name
            groups: Filter by groups
            hide_email: Filter by hide_email
            hide_phone: Filter by hide_phone
            is_admin: Filter by is_admin
            password_changed: Filter by password_changed
            phone: Filter by phone
            photo: Filter by photo
            status: Filter by status
            query: Filter by any of first_name, last_name and email with
                wildcard support
            ids: Filter list of id:s (comma separated)
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=UsersSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 Specified page does not exist
        """
        params: Dict[str, Any] = {
            "page": page,
            "per_page": per_page,
        }

        # Add optional parameters if provided
        if sort is not None:
            params["sort"] = sort
        if date_created is not None:
            params["date_created"] = date_created
        if date_modified is not None:
            params["date_modified"] = date_modified
        if email is not None:
            params["email"] = email
        if first_name is not None:
            params["first_name"] = first_name
        if last_name is not None:
            params["last_name"] = last_name
        if groups is not None:
            params["groups"] = groups
        if hide_email is not None:
            params["hide_email"] = hide_email
        if hide_phone is not None:
            params["hide_phone"] = hide_phone
        if is_admin is not None:
            params["is_admin"] = is_admin
        if password_changed is not None:
            params["password_changed"] = password_changed
        if phone is not None:
            params["phone"] = phone
        if photo is not None:
            params["photo"] = photo
        if status is not None:
            params["status"] = status
        if query is not None:
            params["query"] = query
        if ids is not None:
            params["ids"] = ids

        url = self.gen_url("")
        resp = self._get(url, params=params, **kwargs)
        return self.parse_response(resp, UsersSchema)

    def create_user(
        self,
        user: Union[UserCreateSchema, Dict[str, Any]],
        exclude_defaults: bool = True,
        **kwargs,
    ) -> Response:
        """
        Create a new user

        Args:
            user: User data (either as UserCreateSchema or dict)
            exclude_defaults: Whether to exclude default values when dumping
                Pydantic models
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=UserSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
        """
        body = (user.model_dump(exclude_defaults=exclude_defaults)
                if is_pydantic_model(user) else user)
        url = self.gen_url("")
        resp = self._post(url, json=body, **kwargs)
        return self.parse_response(resp, UserSchema)

    # pylint: disable=too-many-positional-arguments
    def list_users_basic(
        self,
        page: int = 1,
        per_page: int = 10,
        sort: Optional[str] = None,
        date_created: Optional[str] = None,
        date_modified: Optional[str] = None,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        groups: Optional[str] = None,
        hide_email: Optional[str] = None,
        hide_phone: Optional[str] = None,
        is_admin: Optional[str] = None,
        password_changed: Optional[str] = None,
        phone: Optional[str] = None,
        photo: Optional[str] = None,
        status: Optional[str] = None,
        query: Optional[str] = None,
        ids: Optional[str] = None,
        emails: Optional[str] = None,
        **kwargs,
    ) -> Response:
        """
        List of users without details

        Args:
            page: Which page number to fetch (default: 1)
            per_page: The number of items for each page (default: 10)
            sort: A comma separated list of fieldnames with order
                (e.g., first_name,asc;last_name,desc)
            date_created: Filter by date_created
            date_modified: Filter by date_modified
            email: Filter by email
            first_name: Filter by first_name
            last_name: Filter by last_name
            groups: Filter by groups
            hide_email: Filter by hide_email
            hide_phone: Filter by hide_phone
            is_admin: Filter by is_admin
            password_changed: Filter by password_changed
            phone: Filter by phone
            photo: Filter by photo
            status: Filter by status
            query: Filter by any of first_name, last_name and email with
                wildcard support
            ids: Filter list of id:s (comma separated)
            emails: Filter by list of emails (comma separated)
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=UsersSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 Specified page does not exist
        """
        params: Dict[str, Any] = {
            "page": page,
            "per_page": per_page,
        }

        # Add optional parameters if provided
        if sort is not None:
            params["sort"] = sort
        if date_created is not None:
            params["date_created"] = date_created
        if date_modified is not None:
            params["date_modified"] = date_modified
        if email is not None:
            params["email"] = email
        if first_name is not None:
            params["first_name"] = first_name
        if last_name is not None:
            params["last_name"] = last_name
        if groups is not None:
            params["groups"] = groups
        if hide_email is not None:
            params["hide_email"] = hide_email
        if hide_phone is not None:
            params["hide_phone"] = hide_phone
        if is_admin is not None:
            params["is_admin"] = is_admin
        if password_changed is not None:
            params["password_changed"] = password_changed
        if phone is not None:
            params["phone"] = phone
        if photo is not None:
            params["photo"] = photo
        if status is not None:
            params["status"] = status
        if query is not None:
            params["query"] = query
        if ids is not None:
            params["ids"] = ids
        if emails is not None:
            params["emails"] = emails

        url = self.gen_url("basic/")
        resp = self._get(url, params=params, **kwargs)
        return self.parse_response(resp, UsersSchema)

    def get_current_user(self, **kwargs) -> Response:
        """
        Returns current user

        Args:
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=UserSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 User does not exist
        """
        url = self.gen_url("current/")
        resp = self._get(url, **kwargs)
        return self.parse_response(resp, UserSchema)

    def update_current_user(
        self,
        user: Union[UserSchema, Dict[str, Any]],
        exclude_defaults: bool = True,
        **kwargs,
    ) -> Response:
        """
        Update current user

        Args:
            user: User data (either as UserSchema or dict)
            exclude_defaults: Whether to exclude default values when dumping
                Pydantic models
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=UserSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 User does not exist
        """
        body = (user.model_dump(exclude_defaults=exclude_defaults)
                if is_pydantic_model(user) else user)
        url = self.gen_url("current/")
        resp = self._put(url, json=body, **kwargs)
        return self.parse_response(resp, UserSchema)

    def partial_update_current_user(
        self,
        user: Union[UserSchema, Dict[str, Any]],
        exclude_defaults: bool = True,
        **kwargs,
    ) -> Response:
        """
        Partially update current user

        Args:
            user: User data to update (either as UserSchema or dict)
            exclude_defaults: Whether to exclude default values when dumping
                Pydantic models
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=UserSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 User does not exist
        """
        body = (user.model_dump(exclude_defaults=exclude_defaults,
                                exclude_unset=True)
                if is_pydantic_model(user) else user)
        url = self.gen_url("current/")
        resp = self._patch(url, json=body, **kwargs)
        return self.parse_response(resp, UserSchema)

    def get_user(self, user_id: str, **kwargs) -> Response:
        """
        Returns a particular user by id

        Args:
            user_id: ID of the user
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=UserSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 User does not exist
        """
        url = self.gen_url(f"{user_id}/")
        resp = self._get(url, **kwargs)
        return self.parse_response(resp, UserSchema)

    def update_user(
        self,
        user_id: str,
        user: Union[UserSchema, Dict[str, Any]],
        exclude_defaults: bool = True,
        **kwargs,
    ) -> Response:
        """
        Update user

        Args:
            user_id: ID of the user
            user: User data (either as UserSchema or dict)
            exclude_defaults: Whether to exclude default values when dumping
                Pydantic models
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=UserSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 User does not exist
        """
        body = (user.model_dump(exclude_defaults=exclude_defaults)
                if is_pydantic_model(user) else user)
        url = self.gen_url(f"{user_id}/")
        resp = self._put(url, json=body, **kwargs)
        return self.parse_response(resp, UserSchema)

    def partial_update_user(
        self,
        user_id: str,
        user: Union[UserSchema, Dict[str, Any]],
        exclude_defaults: bool = True,
        **kwargs,
    ) -> Response:
        """
        Partially update user

        Args:
            user_id: ID of the user
            user: User data to update (either as UserSchema or dict)
            exclude_defaults: Whether to exclude default values when dumping
                Pydantic models
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=UserSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 User does not exist
        """
        body = (user.model_dump(exclude_defaults=exclude_defaults,
                                exclude_unset=True)
                if is_pydantic_model(user) else user)
        url = self.gen_url(f"{user_id}/")
        resp = self._patch(url, json=body, **kwargs)
        return self.parse_response(resp, UserSchema)

    def delete_user(self, user_id: str, **kwargs) -> Response:
        """
        Delete a particular user by id

        Args:
            user_id: ID of the user to delete
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=None)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 User does not exist
        """
        url = self.gen_url(f"{user_id}/")
        resp = self._delete(url, **kwargs)
        return self.parse_response(resp, None)

    def get_current_user_roles(self, **kwargs) -> Response:
        """
        Returns current user roles

        Args:
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=UserRolesSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
        """
        url = self.gen_url("current/roles/")
        resp = self._get(url, **kwargs)
        return self.parse_response(resp, UserRolesSchema)

    def get_user_roles(self, user_id: str, **kwargs) -> Response:
        """
        Returns user roles by user_id

        Args:
            user_id: ID of the user
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=UserRolesSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
        """
        url = self.gen_url(f"{user_id}/roles/")
        resp = self._get(url, **kwargs)
        return self.parse_response(resp, UserRolesSchema)

    def check_user_role(self, user_id: str, role: str, **kwargs) -> Response:
        """
        Returns user roles by user_id

        Args:
            user_id: ID of the user
            role: Role to check
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=None) - Returns 200 if user has role, 404 if not

        Raises:
            - 401 Token is invalid
        """
        url = self.gen_url(f"{user_id}/roles/{role}/")
        resp = self._get(url, **kwargs)
        return self.parse_response(resp, None)

    def upload_user_photo(self, user_id: str, photo: bytes,
                          **kwargs) -> Response:
        """
        Upload user photo image

        Args:
            user_id: ID of the user
            photo: User photo image data
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response containing URLs for the uploaded photo

        Raises:
            - 400 Bad request
            - 404 User does not exist
        """
        url = self.gen_url(f"{user_id}/photo/")
        files = {"photo": photo}
        resp = self._post(url, files=files, **kwargs)
        return self.parse_response(resp, None)

    def delete_user_photo(self, user_id: str, **kwargs) -> Response:
        """
        Delete a photo image of a specified user

        Args:
            user_id: ID of the user
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=None)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 User does not exist
        """
        url = self.gen_url(f"{user_id}/photo/")
        resp = self._delete(url, **kwargs)
        return self.parse_response(resp, None)

    def upload_current_user_photo(self, photo: bytes, **kwargs) -> Response:
        """
        Upload current user photo image

        Args:
            photo: User photo image data
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response containing URLs for the uploaded photo

        Raises:
            - 400 Bad request
            - 404 User does not exist
        """
        url = self.gen_url("current/photo/")
        files = {"photo": photo}
        resp = self._post(url, files=files, **kwargs)
        return self.parse_response(resp, None)

    def delete_current_user_photo(self, **kwargs) -> Response:
        """
        Delete current user photo image

        Args:
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=None)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 User does not exist
        """
        url = self.gen_url("current/photo/")
        resp = self._delete(url, **kwargs)
        return self.parse_response(resp, None)

    def reindex_user(
        self,
        user_id: str,
        reindex_data: Optional[Union[ReindexUserSchema, Dict[str,
                                                             Any]]] = None,
        exclude_defaults: bool = True,
        **kwargs,
    ) -> Response:
        """
        Reindex a particular user by id

        Args:
            user_id: ID of the user
            reindex_data: Reindex data (either as ReindexUserSchema or dict)
            exclude_defaults: Whether to exclude default values when dumping
                Pydantic models
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=UserSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 User does not exist
        """
        url = self.gen_url(f"{user_id}/reindex/")
        body = None
        if reindex_data is not None:
            body = (reindex_data.model_dump(exclude_defaults=exclude_defaults)
                    if is_pydantic_model(reindex_data) else reindex_data)
        resp = self._post(url, json=body, **kwargs)
        return self.parse_response(resp, UserSchema)

    # pylint: disable=too-many-positional-arguments
    def list_groups(
        self,
        page: int = 1,
        per_page: int = 10,
        sort: Optional[str] = None,
        alias: Optional[str] = None,
        description: Optional[str] = None,
        name: Optional[str] = None,
        roles: Optional[str] = None,
        date_created: Optional[str] = None,
        date_modified: Optional[str] = None,
        query: Optional[str] = None,
        ids: Optional[str] = None,
        **kwargs,
    ) -> Response:
        """
        List groups with details

        Args:
            page: Which page number to fetch (default: 1)
            per_page: The number of items for each page (default: 10)
            sort: A comma separated list of fieldnames with order
                (e.g., name,asc;alias,desc)
            alias: Filter by alias
            description: Filter by description
            name: Filter by name
            roles: Filter by roles
            date_created: Filter by date_created
            date_modified: Filter by date_modified
            query: Filter by any of field with wildcard support
            ids: Filter list of id:s (comma separated)
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=GroupsSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 Requested page does not exist
        """
        params: Dict[str, Any] = {
            "page": page,
            "per_page": per_page,
        }

        # Add optional parameters if provided
        if sort is not None:
            params["sort"] = sort
        if alias is not None:
            params["alias"] = alias
        if description is not None:
            params["description"] = description
        if name is not None:
            params["name"] = name
        if roles is not None:
            params["roles"] = roles
        if date_created is not None:
            params["date_created"] = date_created
        if date_modified is not None:
            params["date_modified"] = date_modified
        if query is not None:
            params["query"] = query
        if ids is not None:
            params["ids"] = ids

        url = self.gen_url("groups/")
        resp = self._get(url, params=params, **kwargs)
        return self.parse_response(resp, GroupsSchema)

    def create_group(
        self,
        group: Union[GroupSchema, Dict[str, Any]],
        exclude_defaults: bool = True,
        **kwargs,
    ) -> Response:
        """
        Create a new group

        Args:
            group: Group data (either as GroupSchema or dict)
            exclude_defaults: Whether to exclude default values when dumping
                Pydantic models
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=GroupSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
        """
        body = (group.model_dump(exclude_defaults=exclude_defaults)
                if is_pydantic_model(group) else group)
        url = self.gen_url("groups/")
        resp = self._post(url, json=body, **kwargs)
        return self.parse_response(resp, GroupSchema)

    # pylint: disable=too-many-positional-arguments
    def list_groups_basic(
        self,
        page: int = 1,
        per_page: int = 10,
        sort: Optional[str] = None,
        alias: Optional[str] = None,
        description: Optional[str] = None,
        name: Optional[str] = None,
        roles: Optional[str] = None,
        date_created: Optional[str] = None,
        date_modified: Optional[str] = None,
        query: Optional[str] = None,
        ids: Optional[str] = None,
        **kwargs,
    ) -> Response:
        """
        List groups info without details

        Args:
            page: Which page number to fetch (default: 1)
            per_page: The number of items for each page (default: 10)
            sort: A comma separated list of fieldnames with order
                (e.g., name,asc;alias,desc)
            alias: Filter by alias
            description: Filter by description
            name: Filter by name
            roles: Filter by roles
            date_created: Filter by date_created
            date_modified: Filter by date_modified
            query: Filter by any of first_name, last_name and email with
                wildcard support
            ids: Filter list of id:s (comma separated)
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=GroupsSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 Requested page does not exist
        """
        params: Dict[str, Any] = {
            "page": page,
            "per_page": per_page,
        }

        # Add optional parameters if provided
        if sort is not None:
            params["sort"] = sort
        if alias is not None:
            params["alias"] = alias
        if description is not None:
            params["description"] = description
        if name is not None:
            params["name"] = name
        if roles is not None:
            params["roles"] = roles
        if date_created is not None:
            params["date_created"] = date_created
        if date_modified is not None:
            params["date_modified"] = date_modified
        if query is not None:
            params["query"] = query
        if ids is not None:
            params["ids"] = ids

        url = self.gen_url("groups/basic/")
        resp = self._get(url, params=params, **kwargs)
        return self.parse_response(resp, GroupsSchema)

    def get_group(self, group_id: str, **kwargs) -> Response:
        """
        Returns a particular group by id

        Args:
            group_id: ID of the group
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=GroupSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 Group does not exist
        """
        url = self.gen_url(f"groups/{group_id}/")
        resp = self._get(url, **kwargs)
        return self.parse_response(resp, GroupSchema)

    def update_group(
        self,
        group_id: str,
        group: Union[GroupSchema, Dict[str, Any]],
        exclude_defaults: bool = True,
        **kwargs,
    ) -> Response:
        """
        Update group

        Args:
            group_id: ID of the group
            group: Group data (either as GroupSchema or dict)
            exclude_defaults: Whether to exclude default values when dumping
                Pydantic models
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=GroupSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 Group does not exist
        """
        body = (group.model_dump(exclude_defaults=exclude_defaults)
                if is_pydantic_model(group) else group)
        url = self.gen_url(f"groups/{group_id}/")
        resp = self._put(url, json=body, **kwargs)
        return self.parse_response(resp, GroupSchema)

    def partial_update_group(
        self,
        group_id: str,
        group: Union[GroupSchema, Dict[str, Any]],
        exclude_defaults: bool = True,
        **kwargs,
    ) -> Response:
        """
        Update group

        Args:
            group_id: ID of the group
            group: Group data to update (either as GroupSchema or dict)
            exclude_defaults: Whether to exclude default values when dumping
                Pydantic models
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=GroupSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 Group does not exist
        """
        body = (group.model_dump(exclude_defaults=exclude_defaults,
                                 exclude_unset=True)
                if is_pydantic_model(group) else group)
        url = self.gen_url(f"groups/{group_id}/")
        resp = self._patch(url, json=body, **kwargs)
        return self.parse_response(resp, GroupSchema)

    def delete_group(self, group_id: str, **kwargs) -> Response:
        """
        Delete a particular group by id

        Args:
            group_id: ID of the group to delete
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=None)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 Group does not exist
        """
        url = self.gen_url(f"groups/{group_id}/")
        resp = self._delete(url, **kwargs)
        return self.parse_response(resp, None)

    def upload_group_logo(self, group_id: str, logo: bytes,
                          **kwargs) -> Response:
        """
        Upload group logo image

        Args:
            group_id: ID of the group
            logo: Group logo image data
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response containing URL for the uploaded logo

        Raises:
            - 400 Bad request
            - 404 Group does not exist
        """
        url = self.gen_url(f"groups/{group_id}/logo/")
        files = {"logo": logo}
        resp = self._post(url, files=files, **kwargs)
        return self.parse_response(resp, None)

    def delete_group_logo(self, group_id: str, **kwargs) -> Response:
        """
        Delete group logo image

        Args:
            group_id: ID of the group
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=None)

        Raises:
            - 400 Bad request
            - 404 Group does not exist
        """
        url = self.gen_url(f"groups/{group_id}/logo/")
        resp = self._delete(url, **kwargs)
        return self.parse_response(resp, None)

    def reindex_group(
        self,
        group_id: str,
        reindex_data: Optional[Union[ReindexGroupSchema, Dict[str,
                                                              Any]]] = None,
        exclude_defaults: bool = True,
        **kwargs,
    ) -> Response:
        """
        Reindex a particular group by id

        Args:
            group_id: ID of the group
            reindex_data: Reindex data (either as ReindexGroupSchema or dict)
            exclude_defaults: Whether to exclude default values when dumping
                Pydantic models
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=UserSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 Group does not exist
        """
        url = self.gen_url(f"groups/{group_id}/reindex/")
        body = None
        if reindex_data is not None:
            body = (reindex_data.model_dump(exclude_defaults=exclude_defaults)
                    if is_pydantic_model(reindex_data) else reindex_data)
        resp = self._post(url, json=body, **kwargs)
        return self.parse_response(resp, UserSchema)

    def add_user_to_group(self, group_id: str, user_id: str,
                          **kwargs) -> Response:
        """
        Add user into a group

        Args:
            group_id: ID of the group
            user_id: ID of the user
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=UserSchema)

        Raises:
            - 401 Token is invalid
            - 404 User or Group does not exist
        """
        url = self.gen_url(f"groups/{group_id}/users/{user_id}/")
        resp = self._post(url, **kwargs)
        return self.parse_response(resp, UserSchema)

    def remove_user_from_group(self, group_id: str, user_id: str,
                               **kwargs) -> Response:
        """
        Delete a user from group

        Args:
            group_id: ID of the group
            user_id: ID of the user
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=UserSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 User or Group does not exist
        """
        url = self.gen_url(f"groups/{group_id}/users/{user_id}/")
        resp = self._delete(url, **kwargs)
        return self.parse_response(resp, UserSchema)

    def list_group_mappings(
        self,
        per_page: Optional[int] = None,
        last_id: Optional[str] = None,
        **kwargs,
    ) -> Response:
        """
        Get all group mappings

        Args:
            per_page: The number of items for each page
            last_id: Last ID for pagination
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=GroupMappingsSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 Requested page does not exist
        """
        params: Dict[str, Any] = {}
        if per_page is not None:
            params["per_page"] = per_page
        if last_id is not None:
            params["last_id"] = last_id

        url = self.gen_url("groups/mappings/")
        resp = self._get(url, params=params, **kwargs)
        return self.parse_response(resp, GroupMappingsSchema)

    def create_group_mapping(
        self,
        mapping: Union[GroupMappingSchema, Dict[str, Any]],
        exclude_defaults: bool = True,
        **kwargs,
    ) -> Response:
        """
        Create a new group mapping

        Args:
            mapping: Group mapping data (either as GroupMappingSchema or dict)
            exclude_defaults: Whether to exclude default values when dumping
                Pydantic models
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=GroupMappingSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 409 Group mapping already exists
        """
        body = (mapping.model_dump(exclude_defaults=exclude_defaults)
                if is_pydantic_model(mapping) else mapping)
        url = self.gen_url("groups/mappings/")
        resp = self._post(url, json=body, **kwargs)
        return self.parse_response(resp, GroupMappingSchema)

    def get_group_mapping(self, name: str, **kwargs) -> Response:
        """
        Get a group mapping

        Args:
            name: Name of the group mapping
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=GroupMappingSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 Requested page does not exist
        """
        url = self.gen_url(f"groups/mappings/{name}/")
        resp = self._get(url, **kwargs)
        return self.parse_response(resp, GroupMappingSchema)

    def delete_group_mapping(self, name: str, **kwargs) -> Response:
        """
        Delete group mapping by name

        Args:
            name: Name of the group mapping to delete
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=None)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 Group mapping does not exist
        """
        url = self.gen_url(f"groups/mappings/{name}/")
        resp = self._delete(url, **kwargs)
        return self.parse_response(resp, None)

    def get_otp_configuration(self, **kwargs) -> Response:
        """
        Get current otp settings

        Args:
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response with OTP configuration

        Raises:
            - 400 Bad request
            - 401 Code is invalid
        """
        url = self.gen_url("current/otp/configure/")
        resp = self._get(url, **kwargs)
        return self.parse_response(resp, None)

    def configure_otp(
        self,
        otp_config: Union[OtpEditSchema, Dict[str, Any]],
        exclude_defaults: bool = True,
        **kwargs,
    ) -> Response:
        """
        Configure OTP settings

        Args:
            otp_config: OTP configuration (either as OtpEditSchema or dict)
            exclude_defaults: Whether to exclude default values when dumping
                Pydantic models
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=None)

        Raises:
            - 400 Bad request
            - 401 Code is invalid
        """
        body = (otp_config.model_dump(exclude_defaults=exclude_defaults)
                if is_pydantic_model(otp_config) else otp_config)
        url = self.gen_url("current/otp/configure/")
        resp = self._post(url, json=body, **kwargs)
        return self.parse_response(resp, None)

    def setup_totp(
        self,
        otp_config: Optional[Union[OtpSchema, Dict[str, Any]]] = None,
        exclude_defaults: bool = True,
        **kwargs,
    ) -> Response:
        """
        Setup TOTP

        Args:
            otp_config: OTP configuration (either as OtpSchema or dict)
            exclude_defaults: Whether to exclude default values when dumping
                Pydantic models
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response with TOTP configuration

        Raises:
            - 400 Bad request
        """
        body = None
        if otp_config is not None:
            body = (otp_config.model_dump(exclude_defaults=exclude_defaults)
                    if is_pydantic_model(otp_config) else otp_config)
        url = self.gen_url("current/totp/configure/")
        resp = self._post(url, json=body, **kwargs)
        return self.parse_response(resp, None)

    def validate_totp_configuration(
        self,
        otp_config: Union[OtpSchema, Dict[str, Any]],
        exclude_defaults: bool = True,
        **kwargs,
    ) -> Response:
        """
        Validate TOTP configuration

        Args:
            otp_config: OTP configuration (either as OtpSchema or dict)
            exclude_defaults: Whether to exclude default values when dumping
                Pydantic models
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=None)

        Raises:
            - 400 Bad request
            - 401 Code is invalid
        """
        body = (otp_config.model_dump(exclude_defaults=exclude_defaults)
                if is_pydantic_model(otp_config) else otp_config)
        url = self.gen_url("current/totp/validate_configuration/")
        resp = self._post(url, json=body, **kwargs)
        return self.parse_response(resp, None)

    def delete_totp_configuration(
        self,
        otp_config: Union[OtpSchema, Dict[str, Any]],
        exclude_defaults: bool = True,
        **kwargs,
    ) -> Response:
        """
        Delete TOTP configuration

        Args:
            otp_config: OTP configuration (either as OtpSchema or dict)
            exclude_defaults: Whether to exclude default values when dumping
                Pydantic models
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=None)

        Raises:
            - 400 Bad request
        """
        body = (otp_config.model_dump(exclude_defaults=exclude_defaults)
                if is_pydantic_model(otp_config) else otp_config)
        url = self.gen_url("current/totp/configure/")
        resp = self._delete(url, json=body, **kwargs)
        return self.parse_response(resp, None)

    def update_user_saml_idp(
        self,
        user_id: str,
        saml_idp: Union[UserSamlIdpUpdateSchema, Dict[str, Any]],
        exclude_defaults: bool = True,
        **kwargs,
    ) -> Response:
        """
        Update a user's SAML IdP settings

        Args:
            user_id: ID of the user
            saml_idp: SAML IdP settings (either as UserSamlIdpUpdateSchema
                or dict)
            exclude_defaults: Whether to exclude default values when dumping
                Pydantic models
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=UserSchema)

        Raises:
            - 400 Bad request
            - 401 Token is invalid
            - 404 User does not exist
        """
        body = (saml_idp.model_dump(exclude_defaults=exclude_defaults)
                if is_pydantic_model(saml_idp) else saml_idp)
        url = self.gen_url(f"{user_id}/saml/")
        resp = self._put(url, json=body, **kwargs)
        return self.parse_response(resp, UserSchema)

    def remove_user_saml_idp(self, user_id: str, **kwargs) -> Response:
        """
        Remove a user's SAML IdP setting

        Args:
            user_id: ID of the user
            **kwargs: Additional kwargs to pass to the request

        Returns:
            Response(model=UserSchema)

        Raises:
            - 401 Token is invalid
            - 404 User does not exist
        """
        url = self.gen_url(f"{user_id}/saml/")
        resp = self._delete(url, **kwargs)
        return self.parse_response(resp, UserSchema)
