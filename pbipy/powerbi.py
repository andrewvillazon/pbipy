"""
Module implements a wrapper around the Power BI Rest API.

Users construct an instance of the PowerBI client and call its methods.

Full API documentation can be found at:

https://learn.microsoft.com/en-us/rest/api/power-bi/
"""

import requests
from requests.exceptions import HTTPError

from pbipy import settings
from pbipy.groups import Group
from pbipy.datasets import Dataset
from pbipy.resources import Report
from pbipy.utils import RequestsMixin, remove_no_values


class PowerBI(RequestsMixin):
    """
    User Interface into Power BI Rest Api.

    Users interact with their Power BI service by constructing an instance
    of this object and calling its methods.

    Authentication with the Power BI service requires a `bearer_token` which
    must be generated in advance before creating the `PowerBI` object.
    How you the token is generated depends on the user's Azure and Power
    BI configuration.

    In general, `PowerBI()` methods (mostly) follow the operations described
    here:

    https://learn.microsoft.com/en-us/rest/api/power-bi/

    Parameters
    ----------
    `bearer_token` : `str`
        Bearer token used to authenticate with your Power BI service.
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
        raw = self.get_raw(resource, self.session)

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

        if isinstance(dataset, Dataset):
            dataset_id = dataset.id
        else:
            dataset_id = dataset

        if group:
            path = f"/groups/{group}/datasets/{dataset_id}"
        else:
            path = f"/datasets/{dataset_id}"

        resource = self.BASE_URL + path

        self.delete(resource, self.session)

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
        """

        params = {
            "$filter": filter,
            "$skip": skip,
            "$top": top,
        }

        preparred_params = remove_no_values(params)

        path = self.BASE_URL + "/groups"
        raw = self.get_raw(path, self.session, params=preparred_params)

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

        raw = self.post_raw(resource, self.session, payload)
        # Endpoint returns as list with one element.
        group_raw = raw[0]

        return Group(group_raw.get("id"), self.session, raw=group_raw)

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

        self.delete(resource, self.session)

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
