from pbipy.resources import Resource


from requests import Session


class Report(Resource):
    def __init__(
        self,
        id: str,
        session: Session,
        group_id: str = None,
        raw: dict = None,
    ) -> None:
        super().__init__(id, session)

        if group_id:
            self.group_id = group_id
        else:
            self.group_id = None

        if self.group_id:
            self.resource_path = f"/groups/{self.group_id}/reports/{self.id}"
        else:
            self.resource_path = f"/reports/{self.id}"

        self.base_path = f"{self.BASE_URL}{self.resource_path}"

        if raw:
            self._load_from_raw(raw)

    def datasources(
        self,
    ) -> list[dict]:
        """
        Return a list of Datasources for the report.

        Returns
        -------
        `list[dict]`
            List of Datasources for the report.
        """

        resource = self.base_path + "/datasources"
        raw = self.get_raw(resource, self.session)

        return raw

    def page(
        self,
        name: str,
    ) -> dict:
        """
        Returns the specified page from the report.

        Parameters
        ----------
        `name` : `str`
            Name of the page to return.

        Returns
        -------
        `dict`
            The specified page.
        """

        resource = self.base_path + f"/pages/{name}"
        raw = self.get_raw(resource, self.session)

        return raw
