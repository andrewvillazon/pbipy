from pbipy.resources import Resource

from requests import Session


class App(Resource):
    _REPR = [
        "id",
        "name",
        "description",
    ]

    def __init__(
        self,
        id: str,
        session: Session,
        raw=None,
    ) -> None:
        super().__init__(id, session)

        self.resource_path = f"/apps/{self.id}"
        self.base_path = f"{self.BASE_URL}{self.resource_path}"

        if raw:
            self._load_from_raw(raw)
