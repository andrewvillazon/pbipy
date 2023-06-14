from pbipy.utils import to_snake_case
from pbipy import settings


class Resource:
    BASE_URL = settings.BASE_URL

    def __init__(self, path, session, **kwargs) -> None:
        self.path = path
        self.url = self.BASE_URL + self.path
        self.session = session
        self.raw = None

        if "group_id" in kwargs:
            # If None, is not part of workspace, set to "me"
            # as per pbi urls: /groups/me/etc.
            if kwargs.get("group_id") is None:
                group_id = "me"
            else:
                group_id = kwargs.get("group_id")

            setattr(self, "group_id", group_id)

    def _load_from_raw(self, raw):
        self.raw = raw

        for k, v in raw.items():
            attr = to_snake_case(k)
            setattr(self, attr, v)

        return self

    def load(self):
        response = self.session.get(self.url)
        raw = response.json()

        self._load_from_raw(raw)


class Dataset(Resource):
    def __init__(
        self,
        id,
        session=None,
        group_id=None,
        raw=None,
    ) -> None:
        if group_id:
            path = f"groups/{group_id}/datasets/{id}"
        else:
            path = f"datasets/{id}"

        super().__init__(path, session, group_id=group_id)

        if raw:
            self._load_from_raw(raw)
