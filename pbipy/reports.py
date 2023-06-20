from pbipy.datasets import Dataset
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

    def pages(
        self,
    ) -> list[dict]:
        """
        Returns a list of pages within the report.

        Returns
        -------
        `list[dict]`
            List of report pages.
        """

        resource = self.base_path + "/pages"
        raw = self.get_raw(resource, self.session)

        return raw

    def rebind(
        self,
        dataset: str | Dataset,
    ) -> None:
        """
        Rebinds the report to the specified dataset.

        If the specified dataset resides in a different workspace than
        the report, then a shared dataset will be created in the report's
        workspace.

        On rebind, reports with a live connection will lose that connection
        and instead have a direct binding to the target dataset.

        Parameters
        ----------
        `dataset` : `str | Dataset`
            The new dataset for the rebound report. If the dataset resides
            in a different workspace than the report, a shared dataset will
            be created in the report's workspace.
        """

        if isinstance(dataset, Dataset):
            dataset_id = dataset.id
        else:
            dataset_id = dataset

        payload = {
            "datasetId": dataset_id,
        }
        resource = self.base_path + "/Rebind"

        self.post(resource, self.session, payload)

    def take_over(
        self,
    ) -> None:
        """
        Transfers ownership of the data sources for the report to the current
        authorized user.

        Raises
        ------
        `TypeError`
            If the Report does not have a Workspace (Group), i.e., the
            Report resides in current authorized user's Workspace.
        """

        if not self.group_id:
            raise TypeError(
                "Report does not have a group_id. Taking over a Report can only be performed on a Report in a Group."
            )

        resource = self.base_path + "/Default.TakeOver"
        self.post(resource, self.session)

    def update_datasources(
        self,
        details: dict | list[dict],
    ) -> None:
        if isinstance(details, dict):
            payload = [details]
        else:
            payload = details
        
        resource = self.base_path + "/Default.UpdateDatasources"

        self.post(resource, self.session, payload)
