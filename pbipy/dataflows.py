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
