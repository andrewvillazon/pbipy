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
