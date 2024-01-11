"""
Module implments representations of a Power BI Dashboard and Tile.

These objects are minimal representations and not yet fully implemented.

"""

from requests import Session

from pbipy.resources import Resource


class Dashboard(Resource):
    """A Power BI Dashboard."""
    
    _REPR = [
        "id",
        "display_name",
        "group_id",
        "app_id",
    ]

    def __init__(
        self,
        id: str,
        session: Session,
        group_id=None,
        raw=None,
    ) -> None:
        super().__init__(id, session)

        if group_id:
            self.group_id = group_id
        else:
            self.group_id = None

        if self.group_id:
            self.resource_path = f"/groups/{self.group_id}/dashboards/{self.id}"
        else:
            self.resource_path = f"/dashboards/{self.id}"

        self.base_path = f"{self.BASE_URL}{self.resource_path}"

        if raw:
            self._load_from_raw(raw)


class Tile(Resource):
    """A Power BI Dashboard Tile."""

    _REPR = [
        "id",
        "title",
        "dashboard_id",
        "group_id",
        "report_id",
        "dataset_id",
    ]

    def __init__(
        self,
        id: str,
        dashboard_id: str,
        session: Session,
        group_id=None,
        raw=None,
    ) -> None:
        super().__init__(id, session)

        self.dashboard_id = dashboard_id

        if group_id:
            self.group_id = group_id
        else:
            self.group_id = None

        if self.group_id:
            self.resource_path = f"/groups/{self.group_id}/dashboards/{self.dashboard_id}/tiles/{self.id}"
        else:
            self.resource_path = f"/dashboards/{self.dashboard_id}/tiles/{self.id}"

        if raw:
            self._load_from_raw(raw)
