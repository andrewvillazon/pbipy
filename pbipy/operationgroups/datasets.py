"""Operations for working with datasets."""

from ..models import (
    Dataset,
    DatasetToDataflowLink,
    DatasetUserAccess,
    Datasource,
    DirectQueryRefreshSchedule,
    Gateway,
    Group,
    MashupParameter,
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
        return self.client._get_and_load_resource(resource, dataset_id, model=Dataset)

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
        return self.client._get_and_load_resource(resource, group_id, dataset, model=Dataset)

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

        return self.client._get_and_load_resource(resource, group_id, model=DatasetToDataflowLink)

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
        return self.client._get_and_load_resource(resource, dataset_id, model=DatasetUserAccess)
    
    def get_dataset_users_in_group(self, group, dataset):
        if isinstance(group, Group):
            group_id = group.id
        else:
            group_id = group
        
        if isinstance(dataset, Dataset):
            dataset_id = dataset.id
        else:
            dataset_id = dataset
        
        resource = "https://api.powerbi.com/v1.0/myorg/groups/{}/datasets/{}/users"
        return self.client._get_and_load_resource(resource, group_id, dataset_id, model=DatasetUserAccess)


    def get_datasets_in_group(self, group):
        if isinstance(group, Group):
            id = group.id
        else:
            id = group

        resource = "https://api.powerbi.com/v1.0/myorg/groups/{0}/datasets"
        return self.client._get_and_load_resource(resource, id, model=Dataset)

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

        return self.client._get_and_load_resource(resource, dataset.id, model=Refresh, parameters=params)

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
        return self.client._get_and_load_resource(resource, dataset_id, model=Datasource)
    
    def get_datasources_in_group(self, group, dataset):
        """
        Returns a list of data sources for the specified dataset from the specified group.

        Parameters
        ----------
        `group` : `Union[str, Group]`
            The Group Id or Group object where the Dataset resides.
        `dataset` : `Union[str, Dataset]`
            The Dataset Id or Dataset object to retrieve datasources for.

        Returns
        -------
        `list`
            List of `Datasource` objects for the specified Dataset and Group.
        """

        if isinstance(group, Group):
            group_id = group.id
        else:
            group_id = group
        
        if isinstance(dataset, Dataset):
            dataset_id = dataset.id
        else:
            dataset_id = dataset
        
        resource = "https://api.powerbi.com/v1.0/myorg/groups/{}/datasets/{}/datasources"

        return self.client._get_and_load_resource(resource, group_id, dataset_id, model=Datasource)
    
    def get_direct_query_refresh_schedule(self, dataset):
        if isinstance(dataset, Dataset):
            dataset_id = dataset.id
        else:
            dataset_id = dataset
        
        resource = "https://api.powerbi.com/v1.0/myorg/datasets/{}/directQueryRefreshSchedule"

        return self.client._get_and_load_resource(resource, dataset_id, model=DirectQueryRefreshSchedule)
    
    def get_direct_query_refresh_schedule_in_group(self, group, dataset):
        if isinstance(group, Group):
            group_id = group.id
        else:
            group_id = group
        
        if isinstance(dataset, Dataset):
            dataset_id = dataset.id
        else:
            dataset_id = dataset
        
        resource = "https://api.powerbi.com/v1.0/myorg/groups/{}/datasets/{}/directQueryRefreshSchedule"

        return self.client._get_and_load_resource(resource, group_id, dataset_id, model=DirectQueryRefreshSchedule)
    
    def get_parameters(self, dataset):
        if isinstance(dataset, Dataset):
            dataset_id = dataset.id
        else:
            dataset_id = dataset
        
        resource = "https://api.powerbi.com/v1.0/myorg/datasets/{}/parameters"

        return self.client._get_and_load_resource(resource, dataset_id, model=MashupParameter)
    
    def discover_gateways(self, dataset):
        """
        Returns a list of gateways that the specified dataset from My workspace 
        can be bound to.

        This API call is only relevant to datasets that have at least one on-premises 
        connection. For datasets with cloud-only connections, this API call returns 
        an empty list.

        Parameters
        ----------
        `dataset` : `Union[str, Dataset]`
            Dataset Id or `Dataset` object to discover Gateways for.

        Returns
        -------
        `list`
            List of `Gateway` objects for the specified Dataset.
        """

        if isinstance(dataset, Dataset):
            dataset_id = dataset.id
        else:
            dataset_id = dataset
        
        resource = f"https://api.powerbi.com/v1.0/myorg/datasets/{dataset_id}/Default.DiscoverGateways"
        response = self.client.session.get(resource)
        raw = response.json()
        
        if not raw["value"]:
            return []
        else:
            return [Gateway.from_raw(gateway) for gateway in raw["value"]]
        