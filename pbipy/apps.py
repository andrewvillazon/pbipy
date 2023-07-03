from pbipy.reports import Report
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
        raw = self.get_raw(resource, self.session)

        report = Report(
            id=raw.get("id"),
            session=self.session,
            raw=raw,
        )

        return report
