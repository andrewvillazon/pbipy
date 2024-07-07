from requests import Session

from pbipy.resources import Resource
from pbipy import _utils


class Gateway(Resource):
    def __init__(
        self,
        id: str,
        session: Session,
        raw=None,
    ) -> None:
        super().__init__(id, session)

        self.resource_path = f"/gateways/{self.id}"
        self.base_path = f"{self.BASE_URL}{self.resource_path}"

        if raw:
            self._load_from_raw(raw)

    def datasources(
        self,
    ) -> list[dict]:
        resource = self.base_path + "/datasources"
        raw = _utils.get_raw(
            resource,
            self.session,
        )

        return raw

    def datasource(
        self,
        datasource: str,
    ) -> dict:
        """
        Return the specified data source from the Gateway.

        Parameters
        ----------
        `datasource` : `str`
            Id of the target data source.

        Returns
        -------
        `dict`
            The specified data source.

        """

        resource = self.base_path + f"/datasources/{datasource}"
        raw = _utils.get_raw(
            resource,
            self.session,
        )

        return raw

    def create_datasource(
        self,
        connection_details: str,
        credential_details: dict,
        datasource_name: str,
        datasource_type: str,
    ) -> dict:
        """
        Create a new data source on the Gateway.

        Parameters
        ----------
        `connection_details` : `str`
            String connection details, e.g., `"{\"server\":\"MyServer\",\"database\":\"MyDatabase\"}"`
        `credential_details` : `dict`
            The data source credential details.
        `datasource_name` : `str`
            The data source name.
        `datasource_type` : `str`
            The type of the data source, e.g., AnalysisServices, Excel, etc.

        Returns
        -------
        `dict`
            The newly created data source.
        
        Notes
        -----
        See https://learn.microsoft.com/en-us/rest/api/power-bi/gateways/create-datasource
        for how to specify `connection_details` and `credential_details`.

        """

        resource = self.base_path + "/datasources"

        payload = {
            "connectionDetails": connection_details,
            "credentialDetails": credential_details,
            "dataSourceName": datasource_name,
            "dataSourceType": datasource_type,
        }

        raw = _utils.post_raw(
            resource,
            self.session,
            payload=payload,
        )

        return raw

    def datasource_status(
        self,
        datasource: str,
    ) -> dict:
        """
        Check the connectivity status of the specified data source.

        Parameters
        ----------
        `datasource` : `str`
            Id of the target data source.

        Returns
        -------
        `dict`
            The status of the data source.

        Notes
        ------
        * When the data source is unreachable, the Get Datasource Status endpoint
        returns a 400 status code. This method will raise the 400 as a `RequestsException`.
        To get the gateway error details, handle the exception and inspect
        it's `response` attribute. e.g., `error_js = error.response.json()`

        """

        resource = self.base_path + f"/datasources/{datasource}/status"
        raw = _utils.get_raw(
            resource,
            self.session,
        )

        return raw

    def datasource_users(
        self,
        datasource: str,
    ) -> list[dict]:
        """
        Returns a list of users who have access to the specified data source.

        Parameters
        ----------
        `datasource` : `str`
            Id of the target data source.

        Returns
        -------
        `list[dict]`
            List of Power BI users with access to the data source.

        """

        resource = self.base_path + f"/datasources/{datasource}/users"
        raw = _utils.get_raw(
            resource,
            self.session,
        )

        return raw

    def delete_datasource_user(
        self,
        datasource: str,
        email_address: str,
        profile_id: str = None,
    ) -> None:
        """
        Remove the specified user from the specified data source.

        Parameters
        ----------
        `datasource` : `str`
            Id of the target data source.
        `email_address` : `str`
            The user's email address or the object Id of the service principal.
        `profile_id` : `str`, optional
            Service principal profile Id to delete.

        """

        resource = self.base_path + f"/datasources/{datasource}/users/{email_address}"
        params = {"profileId": profile_id}

        _utils.delete(
            resource,
            self.session,
            params=params,
        )
