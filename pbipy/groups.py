from pbipy.resources import Resource
from pbipy.utils import remove_no_values


from requests import Session


class Group(Resource):
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

        prepared_payload = remove_no_values(payload)
        resource = self.base_path + "/users"

        self.post(resource, self.session, prepared_payload)

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

        self.delete(resource, self.session)

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

        prepared_payload = remove_no_values(payload)
        resource = self.base_path + "/users"

        self.put(resource, self.session, prepared_payload)

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

        prepared_params = remove_no_values(params)
        resource = self.base_path + "/users"

        raw = self.get_raw(resource, self.session, params=prepared_params)

        return raw