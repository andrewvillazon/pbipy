"""
Module implements a wrapper around the Power BI Rest API Group operations.

Full Group Operations documentation can be found at:

https://learn.microsoft.com/en-us/rest/api/power-bi/groups

"""

from pbipy.resources import Resource
from pbipy import _utils

from requests import Session


class Group(Resource):
    """
    A Power BI Group (better know as a Workspace).

    Users should initialize a `Group` object by calling the `group()` method
    on the `PowerBI` client, rather than creating directly.

    Examples
    --------
    Retrieving a `Group` object using a `pbi` client object.

    ```
    >>> my_group = pbi.group("a2f89923-421a-464e-bf4c-25eab39bb09f")
    ```

    Retrieve a list of users with access to a Group.

    ```
    >>> my_group = pbi.group("a2f89923-421a-464e-bf4c-25eab39bb09f")
    >>> group_users = my_group.users()
    ```

    """

    _REPR = [
        "id",
        "name",
    ]

    def __init__(
        self,
        id: str,
        session: Session,
        raw: dict = None,
        **kwargs,
    ) -> None:
        super().__init__(id, session, **kwargs)

        self.base_path = f"{self.BASE_URL}/groups/{self.id}"

        if raw:
            self._load_from_raw(raw)

    def add_user(
        self,
        identifier: str,
        principal_type: str,
        access_right: str,
        display_name: str = None,
        email_address: str = None,
        graph_id: str = None,
        profile: dict = None,
        user_type: str = None,
    ) -> None:
        """
        Grants the specified user the specified permissions to the workspace.

        Parameters
        ----------
        `identifier` : `str`
            Identifier of the principal.
        `principal_type` : `str`
            The principal type, e.g., "App", "Group", "None", or "User".
        `access_right` : `str`
            The access right (permission level) that a user has on the
            workspace, e.g., "Admin", "Contributor", "Member", "None",
            or "Viewer".
        `display_name` : `str`, optional
            Display name of the principal.
        `email_address` : `str`, optional
            Email address of the user.
        `graph_id` : `str`, optional
            Identifier of the principal in Microsoft Graph. Only available
            for admin APIs.
        `profile` : `dict`, optional
            A Power BI service principal profile. Only relevant for Power
            BI Embedded multi-tenancy solution.
        `user_type` : `str`, optional
            Type of the user.

        """

        payload = {
            "identifier": identifier,
            "groupUserAccessRight": access_right,
            "principalType": principal_type,
            "displayName": display_name,
            "emailAddress": email_address,
            "graphId": graph_id,
            "profile": profile,
            "userType": user_type,
        }

        prepared_payload = _utils.remove_no_values(payload)
        resource = self.base_path + "/users"

        _utils.post(resource, self.session, prepared_payload)

    def delete_user(
        self,
        user: str,
        profile: str = None,
    ) -> None:
        """
        Deletes the specified user permissions from the specified workspace.

        Parameters
        ----------
        `user` : `str`
            The email address of the user or object ID of the service principal
            to delete.
        `profile` : `str`, optional
            The service principal profile ID to delete.

        """

        if profile:
            resource = self.base_path + f"/users/{user}?profileId={profile}"
        else:
            resource = self.base_path + f"/users/{user}"

        _utils.delete(resource, self.session)

    def update_user(
        self,
        identifier: str,
        principal_type: str,
        access_right: str,
        display_name: str = None,
        email_address: str = None,
        graph_id: str = None,
        profile: dict = None,
        user_type: str = None,
    ) -> None:
        """
        Updates the specified user permissions on the workspace.

        Parameters
        ----------
        `identifier` : `str`
            Identifier of the principal.
        `principal_type` : `str`
            The principal type, e.g., "App", "Group", "None", or "User".
        `access_right` : `str`
            The access right (permission level) that a user has on the
            workspace, e.g., "Admin", "Contributor", "Member", "None",
            or "Viewer".
        `display_name` : `str`, optional
            Display name of the principal.
        `email_address` : `str`, optional
            Email address of the user.
        `graph_id` : `str`, optional
            Identifier of the principal in Microsoft Graph. Only available
            for admin APIs.
        `profile` : `dict`, optional
            A Power BI service principal profile. Only relevant for Power
            BI Embedded multi-tenancy solution.
        `user_type` : `str`, optional
            Type of the user.

        """

        payload = {
            "identifier": identifier,
            "groupUserAccessRight": access_right,
            "principalType": principal_type,
            "displayName": display_name,
            "emailAddress": email_address,
            "graphId": graph_id,
            "profile": profile,
            "userType": user_type,
        }

        prepared_payload = _utils.remove_no_values(payload)
        resource = self.base_path + "/users"

        _utils.put(resource, self.session, prepared_payload)

    def update(
        self,
        name: str = None,
        default_dataset_storage_format: str = None,
    ) -> "Group":
        """
        Update properties for this Group on the Power BI instance. First attempts
        to update the Group on the Power BI instance, and then reflects these
        changes in the Group.

        Parameters
        ----------
        `name` : `str`, optional
            The new name for the group.
        `default_dataset_storage_format` : `str`, optional
            The new Default Dataset Storage Format for the group.

        Returns
        -------
        `Group`
            The group with the specified values updated.

        Raises
        ------
        `ValueError`
            If no values to update were provided.

        """

        request_body = {
            "name": name,
            "defaultDatasetStorageFormat": default_dataset_storage_format,
        }
        request_body = _utils.remove_no_values(request_body)

        if not request_body:
            raise ValueError(
                "No options were provided to update. Please specify an option to update."
            )

        _utils.patch(
            self.base_path,
            self.session,
            request_body,
        )

        # Update existing group to reflect changes
        self.raw.update(request_body)

        for k, v in request_body.items():
            attr = _utils.to_identifier(k)
            attr = _utils.to_snake_case(attr)
            setattr(self, attr, v)

        return self

    def users(
        self,
        skip: int = None,
        top: int = None,
    ) -> list[dict]:
        """
        Returns a list of users that have access to the workspace.

        Parameters
        ----------
        `skip` : `int`, optional
            Skips the first n results.
        `top` : `int`, optional
            Returns onl the first n results.
        Returns
        -------
        `list[dict]`
            List of users that have access to the workspace.

        """

        params = {
            "$skip": skip,
            "$top": top,
        }

        prepared_params = _utils.remove_no_values(params)
        resource = self.base_path + "/users"

        raw = _utils.get_raw(
            resource,
            self.session,
            params=prepared_params,
        )

        return raw
