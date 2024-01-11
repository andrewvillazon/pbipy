"""
Module implements a Power BI client that wraps around the Power BI Rest 
API.

Full API documentation can be found at:

https://learn.microsoft.com/en-us/rest/api/power-bi/

"""

import requests

from pbipy import settings
from pbipy.admin import Admin
from pbipy.apps import App
from pbipy.dashboards import Dashboard
from pbipy.dataflows import Dataflow
from pbipy.datasets import Dataset
from pbipy.groups import Group
from pbipy.reports import Report
from pbipy import _utils


class PowerBI:
    """
    User Interface into Power BI Rest Api.

    Users interact with their Power BI service by constructing an instance
    of this object and calling its methods.

    Authentication with the Power BI service requires a `bearer_token` which
    must be generated in advance of initializing the `PowerBI` client. How 
    the token is generated depends on the user's Azure and Power BI configuration.

    In general, `PowerBI()` methods wrap the operations described here:

    https://learn.microsoft.com/en-us/rest/api/power-bi/

    Parameters
    ----------
    `bearer_token` : `str`
        Bearer token used to authenticate with your Power BI service.
    `session` : `requests.Session`, optional
        `Session` object used to make http requests. Users can subclass
        a `Session` and pass to the constructor of the client to implement 
        customized request handling, e.g., implementing a retry strategy.
    
    Examples
    --------
    Initializing the client.

    ```
    >>> from powerbi import PowerBI
    >>> pbi = PowerBI(bearer_token="aBCdEFGhijK123456xYz")
    ```

    Using the client to retrieve a report and then initiate a refresh.

    ```
    >>> my_report = pbi.report("5b218778-e7a5-4d73-8187-f10824047715")
    >>> my_report.refresh()
    ```

    Using the client to create a new Workspace (Group) in the user's Power 
    BI instance.

    ```
    >>> my_workspace = pbi.create_group("Workspace Name")
    ```

    """

    BASE_URL = settings.BASE_URL

    def __init__(
        self,
        bearer_token: str,
        session: requests.Session = None,
    ) -> None:
        self.bearer_token = bearer_token

        if not session:
            self.session = requests.Session()

        self.session.headers.update({"Authorization": f"Bearer {self.bearer_token}"})

    def admin(
        self,
    ) -> Admin:
        """
        Initialize and return an `Admin` object. The `Admin` object is used
        to access admin-only functionality.

        Returns
        -------
        `Admin`
            The initialized `Admin` object.

        """

        return Admin(self.session)

    def app(
        self,
        app: str,
    ) -> App:
        """
        Return the specified installed app.

        Parameters
        ----------
        `app` : `str`
            App id of the App to retrieve.

        Returns
        -------
        `App`
            The specified App.

        """

        if isinstance(app, App):
            return app

        app = App(app, self.session)
        app.load()

        return app

    def apps(
        self,
    ) -> list[App]:
        resource = self.BASE_URL + "/apps"
        raw = _utils.get_raw(
            resource,
            self.session,
        )

        apps = [
            App(
                app_js.get("id"),
                self.session,
                raw=app_js,
            )
            for app_js in raw
        ]

        return apps

    def cancel_transaction(
        self,
        transaction_id: str,
        group: str | Group,
    ) -> dict:
        """
        Attempt to cancel the specified Dataflow Transaction.

        Parameters
        ----------
        `transaction_id` : `str`
            Id of the Transaction to cancel.
        `group` : `str | Group`
            Group Id or `Group` object where the Transaction originated.
            Should match the Group of the Dataflow that generated the
            transaction.

        Returns
        -------
        `dict`
            Dataflow transaction status.

        """

        if isinstance(group, Group):
            group_id = group.id
        else:
            group_id = group

        resource = (
            self.BASE_URL
            + f"/groups/{group_id}/dataflows/transactions/{transaction_id}/cancel"
        )
        raw = _utils.post_raw(
            resource,
            self.session,
        )

        return raw

    def add_dashboard(
        self,
        name: str,
        group: str | Group = None,
    ) -> Dashboard:
        """
        Creates a new empty dashboard in current users workspace or the
        specified Workspace.

        Parameters
        ----------
        `name` : `str`
            The name of the new dashboard.
        `group` : `str | Group`, optional
            The Group Id or `Group` object to target.

        Returns
        -------
        `Dashboard`
            The newly created `Dashboard`.

        """

        if isinstance(group, Group):
            group_id = group.id
        else:
            group_id = group

        if group:
            path = _utils.build_path("/groups/{}/dashboards", group)
        else:
            path = "/dashboards"

        url = self.BASE_URL + path
        payload = {"name": name}
        raw = _utils.post_raw(
            url,
            self.session,
            payload=payload,
        )

        dashboard = Dashboard(
            raw.get("id"),
            self.session,
            group_id=group_id,
            raw=raw,
        )

        return dashboard

    def dashboard(
        self,
        dashboard: str | Dashboard,
        group: str | Group = None,
    ) -> Dashboard:
        """
        Returns the specified dashboard from the current user's Workspace
        or the specified Workspace.

        Parameters
        ----------
        `dashboard` : `str | Dashboard`
            The id of the Dashboard to retrieve.
        `group` : `str | Group`, optional
            The Group Id or `Group` object to target.

        Returns
        -------
        `Dashboard`
            The specified Dashboard.

        """

        if isinstance(dashboard, Dashboard):
            return dashboard

        if isinstance(group, Group):
            group_id = group.id
        else:
            group_id = group

        if group:
            path = _utils.build_path("/groups/{}/dashboards/{}", group, dashboard)
        else:
            path = _utils.build_path("/dashboards/{}", dashboard)

        url = self.BASE_URL + path
        raw = _utils.get_raw(
            url,
            self.session,
        )

        dashboard = Dashboard(
            raw.get("id"),
            self.session,
            group_id=group_id,
            raw=raw,
        )

        return dashboard

    def dataflow(
        self,
        dataflow: str | Dataflow,
        group: str | Group,
    ) -> Dataflow:
        """
        Get and load the specified dataflow.

        Parameters
        ----------
        `dataflow` : `str | Dataflow`
            The Dataflow Id of the Dataflow to retrieve.
        `group` : `str | Group`
            The Group Id or `Group` object where the Dataflow resides.

        Returns
        -------
        `Dataflow`
            The specified Dataflow.

        Notes
        -----
        The Get Dataflow endpoint returns a json file. For consistency
        with the rest of pbipy, this method returns a `Dataflow` object instead
        of the file itself. To access the json file, use the `Dataflow.raw`
        property.

        """

        if isinstance(dataflow, Dataflow):
            return Dataflow

        if isinstance(group, Group):
            group_id = group.id
        else:
            group_id = group

        resource = self.BASE_URL + f"/groups/{group_id}/dataflows/{dataflow}"
        raw = _utils.get_raw(
            resource,
            self.session,
        )

        dataflow = Dataflow(
            raw.get("objectId"),
            self.session,
            group_id=group_id,
            raw=raw,
        )

        return dataflow

    def dataflows(
        self,
        group: str | Group,
    ) -> list[Dataflow]:
        """
        Returns a list of all dataflows from the specified Workspace.

        Parameters
        ----------
        `group` : `str | Group`
            Group Id or `Group` object where the Dataflow resides.

        Returns
        -------
        `list[Dataflow]`
            List of `Dataflow` objects from the specified Workspace.

        """

        if isinstance(group, Group):
            group_id = group.id
        else:
            group_id = group

        resource = self.BASE_URL + f"/groups/{group_id}/dataflows"
        raw = _utils.get_raw(
            resource,
            self.session,
        )

        dataflows = [
            Dataflow(
                dataflow_js.get("objectId"),
                self.session,
                group_id=group_id,
                raw=dataflow_js,
            )
            for dataflow_js in raw
        ]

        return dataflows

    def delete_dataflow(
        self,
        dataflow: str | Dataflow,
        group: str | Group,
    ) -> None:
        """
        Deletes a dataflow from Power BI data prep storage, including its
        definition file and model.

        Parameters
        ----------
        `dataflow` : `str | Dataflow`
            Dataflow Id or `Dataflow` object to delete.
        `group` : `str | Group`
            Group Id or `Group` object where the Dataflow resides.

        """

        if isinstance(dataflow, Dataflow):
            dataflow_id = dataflow.id
        else:
            dataflow_id = dataflow

        if isinstance(group, Group):
            group_id = group.id
        else:
            group_id = group

        resource = self.BASE_URL + f"/groups/{group_id}/dataflows/{dataflow_id}"

        _utils.delete(
            resource,
            self.session,
        )

    # TODO: Add support for passing in a group obj
    def dataset(
        self,
        dataset: str | Dataset,
        group: str = None,
    ) -> Dataset:
        """
        Return the specified dataset from MyWorkspace or the specified
        group.

        Parameters
        ----------
        `dataset` : `str | Dataset`
            Dataset Id of the dataset to retrieve.
        `group` : `str`, optional
            Group Id where the dataset resides., by default None

        Returns
        -------
        `Dataset`
            The specified dataset.

        """

        if isinstance(dataset, Dataset):
            return dataset

        dataset = Dataset(dataset, self.session, group_id=group)
        dataset.load()

        return dataset

    def datasets(
        self,
        group: str = None,
    ) -> list[Dataset]:
        """
        Returns a list of datasets from MyWorkspace or the specified group.

        Parameters
        ----------
        `group` : str, optional
            Group Id where the datasets reside. If not supplied, then datasets
            will be retrieved from MyWorkspace.

        Returns
        -------
        `list[Dataset]`
            List of datasets for MyWorkspace or the specified group.

        """

        if group:
            path = f"/groups/{group}/datasets"
        else:
            path = "/datasets"

        resource = self.BASE_URL + path
        raw = _utils.get_raw(
            resource,
            self.session,
        )

        datasets = [
            Dataset(
                dataset_js.get("id"),
                self.session,
                group_id=group,
                raw=dataset_js,
            )
            for dataset_js in raw
        ]

        return datasets

    def delete_dataset(
        self,
        dataset: str | Dataset,
        group: str = None,
    ) -> None:
        """
        Delete the specified dataset from MyWorkspace or the specified
        group.

        Parameters
        ----------
        `dataset` : `str | Dataset`
            Dataset Id or `Dataset` object to delete.
        `group` : `str`, optional
            Group Id where the dataset resides., by default None

        Raises
        ------
        `HTTPError`
            If the api response status code is not equal to 200.

        """
        # FIXME: Doesn't use the group from the Dataset.

        if isinstance(dataset, Dataset):
            dataset_id = dataset.id
        else:
            dataset_id = dataset

        if group:
            path = f"/groups/{group}/datasets/{dataset_id}"
        else:
            path = f"/datasets/{dataset_id}"

        resource = self.BASE_URL + path

        _utils.delete(
            resource,
            self.session,
        )

    def group(
        self,
        group_id: str,
    ) -> Group:
        """
        Return the specified group.

        Convenience function that is the equivalent of
        `group(filter="id eq 'group_id'")`.

        Parameters
        ----------
        `group_id` : `str`
            Group Id of the group to retrieve.

        Returns
        -------
        `Group`
            The specified group.

        Raises
        ------
        `ValueError`
            If the Group was not found by the api.

        """

        id_filter = f"id eq '{group_id}'"

        groups = self.groups(filter=id_filter)

        if groups == []:
            raise ValueError(f"Group Id: {id_filter}, was not found by the API.")

        return groups[0]

    def groups(
        self,
        filter: str = None,
        skip: int = None,
        top: int = None,
    ) -> list[Group]:
        """
        Returns a list of workspaces the user has access to.

        Parameters
        ----------
        `filter` : `str`, optional
            Filters the results, based on a boolean condition, e.g.,
            `contains(name, 'marketing')`, `name eq 'contoso'`
        `skip` : `int`, optional
            Skips the first n results.
        `top` : `int`, optional
            Returns only the first n results.

        Returns
        -------
        `list[Group]`
            List of `Group` objects the user has access to, and/or
            that matched the specified filters.

        Notes
        -----
        See below for more details on filter syntax:
        https://learn.microsoft.com/en-us/power-bi/collaborate-share/service-url-filters

        """

        params = {
            "$filter": filter,
            "$skip": skip,
            "$top": top,
        }

        preparred_params = _utils.remove_no_values(params)

        path = self.BASE_URL + "/groups"
        raw = _utils.get_raw(
            path,
            self.session,
            params=preparred_params,
        )

        groups = [
            Group(
                group_js.get("id"),
                self.session,
                raw=group_js,
            )
            for group_js in raw
        ]

        return groups

    def create_group(
        self,
        name: str,
        workspace_v2: bool = None,
    ) -> Group:
        """
        Create a new workspace.

        Parameters
        ----------
        `name` : `str`
            The name for the new workspace.
        `workspace_v2` : `bool`, optional
            (Preview feature) Whether to create a workspace. The only supported value is `true`.

        Returns
        -------
        `Group`
            The newly created workspace (group).

        """

        payload = {"name": name}

        if workspace_v2 is not None:
            resource = self.BASE_URL + f"/groups?workspaceV2={workspace_v2}"
        else:
            resource = self.BASE_URL + "/groups"

        raw = _utils.post_raw(
            resource,
            self.session,
            payload,
        )

        return Group(
            raw.get("id"),
            self.session,
            raw=raw,
        )

    def delete_group(
        self,
        group: str | Group,
    ) -> None:
        """
        Delete the specified workgroup.

        Parameters
        ----------
        `group` : `str | Group`
            Group Id or `Group` object to delete.

        """

        if isinstance(group, Group):
            group_id = group.id
        else:
            group_id = group

        resource = self.BASE_URL + f"/groups/{group_id}"

        _utils.delete(
            resource,
            self.session,
        )

    def report(
        self,
        report: str | Report,
        group: str | Group = None,
    ) -> Report:
        """
        Return the specified report from MyWorkspace or the specified group.

        Parameters
        ----------
        report : `str | Report`
            Report Id to retrieve.
        group : `str | Group`, optional
            Group Id or `Group` object where the report resides.

        Returns
        -------
        `Report`
            The specified `Report` object.

        """

        if isinstance(report, Report):
            return report

        if isinstance(group, Group):
            group_id = group.id
        else:
            group_id = group

        report = Report(report, self.session, group_id=group_id)
        report.load()

        return report

    def reports(
        self,
        group: str | Group = None,
    ) -> list[dict]:
        """
        Return a list of reports for MyWorkspace or the specified
        group (workspace).

        Parameters
        ----------
        `group` : `str | Group`, optional
            Group Id or `Group` object where the reports reside., by default None

        Returns
        -------
        `list[dict]`
            List of `Report` objects for MyWorkspace or the specified
            group (workspace).

        """

        if isinstance(group, Group):
            group_id = group.id
        else:
            group_id = group

        if group_id:
            path = f"/groups/{group_id}/reports"
        else:
            path = "/reports"

        resource = self.BASE_URL + path
        raw = _utils.get_raw(
            resource,
            self.session,
        )

        reports = [
            Report(
                report_js.get("id"),
                self.session,
                group_id=group_id,
                raw=report_js,
            )
            for report_js in raw
        ]

        return reports

    def delete_report(
        self,
        report: str | Report,
        group: str | Group = None,
    ) -> None:
        """
        Delete the specified report.

        If a `Report` type is provided as `report`, then it's `group_id`
        will be taken as the `group` value.

        Parameters
        ----------
        `report` : `str | Report`
            Report Id or `Report` object to delete.
        `group` : `str | Group`, optional
            The Group Id or `Group` object where the report resides. If
            a `Report` object is provided then the `group_id` of that report
            will override the provided group value.

            If no group value is provided, it is assumed the report resides
            in the current user's workspace.

        """

        if isinstance(report, Report):
            report_id = report.id
        else:
            report_id = report

        # If we got report, use its group_id and ignore provided
        if isinstance(report, Report):
            group_id = report.group_id
        else:
            if isinstance(group, Group):
                group_id = group.id
            else:
                group_id = group

        if group_id:
            resource = self.BASE_URL + f"/groups/{group_id}/reports/{report_id}"
        else:
            resource = self.BASE_URL + f"/reports/{report_id}"

        _utils.delete(
            resource,
            self.session,
        )
