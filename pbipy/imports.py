from types import SimpleNamespace

from requests import Session

from pbipy.groups import Group
from pbipy.resources import Resource


class Import(Resource):
    """
    A file that has been uploaded into Power BI.

    """

    _REPR = [
        "id",
        "name",
        "group_id",
        "created_date_time",
        "updated_date_time",
        "import_state",
        "connection_type",
        "source",
    ]

    def __init__(
        self,
        id: str,
        session: Session,
        group_id: str | Group = None,
        raw: dict = None,
    ) -> None:
        super().__init__(id, session)

        if group_id:
            self.group_id = group_id
        else:
            self.group_id = None

        if self.group_id:
            self.resource_path = f"/groups/{self.group_id}/imports/{self.id}"
        else:
            self.resource_path = f"/imports/{self.id}"

        self.base_path = f"{self.BASE_URL}{self.resource_path}"

        if raw:
            self._load_from_raw(raw)


class TemporaryUploadLocation(SimpleNamespace):
    """
    Temporary blob storage location for importing large Power BI `.pbix`
    files.

    Parameters
    ----------
    `expiration_time` : `str`
        The expiration date and time of the shared access signature URL.
    `url` : `str`
        The shared access signature URL for the temporary blob storage.

    """

    def __init__(
        self,
        expiration_time: str,
        url: str,
    ) -> None:
        self.expiration_time = expiration_time
        self.url = url
