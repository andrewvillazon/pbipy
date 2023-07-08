from requests import Session
from pbipy.resources import Resource


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
        payload={"notifyOption": notify_option}
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
