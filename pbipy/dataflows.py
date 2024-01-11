"""
Module implements a wrapper around the Power BI Rest API Dataflow operations.

Full Dataflow Operations documentation can be found at:

https://learn.microsoft.com/en-us/rest/api/power-bi/dataflows

"""

from requests import Session

from pbipy.resources import Resource
from pbipy import _utils


class Dataflow(Resource):
    """
    A Power BI Dataflow.

    Users should initialize a `Dataflow` object by calling the `dataflow()` method
    on the `PowerBI` client, rather than creating directly.

    Examples
    --------
    Retrieving a `Dataflow` object using a `pbi` client object.

    ```
    >>> my_dataflow = pbi.dataflow("bd32e5c0-363f-430b-a03b-5535a4804b9b")
    ```

    """

    _REPR = [
        "id",
        "name",
        "description",
        "group_id",
    ]

    def __init__(
        self,
        id: str,
        session: Session,
        group_id: str,
        raw: dict = None,
    ) -> None:
        super().__init__(id, session)

        self.group_id = group_id

        self.resource_path = f"/groups/{self.group_id}/dataflows/{self.id}"
        self.base_path = f"{self.BASE_URL}{self.resource_path}"

        if raw:
            self._load_from_raw(raw)

    def datasources(
        self,
    ) -> list[dict]:
        """
        Return a list of Datasources for the Dataflow.

        Returns
        -------
        `list[dict]`
            The list of Datasources associated with the Dataflow.

        """

        resource = self.base_path + "/datasources"
        raw = _utils.get_raw(
            resource,
            self.session,
        )

        return raw

    def refresh(
        self,
        notify_option: str,
        process_type: str = None,
    ) -> None:
        """
        Trigger a refresh of the Dataflow.

        Parameters
        ----------
        `notify_option` : `str`
            Email notification options. Supported options are: `MailOnFailure`
            or `NoNotification`. `MailOnCompletion` is not supported.
        `process_type` : `str`, optional
            The type of refresh process to use.

        """

        resource = self.base_path + "/refreshes"
        payload = {"notifyOption": notify_option}
        params = {"processType": process_type}

        _utils.post(
            resource,
            self.session,
            payload=payload,
            params=params,
        )

    def transactions(
        self,
    ) -> list[dict]:
        """
        Returns a list of transactions for the Dataflow.

        Returns
        -------
        `list[dict]`
            List of Dataflow transactions.

        """

        resource = self.base_path + "/transactions"
        raw = _utils.get_raw(
            resource,
            self.session,
        )

        return raw

    def update(
        self,
        name: str = None,
        description: str = None,
        allow_native_queries: bool = None,
        compute_engine_behavior: str = None,
    ) -> None:
        """
        Updates Dataflow properties, capabilities, and settings.

        Parameters
        ----------
        `name` : `str`, optional
            The new name for the Dataflow.
        `description` : `str`, optional
            The new description for the Dataflow.
        `allow_native_queries` : `bool`, optional
            Whether to allow native queries.
        `compute_engine_behavior` : `str`, optional
            The behavior of the compute engine.

        Raises
        ------
        `ValueError`
            If no properties to update were provided.

        """

        update_request = {
            "name": name,
            "description": description,
            "allowNativeQueries": allow_native_queries,
            "computeEngineBehavior": compute_engine_behavior,
        }

        request_body = _utils.remove_no_values(update_request)

        if request_body in [None, {}]:
            raise ValueError(
                "No properties were provided to update. Please specify at least one property to update."
            )

        resource = self.base_path

        _utils.patch(
            resource,
            self.session,
            request_body,
        )

    def update_refresh_schedule(
        self,
        notify_option: str = None,
        days: list[str] = None,
        enabled: bool = None,
        local_time_zone_id: str = None,
        times: list[str] = None,
    ) -> None:
        """
        Creates or updates the Refresh Schedule for the Dataflow.

        Parameters
        ----------
        `notify_option` : `str`, optional
            Email notification option, e.g. "MailOnCompletion", "MailOnFailure",
            or "NoNotification".
        `days` : `list[str]`, optional
             The full name of days on which to execute the refresh,e.g, "Monday",
            "Tuesday", "Wednesday", etc.
        `enabled` : `bool`, optional
            Enable/Disable the Refresh Schedule.
        `local_time_zone_id` : `str`, optional
            The ID of the time zone to use, e.g, "UTC".
        `times` : `list[str]`, optional
            The times of day to execute the refresh expressed as hh:mm, e.g.,
            "07:00", "16:00", etc.

        Raises
        ------
        `ValueError`
            If no values are provided to update.

        """

        refresh_schedule_request = {
            "value": {
                "notifyOption": notify_option,
                "days": days,
                "enabled": enabled,
                "localTimeZoneId": local_time_zone_id,
                "times": times,
            }
        }

        request_body = _utils.remove_no_values(refresh_schedule_request)

        if request_body in [None, {}]:
            raise ValueError(
                "No options were provided to update. Please specify an option to update."
            )

        resource = self.base_path + "/refreshSchedule"

        _utils.patch(
            resource,
            self.session,
            request_body,
        )

    def upstream_dataflows(
        self,
    ) -> list[dict]:
        """
        Returns a list of upstream dataflows for the Dataflow.

        Returns
        -------
        `list[dict]`
            List of Dependent Dataflows.

        """

        resource = self.base_path + "/upstreamDataflows"
        raw = _utils.get_raw(
            resource,
            self.session,
        )

        return raw
