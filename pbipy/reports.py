from typing import TypeVar
from requests import Session

from pbipy.datasets import Dataset
from pbipy.groups import Group
from pbipy.resources import Resource
from pbipy.utils import remove_no_values


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

    def update_content(
        self,
        source_report: "str | Report",
        source_group: str | Group = None,
        source_type: str = "ExistingReport",
    ) -> None:
        """
        Updates the content of the report with the content of a specified 
        source report.
        
        If the caller provides a `Report` object as a `source_report`, then
        the `group_id` of the `source_report` is used in the update request
        and any `source_group` argument is ignored.

        Parameters
        ----------
        `source_report` : `str | Report`
            The Report Id or `Report` object that is the source of the content.
        `source_group` : `str | Group`, optional
            The Group Id or `Group` object where the `source_report` resides.
            If `source_report` is a `Report` object, this argument is ignored.
        `source_type` : `str`, optional
            Type of source. API specification indicates the only valid 
            value is "ExistingReport".
        
        """

        if isinstance(source_report, Report):
            report_id = source_report.id
        else:
            report_id = source_report
        
        # If we got report, use its group_id and ignore provided
        if isinstance(source_report, Report):
            group_id = source_report.group_id
        else:
            if isinstance(source_group, Group):
                group_id = source_group.id
            else:
                group_id = source_group

        payload = {
            "sourceReport": {
                "sourceReportId": report_id,
                "sourceWorkspaceId": group_id,
            },
            "sourceType": source_type,
        }

        prepared_payload = remove_no_values(payload)
        resource = self.base_path + "/UpdateReportContent"

        self.post(resource, self.session, prepared_payload)

    def update_datasources(
        self,
        details: dict | list[dict],
    ) -> None:
        """
        Updates the data sources of the report with supplied update details.

        Both the original data source and the new data source must have the
        exact same schema.

        Parameters
        ----------
        `details` : `dict | list[dict]`
            The update details for the data sources of the paginated report.

        Notes
        -----
        See below for the update details schema.

        https://learn.microsoft.com/en-us/rest/api/power-bi/reports/update-datasources#examples

        """

        if isinstance(details, dict):
            payload = [details]
        else:
            payload = details

        resource = self.base_path + "/Default.UpdateDatasources"

        self.post(resource, self.session, payload)
