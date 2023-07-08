from requests import Session
from pbipy.resources import Resource
from pbipy.utils import remove_no_values


class Dataflow(Resource):
    _REPR = [
        "id",
        "name",
        "description",
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
        raw = self.get_raw(resource, self.session)

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

        self.post(resource, self.session, payload=payload, params=params)

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
        raw = self.get_raw(resource, self.session)

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

        request_body = remove_no_values(update_request)

        if request_body in [None, {}]:
            raise ValueError(
                "No properties were provided to update. Please specify at least one property to update."
            )

        resource = self.base_path

        self.patch(resource, self.session, request_body)

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
        raw = self.get_raw(resource, self.session)

        return raw
