import requests

from pbipy import settings
from pbipy.apps import App
from pbipy.dashboards import Dashboard
from pbipy.dataflows import Dataflow
from pbipy.datasets import Dataset
from pbipy.groups import Group
from pbipy.utils import RequestsMixin


class Admin(RequestsMixin):
    BASE_URL = settings.BASE_URL

    def __init__(
        self,
        session: requests.Session,
    ) -> None:
        self.session = session

        self.resource_path = "/admin"
        self.base_path = f"{self.BASE_URL}{self.resource_path}"

    def apps(
        self,
        top: int = None,
    ) -> list[App]:
        """
        Return a list of Apps in the Organization.

        Parameters
        ----------
        top : `int`, optional
            The requested number of entries in the refresh history. If not
            provided, the default is all available entries.

        Returns
        -------
        `list[App]`
            The list of Apps for the organization.

        """

        resource = self.base_path + "/apps"
        params = {"$top": top}

        raw = self.get_raw(resource, self.session, params)

        apps = [
            App(
                app_js.get("id"),
                self.session,
                raw=app_js,
            )
            for app_js in raw
        ]

        return apps

    def app_users(
        self,
        app: str | App,
    ) -> list[dict]:
        if isinstance(app, App):
            app_id = app.id
        else:
            app_id = app

        resource = self.base_path + f"/apps/{app_id}/users"
        raw = self.get_raw(resource, self.session)

        return raw

    def dashboards(
        self,
        group: str | Group = None,
        expand: str = None,
        filter: str = None,
        skip: int = None,
        top: int = None,
    ) -> list[Dashboard]:
        """
        Returns a list of dashboards for the organization or specified Workspace.

        Parameters
        ----------
        `group` : `str | Group`, optional
            Group Id or `Group` object where the Apps reside. If not supplied
            then returns all apps for the organization.
        `expand` : `str`, optional
            Accepts a comma-separated list of data types, which will be
            expanded inline in the response. Supports tiles.
        `filter` : `str`, optional
            Filters the results, based on a boolean condition.
        `skip` : `int`, optional
            Skips the first n results.
        `top` : `int`, optional
            Returns only the first n results.

        Returns
        -------
        `list[Dashboard]`
            List of `Dashboard` objects for the organization.

        """
        if group:
            if isinstance(group, Group):
                group_id = group.id
            else:
                group_id = group

            path = f"/groups/{group_id}/dashboards"
        else:
            path = "/dashboards"

        resource = self.base_path + path

        params = {
            "$expand": expand,
            "$filter": filter,
            "$skip": skip,
            "$top": top,
        }

        raw = self.get_raw(resource, self.session, params=params)

        dashboards = [
            Dashboard(
                dashboard_js.get("id"),
                self.session,
                raw=dashboard_js,
            )
            for dashboard_js in raw
        ]

        return dashboards

    def dataflow(
        self,
        dataflow: str | Dataflow,
    ) -> Dataflow:
        """
        Get and load the specified Dataflow.

        Parameters
        ----------
        `dataflow` : `str | Dataflow`
            The Dataflow Id of the Dataflow to retrieve.

        Returns
        -------
        `Dataflow`
            The specified Dataflow.

        Notes
        -----
        The ExportDataflowAsAdmin endpoint returns a json file. For consistency
        with the rest of pbipy, this method returns a `Dataflow` object instead
        of the file itself. To access the json file, use the `Dataflow.raw`
        property.

        """
        if isinstance(dataflow, Dataflow):
            return Dataflow

        resource = self.base_path + f"/dataflows/{dataflow}/export"
        raw = self.get_raw(resource, self.session)

        dataflow = Dataflow(
            raw.get("objectId"),
            self.session,
            group_id=None,
            raw=raw,
        )

        return dataflow

    def dataflow_datasources(
        self,
        dataflow: str | Dataflow,
    ) -> list[dict]:
        """
        Return a list of Datasources for the specified Dataflow.

        Returns
        -------
        `list[dict]`
            The list of Datasources associated with the Dataflow.

        """

        if isinstance(dataflow, Dataflow):
            dataflow_id = dataflow.id
        else:
            dataflow_id = dataflow

        resource = self.base_path + f"/dataflows/{dataflow_id}/datasources"
        raw = self.get_raw(resource, self.session)

        return raw

    def dataflow_upstream_dataflows(
        self,
        dataflow: str | Dataflow,
        group: str | Group,
    ) -> list[dict]:
        """
        Returns a list of upstream dataflows for the specified Dataflow.

        Parameters
        ----------
        `dataflow` : `str | Dataflow`
            The Dataflow Id or `Dataflow` object to target.
        `group` : `str | Group`
            The Group Id or `Group` object where the target Dataflow resides.

        Returns
        -------
        `list[dict]`
            List of upstream dataflows.

        """

        if isinstance(dataflow, Dataflow):
            dataflow_id = dataflow.id
        else:
            dataflow_id = dataflow

        if isinstance(group, Group):
            group_id = group.id
        else:
            group_id = group

        resource = (
            self.base_path
            + f"/groups/{group_id}/dataflows/{dataflow_id}/upstreamDataflows"
        )
        raw = self.get_raw(resource, self.session)

        return raw

    def dataflow_users(
        self,
        dataflow: str | Dataflow,
    ) -> list[dict]:
        """
        Returns a list of users that have access to the specified Dataflow.

        Parameters
        ----------
        `dataflow` : `str | Dataflow`
            The Dataflow Id or `Dataflow` object to retrieve the users for.

        Returns
        -------
        `list[dict]`
            List of users with access to the Dataflow.

        """

        if isinstance(dataflow, Dataflow):
            dataflow_id = dataflow.id
        else:
            dataflow_id = dataflow

        resource = self.base_path + f"/dataflows/{dataflow_id}/users"
        raw = self.get_raw(resource, self.session)

        return raw

    def datasets(
        self,
        group: str | Group = None,
        expand: str = None,
        filter: str = None,
        skip: int = None,
        top: int = None,
    ) -> list[Dataset]:
        """
        Returns a list of datasets for the Organization or specified Workspace 
        (Group).

        Parameters
        ----------
        `group` : `str | Group`, optional
            Group Id or `Group` object to target. If provided then this
            method will return Datasets for the specified Group and not the
            Organization.
        `expand` : `str`, optional
            Expands related entities inline. If no `group` argument was 
            provided, then this argument is ignored.
        `filter` : `str`, optional
            Filters the results, based on a boolean condition.
        `skip` : `int`, optional
            Skips the first n results.
        `top` : `int`, optional
            Returns only the first n results.

        Returns
        -------
        `list[Dataset]`
            List of Datasets for the Organization or specified Workspace.
        
        """

        params = {
            "$expand": expand,
            "$filter": filter,
            "$skip": skip,
            "$top": top,
        }

        # The non-group endpoint doesn't support $expand
        if group is None:
            params.pop("$expand")

        # Avoid referencing error in dataset_js.get("workspaceId", group_id)
        group_id = None

        if group:
            if isinstance(group, Group):
                group_id = group.id
            else:
                group_id = group

            path = f"/groups/{group_id}/datasets"
        else:
            path = "/datasets"

        resource = self.base_path + path
        raw = self.get_raw(resource, self.session, params=params)

        datasets = [
            Dataset(
                id=dataset_js.get("id"),
                session=self.session,
                group_id=dataset_js.get("workspaceId", group_id),
                raw=dataset_js,
            )
            for dataset_js in raw
        ]

        return datasets

    def dataset_users(
        self,
        dataset: str | Dataset,
    ) -> list[dict]:
        """
        Return a list of users that have access to the specified Dataset.

        Parameters
        ----------
        dataset : `str | Dataset`
            Dataset Id or `Dataset` object to target.

        Returns
        -------
        `list[dict]`
            List of Users with access to the specified Dataset.

        """

        if isinstance(dataset, Dataset):
            dataset_id = dataset.id
        else:
            dataset_id = dataset

        resource = self.base_path + f"/datasets/{dataset_id}/users"
        raw = self.get_raw(resource, self.session)

        return raw

    def datasets_upstream_dataflows(
        self,
        group: str | Group,
    ) -> list[dict]:
        """
        Return a list of upstream dataflows for datasets from the specified
        Workspace (Group).

        Parameters
        ----------
        `group` : `str | Group`
            Group Id or `Group` object to target.

        Returns
        -------
        `list[dict]`
            List of Dataset to Dataflow Links for the specified Workspace.
            Each element in this list represents a link between a Dataset
            and Dataflow.

        """

        if isinstance(group, Group):
            group_id = group.id
        else:
            group_id = group

        resource = self.base_path + f"/groups/{group_id}/datasets/upstreamDataflows"
        raw = self.get_raw(resource, self.session)

        return raw
