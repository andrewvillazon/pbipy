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
