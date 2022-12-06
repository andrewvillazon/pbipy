"""Operations for working with datasets."""

from ..models import (
    Dataset,
    DatasetToDataflowLink,
    DatasetUserAccess,
    Datasource,
    Group,
    Refresh,
)


class Datasets:
    """
    Operations for working with datasets.

    Methods correspond to end points laid out at:

    https://learn.microsoft.com/en-us/rest/api/power-bi/datasets

    Parameters
    ----------
    `client` : `PowerBI`
        pbipy PowerBI client for handling interactions with API.
    """

    def __init__(self, client):
        self.client = client

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
        raw = self.client._get_resource(resource, dataset_id)

        return Dataset.from_raw(raw=raw)

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
        raw = self.client._get_resource(resource, group_id, dataset)

        return Dataset.from_raw(raw=raw)

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

        raw = self.client._get_resource(resource, group_id)

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
        raw = self.client._get_resource(resource, dataset_id)

        return [
            DatasetUserAccess.from_raw(dataset_user_access)
            for dataset_user_access in raw
        ]
    
    def get_dataset_users_in_group(self, group, dataset):
        if isinstance(group, Group):
            group_id = group.id
        else:
            group_id = group.id
        
        if isinstance(dataset, Dataset):
            dataset_id = dataset.id
        else:
            dataset_id = dataset
        
        resource = "https://api.powerbi.com/v1.0/myorg/groups/{}/datasets/{}/users"
        raw = self.client._get_resource(resource, group_id, dataset_id)

        return [
            DatasetUserAccess.from_raw(dataset_user_access)
            for dataset_user_access in raw
        ]

    def get_datasets_in_group(self, group):
        if isinstance(group, Group):
            id = group.id
        else:
            id = group

        resource = "https://api.powerbi.com/v1.0/myorg/groups/{0}/datasets"
        raw = self.client._get_resource(resource, id)

        return [Dataset.from_raw(raw=dataset) for dataset in raw]

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

        raw = self.client._get_resource(resource, dataset.id, parameters=params)

        return [Refresh.from_raw(raw=refresh) for refresh in raw]

    def get_datasources(self, dataset):
        """
        Returns a list of data sources for the specified dataset.

        Parameters
        ----------
        `dataset` : `Union[str, Dataset]`
            The Dataset Id or Dataset object to retrieve datasources for.

        Returns
        -------
        `list`
            List of `Datasource` objects for the specified Dataset.
        """

        if isinstance(dataset, Dataset):
            dataset_id = dataset.id
        else:
            dataset_id = dataset
        
        resource = "https://api.powerbi.com/v1.0/myorg/datasets/{}/datasources"
        raw = self.client._get_resource(resource, dataset_id)

        return [Datasource.from_raw(datasource) for datasource in raw]
