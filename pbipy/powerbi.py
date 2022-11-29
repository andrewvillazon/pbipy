"""
Module implements a wrapper around the Power BI Rest API.

Users construct an instance of the PowerBI client and call its methods. These 
methods closely follow the naiming laid out here:

https://learn.microsoft.com/en-us/rest/api/power-bi/
"""

import requests

from .models import Group, Dataset, Refresh, DatasetToDataflowLink, DatasetUserAccess


class PowerBI:
    """
    User Interface into Power BI Rest Api.

    Users interact with their Power BI service by constructing an instance of this
    object and calling its methods.

    Authentication with the Power BI service requires a `bearer_token` which must be
    generated in advance before creating the `PowerBI` object. How you generate the token
    will depend on your Azure and Power BI configuration.

    In general, `PowerBI()` methods follow the naming laid out here:

    https://learn.microsoft.com/en-us/rest/api/power-bi/

    Parameters
    ----------
    `bearer_token` : `str`
        Bearer token used to authenticate with your Power BI service.
    """

    def __init__(self, bearer_token, session=None):
        self.bearer_token = bearer_token

        if not session:
            self.session = requests.Session()

        self.session.headers.update({"Authorization": f"Bearer {self.bearer_token}"})

    def _get_resource(self, url_format, *id, parameters={}):
        """
        Fetch a resource from the Power BI Rest API.

        Takes a templated url, id(s) used in the resource, and optional
        parameters. Constructs the url to the resource and requests the
        resource from the Power BI Rest API. Returns the associated response.

        If the response contains a list of Power BI objects, this will be
        parsed and the list of objects returned.

        Parameters
        ----------
        `url_format` : `str`
            The url of the resource. May also include placeholders,
            e.g., `datasets/{datasetId}/refreshes`.
        `*id` : `tuple`
            Id values to include in the url. Any placeholders in
            `url_format` will be replaced with these values in the
            order they are passed in.
        `**parameters`: `dict`
            Keyword argument of optional url parameters, e.g.,
            `$top` to limit number of results returned.


        Returns
        -------
        `json`
            The json response as returned from the api call. Where the api response contains
            a list of objects, e.g., a list of Datasets, the response will be parsed to only
            return this list.
        """

        if id:
            if isinstance(id, tuple):
                url = url_format.format(*id)
            else:
                url = url_format.format(id)
        else:
            url = url_format

        resp = self.session.get(url, params=parameters)
        raw = resp.json()

        # NOTE: Will we need this in future?
        if "@odata.context" in raw:
            del raw["@odata.context"]

        if "value" in raw:
            if isinstance(raw["value"], list):
                raw = raw["value"]

        return raw

    def get_groups(self, filter=None, top=None, skip=None):
        """
        Return a list of workspaces the user has access to.

        Parameters
        ----------
        `filter` : `str`
            Filters the results, based on a boolean condition, by default None
        `top` : `int`
            Returns only the first n results, by default None
        `skip` : `int`
            Skip the first n results, by default None

        Returns
        -------
        `list`
            List of `Group` objects.
        """

        resource = "https://api.powerbi.com/v1.0/myorg/groups"
        params = {
            "$filter": filter,
            "$top": top,
            "$skip": skip,
        }
        raw = self._get_resource(resource, parameters=params)

        return [Group.from_raw(raw=group) for group in raw]

    def get_datasets_in_group(self, group):
        if isinstance(group, Group):
            id = group.id
        else:
            id = group

        resource = "https://api.powerbi.com/v1.0/myorg/groups/{0}/datasets"
        raw = self._get_resource(resource, id)

        return [Dataset.from_raw(raw=dataset) for dataset in raw]

    def get_dataset_in_group(self, group, dataset):
        """
        Return the specified dataset from the specified group.

        Parameters
        ----------
        `group` : `str`
            The Group Id or Group Object where the Dataset resides.
        `dataset` : `str`
            The Dataset Id of the Dataset to retrieve.

        Returns
        -------
        `Dataset`
            The specified Dataset.
        """

        if isinstance(group, Group):
            group_id = group.id
        else:
            group_id = group

        resource = "https://api.powerbi.com/v1.0/myorg/groups/{0}/datasets/{1}"
        raw = self._get_resource(resource, group_id, dataset)

        return Dataset.from_raw(raw=raw)

    def get_refresh_history(self, dataset, top=None):
        """
        Returns the refresh history for the specified dataset.

        Parameters
        ----------
        `dataset` : `str`
            The Dataset Id or Dataset Object to get the refresh history for.
        `top` : `int`
            The requested number of entries in the refresh history. If not provided,
            the default is the last available 500 entries.

        Returns
        -------
        `list`
            List of `Refresh` objects.

        Raises
        ------
        `TypeError`
            If the `Dataset` is not refreshable.
        """

        # TODO: What if they pass in a partially constructed Dataset obj?

        # If string, we need to find out if the dataset is refreshable.
        if isinstance(dataset, str):
            dataset = self.get_dataset(dataset)

        if not dataset.is_refreshable:
            raise TypeError(
                "Dataset is not refreshable. Dataset id: {dataset.id}. Dataset name: {dataset.name}."
            )

        resource = "https://api.powerbi.com/v1.0/myorg/datasets/{0}/refreshes"
        params = {
            "$top": top,
        }

        raw = self._get_resource(resource, dataset.id, parameters=params)

        return [Refresh.from_raw(raw=refresh) for refresh in raw]

    def get_dataset(self, dataset_id):
        """
        Returns the specified dataset.

        Parameters
        ----------
        `dataset_id` : `str`
            Id of the Dataset object to get.

        Returns
        -------
        `Dataset`
            Dataset matching the specified Id.
        """

        # TODO: What if the Dataset isn't found?

        resource = "https://api.powerbi.com/v1.0/myorg/datasets/{0}"
        raw = self._get_resource(resource, dataset_id)

        return Dataset.from_raw(raw=raw)

    def get_activity_events(self, start_date_time, end_date_time, filter=None):
        """
        Returns a list of Activity Events on the Power BI Instance for a
        given time period. Activity Events can include viewing reports,
        downloading reports, modifying datasets, etc.

        Note: Due to a limitation of the Power BI Rest API, the start and
        end date times must be for the same UTC day. In other words, this
        method can only query the API one day at a time.

        If the number of Activity Events exceeds the API's limit, then this
        method will continue to call the API until all records are retrieved.

        Parameters
        ----------
        `start_date_time` : `str`
            Start date and time of the time period for audit event results.
            Must be in ISO 8601 compliant UTC format: 'yyyy-mm-ddThh:mm:ss.SSSZ'
        `end_date_time` : `str`
            End date and time of the time period for audit event results. Must
            be in ISO 8601 compliant UTC format: 'yyyy-mm-ddThh:mm:ss.SSSZ'
        `filter` : `str`
            Filters the results based on a boolean condition, using 'Activity',
            'UserId', or both properties. Supports only 'eq' and 'and' operators.

        Returns
        -------
        `list`
            List of `ActivityEvent` objects.

        Raises
        ------
        `ValueError`
            If supplied start and end times are invalid.
        """

        # TODO: Add support for passing in datetime types
        # TODO: Implment logging. Especially if this is making continuous calls.

        resource = "https://api.powerbi.com/v1.0/myorg/admin/activityevents"
        params = {
            # API expects dtms to be enclosed in single quotes.
            "startDateTime": "'" + start_date_time + "'",
            "endDateTime": "'" + end_date_time + "'",
            "$filter": filter,
        }

        raw = self._get_resource(resource, parameters=params)

        # Handle json errors
        if "error" in raw:
            error = raw["error"]
            message = error["message"]

            if "within the same UTC day" in message:
                raise ValueError(
                    "start_date_time and end_date_time must be on the same UTC day."
                )

        # API will return continuation token when further requests needed to
        # get all data. "continuationToken" will be null when no more data.

        activity_events = raw["activityEventEntities"]
        continuation_token = raw["continuationToken"]
        continuation_uri = raw["continuationUri"]

        while continuation_token:
            raw = self._get_resource(continuation_uri)
            activity_events.extend(raw["activityEventEntities"])
            continuation_token = raw["continuationToken"]
            continuation_uri = raw["continuationUri"]

        return activity_events

    def get_dataset_to_dataflow_links_in_group(self, group):
        """
        Returns a list of upstream dataflows for datasets from the specified group.

        Parameters
        ----------
        `group` : `str`
            Id of the specified group.

        Returns
        -------
        `list`
            List of `DatasetToDataflowLink` objects.
        """

        # TODO: Add "resolve" arg that will return the links with PBI Objects
        # instead of strings

        if isinstance(group, Group):
            group_id = group.id
        else:
            group_id = group

        resource = (
            "https://api.powerbi.com/v1.0/myorg/groups/{}/datasets/upstreamDataflows"
        )

        raw = self._get_resource(resource, group_id)

        return [
            DatasetToDataflowLink.from_raw(raw=dataset_to_dataflow_link)
            for dataset_to_dataflow_link in raw
        ]

    def get_dataset_users(self, dataset):
        """
        Returns a list of principals that have access to the specified dataset.

        Parameters
        ----------
        `dataset` : `Union[str, Dataset]`
            The Dataset Id or Dataset object to retrieve users for.

        Returns
        -------
        `list`
            List of `DatasetUserAccess` objects for the specified dataset.
        """

        if isinstance(dataset, Dataset):
            dataset_id = dataset.id
        else:
            dataset_id = dataset

        resource = "https://api.powerbi.com/v1.0/myorg/datasets/{}/users"
        raw = self._get_resource(resource, dataset_id)

        return [
            DatasetUserAccess.from_raw(dataset_user_access)
            for dataset_user_access in raw
        ]
