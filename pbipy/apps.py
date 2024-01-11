"""
Module implements a wrapper around the Power BI Rest API App operations.

Full App Operations documentation can be found at:

https://learn.microsoft.com/en-us/rest/api/power-bi/apps

"""

from requests import Session

from pbipy.dashboards import Dashboard, Tile
from pbipy.reports import Report
from pbipy.resources import Resource
from pbipy import _utils


class App(Resource):
    """
    A Power BI installed App.
    
    Users should initialize an `App` object by calling the `app()` method
    on the `PowerBI` client, rather than creating directly.

    Examples
    --------
    Retrieving an `App` object using a `pbi` client object.
    
    ```
    >>> my_app = pbi.app("f089354e-8366-4e18-aea3-4cb4a3a50b48")
    ```

    """

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

    def dashboard(
        self,
        dashboard: str,
    ) -> Dashboard:
        """
        Return the specified Dashboard from the App.

        Parameters
        ----------
        dashboard : `str`
            Dashboard Id of the Dashboard to retrieve.

        Returns
        -------
        `Dashboard`
            The specified Dashboard.

        """

        resource = self.base_path + f"/dashboards/{dashboard}"
        raw = _utils.get_raw(
            resource,
            self.session,
        )

        dashboard = Dashboard(
            id=raw.get("id"),
            session=self.session,
            raw=raw,
        )

        return dashboard

    def dashboards(
        self,
    ) -> list[Dashboard]:
        """
        Returns a list of Dashboards from the App.

        Returns
        -------
        `list[Dashboard]`
            List of Dashboards associated with the App.

        """

        resource = self.base_path + "/dashboards"
        raw = _utils.get_raw(
            resource,
            self.session,
        )

        dashboards = [
            Dashboard(
                id=dashboard_js.get("id"),
                session=self.session,
                raw=dashboard_js,
            )
            for dashboard_js in raw
        ]

        return dashboards

    def report(
        self,
        report: str,
    ) -> Report:
        """
        Return the specified report from the specified app.

        Parameters
        ----------
        `report` : `str`
            The Report Id

        Returns
        -------
        `Report`
            A Power BI report. The API returns a subset of the following
            list of report properties. The subset depends on the API called,
            caller permissions, and the availability of data in the Power
            BI database.

        """

        resource = self.base_path + f"/reports/{report}"
        raw = _utils.get_raw(
            resource,
            self.session,
        )

        report = Report(
            id=raw.get("id"),
            session=self.session,
            raw=raw,
        )

        return report

    def reports(
        self,
    ) -> list[Report]:
        """
        Returns a list of reports from the app.

        Returns
        -------
        `list[Report]`
            The collection of reports from the app.

        """

        resource = self.base_path + "/reports"
        raw = _utils.get_raw(
            resource,
            self.session,
        )

        reports = [
            Report(
                report_js.get("id"),
                self.session,
                raw=report_js,
            )
            for report_js in raw
        ]

        return reports

    def tile(
        self,
        tile: str,
        dashboard: str,
    ) -> Tile:
        """
        Return the specified tile from the specified dashboard for the App.

        Parameters
        ----------
        `tile` : `str`
            Tile Id of the tile to retrieve.
        `dashboard` : `str`
            Dashboard Id of the dashboard to retrieve.

        Returns
        -------
        `Tile`
            The specified tile.

        """

        resource = self.base_path + f"/dashboards/{dashboard}/tiles/{tile}"
        raw = _utils.get_raw(
            resource,
            self.session,
        )

        tile = Tile(
            tile,
            dashboard,
            session=self.session,
            raw=raw,
        )

        return tile

    def tiles(
        self,
        dashboard: str,
    ) -> list[Tile]:
        """
        Returns a list of `Tile` objects within the specified dashboard
        from the App.

        Parameters
        ----------
        `dashboard` : `str`
            Dashboard Id of the Dashboard that includes the tiles.

        Returns
        -------
        `list[Tile]`
            List of `Tile` objects from the specified dashboard and App.

        """

        resource = self.base_path + f"/dashboards/{dashboard}/tiles"
        raw = _utils.get_raw(
            resource,
            self.session,
        )

        tiles = [
            Tile(
                tile_js.get("id"),
                dashboard_id=dashboard,
                session=self.session,
                raw=tile_js,
            )
            for tile_js in raw
        ]

        return tiles
