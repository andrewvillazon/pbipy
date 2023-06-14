"""Operations for working with datasets."""
from dataclasses import asdict
from typing import Union

from requests import HTTPError

from pbipy.utils import to_camel_case
from ..models import (
    Dataset,
    DatasetRefreshDetail,
    DatasetToDataflowLink,
    DatasetUserAccess,
    Datasource,
    DirectQueryRefreshSchedule,
    Gateway,
    Group,
    MashupParameter,
    Refresh,
    RefreshSchedule,
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
            The Dataset Id or `Dataset` object to retrieve users for.

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
        """
        Returns a list of principals that have access to the specified dataset.

        Parameters
        ----------
        `group` : `Union[str, Group]`
            The Group Id or `Group` object where the provided dataset resides.
        `dataset` : `Union[str, Dataset]`
            The Dataset Id or `Dataset` object to retrieve users for.

        Returns
        -------
        `list`
            List of `DatasetUserAccess` objects for the specified dataset.
        """

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
    
    def get_datasets(self):
        """
        Returns a list of datasets from My workspace.

        Returns
        -------
        `list[Dataset]`
            List of `Dataset` objects.

        Raises
        ------
        `HTTPError`
            If api response status code is not equal to 200.
        """

        resource = "https://api.powerbi.com/v1.0/myorg/datasets"
        response = self.client.session.get(resource)

        if response.status_code != 200:
            raise HTTPError(f"Encountered problem getting datasets. Response details: {response}")
        
        raw = response.json()

        return [Dataset.from_raw(refresh) for refresh in raw["value"]]


    def get_datasets_in_group(self, group):
        """
        Returns a list of datasets from the specified workspace.

        Parameters
        ----------
        `group` : `Union[str, Group]`
            The Group Id or `Group` Object to get the datasets for.

        Returns
        -------
        `list[Dataset]`
            List of `Dataset` objects.
        """

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
    
    def get_refresh_history_in_group(self, group, dataset, top=None):
        """
        Returns the refresh history for the specified dataset from the specified workspace.

        Parameters
        ----------
        `group` : `Union[str, Group]`
            Group Id or `Group` object to get refresh history for.
        `dataset` : `Union[str, Dataset]`
            Dataset Id or `Dataset` object to get refresh history for.
        `top` : `int`, optional
            The requested number of entries in the refresh history. If not provided,
            the default is the last available 500 entries.

        Returns
        -------
        `list`
            List of `Refresh` objects for the specified group and dataset.
        """

        if isinstance(group, Group):
            group_id = group.id
        else:
            group_id = group
        
        if isinstance(dataset, Dataset):
            dataset_id = dataset.id
        else:
            dataset_id = dataset
        
        resource = f"https://api.powerbi.com/v1.0/myorg/groups/{group_id}/datasets/{dataset_id}/refreshes"
        parameters = {
            "$top": top,
        }
        response = self.client.session.get(resource, params=parameters)
        raw = response.json()

        if not raw["value"]:
            return []
        else:
            return [Refresh.from_raw(refresh) for refresh in raw["value"]]

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
        """
        Returns the refresh schedule for a specified DirectQuery or LiveConnection 
        dataset from My workspace.

        Parameters
        ----------
        `dataset` : `Union[str, Dataset]`
            The Dataset Id or `Dataset` object to return the refresh schedule for.

        Returns
        -------
        `DirectQueryRefreshSchedule`
            The direct query refresh schedule for the specified dataset.
        """

        # TODO: What if there's no refresh schedule for the Dataset?

        if isinstance(dataset, Dataset):
            dataset_id = dataset.id
        else:
            dataset_id = dataset
        
        resource = "https://api.powerbi.com/v1.0/myorg/datasets/{}/directQueryRefreshSchedule"

        return self.client._get_and_load_resource(resource, dataset_id, model=DirectQueryRefreshSchedule)
    
    def get_direct_query_refresh_schedule_in_group(self, group, dataset):
        """
        Returns the refresh schedule for a specified DirectQuery or LiveConnection 
        dataset from the specified workspace.

        Parameters
        ----------
        `group` : `Union[str, Group]`
            The Group Id or `Group` object to where the dataset resides.
        `dataset` : `Union[str, Dataset]`
            The Dataset Id or `Dataset` object to return the refresh schedule for.

        Returns
        -------
        `DirectQueryRefreshSchedule`
            The direct query refresh schedule for the specified dataset.
        """

        # TODO: What if there's no refresh schedule for the Dataset?

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
        """
        Returns a list of parameters for the specified dataset from My 
        workspace.

        Parameters
        ----------
        `dataset` : `Union[str, Dataset]`
            Dataset Id or `Dataset` object to retrieve the parameters for.

        Returns
        -------
        `List[MashupParameter]`
            List of `MashupParameter` objects from the specified group 
            and dataset.
        """

        if isinstance(dataset, Dataset):
            dataset_id = dataset.id
        else:
            dataset_id = dataset
        
        resource = "https://api.powerbi.com/v1.0/myorg/datasets/{}/parameters"

        return self.client._get_and_load_resource(resource, dataset_id, model=MashupParameter)
    
    def get_parameters_in_group(self, group, dataset):
        """
        Returns a list of parameters for the specified dataset from the specified 
        workspace.

        Parameters
        ----------
        `group` : `Union[str, Group]`
            Group Id or `Group` object to retrieve the parameters for.
        `dataset` : `Union[str, Dataset]`
            Dataset Id or `Dataset` object to retrieve the parameters for.

        Returns
        -------
        `List[MashupParameter]`
            List of `MashupParameter` objects from the specified group 
            and dataset.
        """

        if isinstance(group, Group):
            group_id = group.id
        else:
            group_id = group
        
        if isinstance(dataset, Dataset):
            dataset_id = dataset.id
        else:
            dataset_id = dataset
        
        resource = f"https://api.powerbi.com/v1.0/myorg/groups/{group_id}/datasets/{dataset_id}/parameters"
        response = self.client.session.get(resource)
        raw = response.json()
        
        if not raw["value"]:
            return []
        else:
            return [MashupParameter.from_raw(parameter) for parameter in raw["value"]]
    
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

    def cancel_refresh(self, dataset, refresh):
        """
        Cancels the specified refresh operation for the specified dataset from My workspace.

        Parameters
        ----------
        `dataset` : `Union[str, Dataset]`
            Dataset Id or `Dataset` object to cancel the refresh for.
        `refresh` : `Union[str, Refresh]`
            Refresh Id or `Refresh` object to cancel the refresh for.
        
        Raises
        ------
        `HTTPError`
            If api response status code is not equal to 200.
        """

        if isinstance(dataset, Dataset):
            dataset_id = dataset.id
        else:
            dataset_id = dataset
        
        if isinstance(refresh, Refresh):
            refresh_id = refresh.id
        else:
            refresh_id = refresh
        
        resource = f"https://api.powerbi.com/v1.0/myorg/datasets/{dataset_id}/refreshes/{refresh_id}"
        response = self.client.session.delete(resource)

        if response.status_code != 200:
            raise HTTPError(f"Encountered problem cancelling refresh. Dataset id: {dataset_id}, Refresh id: {refresh_id}. Response details: {response}")

    def cancel_refresh_in_group(self, dataset, refresh, group):
        """
        Cancels the specified refresh operation for the specified dataset from the specified workspace.

        Parameters
        ----------
        `dataset` : `Union[str, Dataset]`
            Dataset Id or `Dataset` object to cancel the refresh for.
        `refresh` : `Union[str, Refresh]`
            Refresh Id or `Refresh` object to cancel the refresh for.
        `group` : `Union[str, Group]`
            Group Id or `Group` object to cancel the refresh for.
        
        Raises
        ------
        `HTTPError`
            If api response status code is not equal to 200.
        """

        if isinstance(dataset, Dataset):
            dataset_id = dataset.id
        else:
            dataset_id = dataset
        
        if isinstance(refresh, Refresh):
            refresh_id = refresh.id
        else:
            refresh_id = refresh
        
        if isinstance(group, Group):
            group_id = group.id
        else:
            group_id = group
        
        resource = f"https://api.powerbi.com/v1.0/myorg/groups/{group_id}/datasets/{dataset_id}/refreshes/{refresh_id}"
        response = self.client.session.delete(resource)
        
        if response.status_code != 200:
            raise HTTPError(f"Encountered problem cancelling refresh. Group id: {group_id}, Dataset id: {dataset_id}, Refresh id: {refresh_id}. Response details: {response}")
    
    def delete_dataset(self, dataset):
        """
        Deletes the specified dataset from My workspace.

        Parameters
        ----------
        `dataset` : `Union[str, Dataset]`
            Dataset Id or `Dataset` object to delete.

        Raises
        ------
        `HTTPError`
            If api response status code is not equal to 200
        """

        if isinstance(dataset, Dataset):
            dataset_id = dataset.id
        else:
            dataset_id = dataset
        
        resource = f"https://api.powerbi.com/v1.0/myorg/datasets/{dataset_id}"
        response = self.client.session.delete(resource)

        if response.status_code != 200:
            raise HTTPError(f"Encountered problem deleting Dataset. Dataset id: {dataset_id}. Response details: {response}")
    
    def delete_dataset_in_group(self, dataset, group):
        if isinstance(dataset, Dataset):
            dataset_id = dataset.id
        else:
            dataset_id = dataset
        
        if isinstance(group, Group):
                    group_id = group.id
        else:
            group_id = group
        
        resource = f"https://api.powerbi.com/v1.0/myorg/groups/{group_id}/datasets/{dataset_id}"
        response = self.client.session.delete(resource)

        if response.status_code != 200:
            raise HTTPError(f"Encountered problem deleting Dataset. Dataset id: {dataset_id}, Group id: {group_id} Response details: {response}")
    
    def get_refresh_execution_details(self, dataset, refresh):
        """
        Returns execution details of an enhanced refresh operation for the specified dataset from My workspace.

        Parameters
        ----------
        `dataset` : `Union[str, Dataset]`
            Dataset Id or `Dataset` object to get the execution detail for.
        `refresh` : `Union[str, Refresh]`
            Refresh Id or `Refresh` object to get the execution detail for.

        Returns
        -------
        `DatasetRefreshDetail`
            The detail of the Dataset refresh.
        """

        if isinstance(dataset, Dataset):
            dataset_id = dataset.id
        else:
            dataset_id = dataset
        
        if isinstance(refresh, Refresh):
            refresh_id = refresh.id
        else:
            refresh_id = refresh
        
        resource = f"https://api.powerbi.com/v1.0/myorg/datasets/{dataset_id}/refreshes/{refresh_id}"
        response = self.client.session.get(resource)
        raw = response.json()

        return DatasetRefreshDetail.from_raw(raw)
    
    def get_refresh_execution_details_in_group(self, dataset, group, refresh):
        """
        Returns execution details of an enhanced refresh operation for the specified dataset from the specified workspace.

        Parameters
        ----------
        `dataset` : `Union[str, Dataset]`
            Dataset Id or `Dataset` object to get the execution detail for.
        `group` : `Union[str, Group]`
            Group Id or `Group` object to get the execution detail for.
        `refresh` : `Union[str, Refresh]`
            Refresh Id or `Refresh` object to get the execution detail for.

        Returns
        -------
        `DatasetRefreshDetail`
            The detail of the Dataset refresh.
        """

        if isinstance(dataset, Dataset):
            dataset_id = dataset.id
        else:
            dataset_id = dataset
        
        if isinstance(group, Group):
            group_id = group.id
        else:
            group_id = group

        if isinstance(refresh, Refresh):
            refresh_id = refresh.id
        else:
            refresh_id = refresh
        
        resource = f"https://api.powerbi.com/v1.0/myorg/groups/{group_id}/datasets/{dataset_id}/refreshes/{refresh_id}"
        response = self.client.session.get(resource)
        raw = response.json()

        return DatasetRefreshDetail.from_raw(raw)
    
    def get_refresh_schedule(self, dataset):
        """
        Returns the refresh schedule for the specified dataset from My workspace.

        Parameters
        ----------
        `dataset` : `Union[str, Dataset]`
            Dataset Id or `Dataset` object to get the refresh schedule for.

        Returns
        -------
        `RefreshSchedule`
            The refresh schedule for the specified dataset.
        """

        if isinstance(dataset, Dataset):
            dataset_id = dataset.id
        else:
            dataset_id = dataset
        
        resource = f"https://api.powerbi.com/v1.0/myorg/datasets/{dataset_id}/refreshSchedule"
        response = self.client.session.get(resource)
        raw = response.json()

        return RefreshSchedule.from_raw(raw)
    
    def get_refresh_schedule_in_group(self, group, dataset):
        """
        Returns the refresh schedule for the specified dataset from My workspace.

        Parameters
        ----------
        `group` : `Union[str, Group]`
            The Group Id or `Group` object where the dataset resides.
        `dataset` : `Union[str, Dataset]`
            Dataset Id or `Dataset` object to get the refresh schedule for.

        Returns
        -------
        `RefreshSchedule`
            The refresh schedule for the specified dataset.
        """

        if isinstance(group, Group):
            group_id = group.id
        else:
            group_id = group

        if isinstance(dataset, Dataset):
            dataset_id = dataset.id
        else:
            dataset_id = dataset
        
        resource = f"https://api.powerbi.com/v1.0/myorg/groups/{group_id}/datasets/{dataset_id}/refreshSchedule"
        response = self.client.session.get(resource)
        raw = response.json()

        return RefreshSchedule.from_raw(raw)
    
    def post_dataset_user(self, dataset, identifier, principal_type, dataset_user_access_right):
        """
        Grants the specified user's permissions to the specified dataset.

        Parameters
        ----------
        `dataset` : `Union[str, Dataset]`
            Dataset Id or `Dataset` object the permissions will be applied to.
        `identifier` : `str`
            UPN or object id of the principal.
        `principal_type` : `str`
            Principal type of the above identifier, e.g., "User", "Group".
        `dataset_user_access_right` : `str`
            The access right to grant to the user for the dataset, e.g., "Read", "ReadReshare".

        Raises
        ------
        `HTTPError`
            If the api status code is not equal to 200.
        """

        if isinstance(dataset, Dataset):
            dataset_id = dataset.id
        else:
            dataset_id = dataset
        
        payload = {
            "identifier": identifier,
            "principalType": principal_type,
            "datasetUserAccessRight": dataset_user_access_right
        }

        resource = f"https://api.powerbi.com/v1.0/myorg/datasets/{dataset_id}/users"
        response = self.client.session.post(resource, json=payload)

        if response.status_code != 200:
            raise HTTPError(f"Encountered problem posting dataset user. Response details: {response}")
    
    def post_dataset_user_in_group(self, group, dataset, identifier, principal_type, dataset_user_access_right):
        """
        Grants the specified user's permissions to the specified dataset.

        Parameters
        ----------
        `group` : `Union[str, Group]`
            Group Id or `Group` object where the dataset resides.
        `dataset` : `Union[str, Dataset]`
            Dataset Id or `Dataset` object the permissions will be applied to.
        `identifier` : `str`
            UPN or object id of the principal.
        `principal_type` : `str`
            Principal type of the above identifier, e.g., "User", "Group".
        `dataset_user_access_right` : `str`
            The access right to grant to the user for the dataset, e.g., "Read", "ReadReshare".

        Raises
        ------
        `HTTPError`
            If the api status code is not equal to 200.
        """
        
        if isinstance(group, Group):
            group_id = group.id
        else:
            group_id = group
        
        if isinstance(dataset, Dataset):
            dataset_id = dataset.id
        else:
            dataset_id = dataset
        
        payload = {
            "identifier": identifier,
            "principalType": principal_type,
            "datasetUserAccessRight": dataset_user_access_right
        }
        
        resource = f"https://api.powerbi.com/v1.0/myorg/groups/{group_id}/datasets/{dataset_id}/users"
        response = self.client.session.post(resource, json=payload)

        if response.status_code != 200:
            raise HTTPError(f"Encountered problem posting dataset user. Response details: {response}")
    
    def put_dataset_user(self, dataset, identifier, principal_type, dataset_user_access_right):
        """
        Updates the existing dataset permissions of the specified user to the 
        specified permissions.

        Parameters
        ----------
        `dataset` : `Union[str, Dataset]`
            Dataset Id or `Dataset` object the permissions will be applied to.
        `identifier` : `str`
            UPN or object id of the principal.
        `principal_type` : `str`
            Principal type of the above identifier, e.g., "User", "Group".
        `dataset_user_access_right` : `str`
            The access right to grant to the user for the dataset, e.g., 
            "Read", "ReadReshare".

        Raises
        ------
        `HTTPError`
            If the api status code is not equal to 200.
        """
        
        if isinstance(dataset, Dataset):
            dataset_id = dataset.id
        else:
            dataset_id = dataset
        
        payload = {
            "identifier": identifier,
            "principalType": principal_type,
            "datasetUserAccessRight": dataset_user_access_right
        }
        
        resource = f"https://api.powerbi.com/v1.0/myorg/datasets/{dataset_id}/users"
        response = self.client.session.put(resource, json=payload)

        if response.status_code != 200:
            raise HTTPError(f"Encountered problem putting dataset user. Response details: {response}")
    
    def put_dataset_user_in_group(self, group, dataset, identifier, principal_type, dataset_user_access_right):
        """
        Updates the existing dataset permissions of the specified user to the 
        specified permissions.

        Parameters
        ----------
        `group` : `Union[str, Group]`
            Group Id or `Group` object where the dataset resides.
        `dataset` : `Union[str, Dataset]`
            Dataset Id or `Dataset` object the permissions will be applied to.
        `identifier` : `str`
            UPN or object id of the principal.
        `principal_type` : `str`
            Principal type of the above identifier, e.g., "User", "Group".
        `dataset_user_access_right` : `str`
            The access right to grant to the user for the dataset, e.g., 
            "Read", "ReadReshare".

        Raises
        ------
        `HTTPError`
            If the api status code is not equal to 200.
        """

        if isinstance(group, Group):
            group_id = group.id
        else:
            group_id = group

        if isinstance(dataset, Dataset):
            dataset_id = dataset.id
        else:
            dataset_id = dataset
        
        payload = {
            "identifier": identifier,
            "principalType": principal_type,
            "datasetUserAccessRight": dataset_user_access_right
        }
        
        resource = f"https://api.powerbi.com/v1.0/myorg/groups/{group_id}/datasets/{dataset_id}/users"
        response = self.client.session.put(resource, json=payload)

        if response.status_code != 200:
            raise HTTPError(f"Encountered problem posting dataset user. Response details: {response}")
    
    def refresh_dataset(self, dataset, notify_option, **options):
        """
        Triggers a refresh for the specified dataset from My workspace. 
        An enhanced refresh is triggered only if a request payload other 
        than `notifyOption` is set.

        Parameters
        ----------
        `dataset` : `Union[str, Dataset]`
            Dataset Id or `Dataset` object to trigger the refresh for.
        `notify_option` : `str`
            Mail notification options. This parameter is not applicable 
            to enhanced refreshes or API operations with a service principal.
        `**options`
            Extra options to pass to the refresh request. Supported options are:
            `apply_refresh_policy`,
            `commit_mode`,
            `effective_date`,
            `max_parallelism`,
            `objects`,
            `retry_count`,
            `type`

        Raises
        ------
        `ValueError`
            If an unsupported option is supplied.
        `HTTPError`
            If the api status code is not equal to 200.
        """

        supported_options = [
            "apply_refresh_policy",
            "commit_mode",
            "effective_date",
            "max_parallelism",
            "objects",
            "retry_count",
            "type",
        ]

        for k in options.keys():
            if k not in supported_options:
                raise ValueError(f"Unsupported option supplied: {k}. Supported options are: {supported_options}")

        if isinstance(dataset, Dataset):
            dataset_id = dataset.id
        else:
            dataset_id = dataset
        
        payload = {"notifyOption": notify_option}
        payload.update({to_camel_case(k):v for k,v in options.items()})
        
        resource = f"https://api.powerbi.com/v1.0/myorg/datasets/{dataset_id}/refreshes"
        response = self.client.session.post(resource, json=payload)

        if response.status_code not in [200, 202]:
            raise HTTPError(f"Encountered problem refreshing dataset. Response details: {response}")
    
    def refresh_dataset_in_group(self, group, dataset, notify_option, **options):
        """
        Triggers a refresh for the specified dataset from the specified 
        workspace. An enhanced refresh is triggered only if a request 
        payload other than `notifyOption` is set.

        Parameters
        ----------
        `group` : `Union[str, Group]`
            Group Id or `Group` object where the dataset resides.
        `dataset` : `Union[str, Dataset]`
            Dataset Id or `Dataset` object to trigger the refresh for.
        `notify_option` : `str`
            Mail notification options. This parameter is not applicable 
            to enhanced refreshes or API operations with a service principal.
        `**options`
            Extra options to pass to the refresh request. Supported options are:
            `apply_refresh_policy`,
            `commit_mode`,
            `effective_date`,
            `max_parallelism`,
            `objects`,
            `retry_count`,
            `type`

        Raises
        ------
        `ValueError`
            If an unsupported option is supplied.
        `HTTPError`
            If the api status code is not equal to 200.
        """

        supported_options = [
            "apply_refresh_policy",
            "commit_mode",
            "effective_date",
            "max_parallelism",
            "objects",
            "retry_count",
            "type",
        ]

        for k in options.keys():
            if k not in supported_options:
                raise ValueError(f"Unsupported option supplied: {k}. Supported options are: {supported_options}")
        
        if isinstance(group, Group):
            group_id = group.id
        else:
            group_id = group

        if isinstance(dataset, Dataset):
            dataset_id = dataset.id
        else:
            dataset_id = dataset
        
        payload = {"notifyOption": notify_option}
        payload.update({to_camel_case(k):v for k,v in options.items()})
        
        resource = f"https://api.powerbi.com/v1.0/myorg/groups/{group_id}/datasets/{dataset_id}/refreshes"
        response = self.client.session.post(resource, json=payload)

        if response.status_code not in [200, 202]:
            raise HTTPError(f"Encountered problem refreshing dataset. Response details: {response}")
        
    def take_over_in_group(self, group, dataset):
        """
        Transfers ownership over the specified dataset to the current authorized 
        user.

        Parameters
        ----------
        `group` : `Union[str, Group]`
            Group Id or `Group` object where the dataset resides
        `dataset` : `Union[str, Dataset]`
            Dataset Id or `Dataset` object to take ownership of.

        Raises
        ------
        `HTTPError`
            If the api status code is not equal to 200.
        """

        if isinstance(group, Group):
            group_id = group.id
        else:
            group_id = group

        if isinstance(dataset, Dataset):
            dataset_id = dataset.id
        else:
            dataset_id = dataset
        
        resource = f"https://api.powerbi.com/v1.0/myorg/groups/{group_id}/datasets/{dataset_id}/Default.TakeOver"
        response = self.client.session.post(resource)

        if response.status_code not in [200, 202]:
            raise HTTPError(f"Encountered problem taking over group. Response details: {response}")
    
    def update_dataset(self, dataset, **properties):
        """
        Updates the properties for the specified dataset from My workspace.

        Parameters
        ----------
        `dataset` : `Union[str, Dataset]`
            Dataset or `Dataset` object to update properties for.
        `**properties`
            The property or properties of the dataset to modify, e.g.,
            `target_storage_mode = "PremiumFiles"`.

        Raises
        ------
        `ValueError`
            If no dataset properties are provided.
        `ValueError`
            If unsupported properties provided.
        `HTTPError`
            If api response code is not equal to 200 (OK).
        """

        # TODO: Should give the caller option to pass in modified Dataset obj?
        # TODO: Add option to return the dataset?

        if isinstance(dataset, Dataset):
            dataset_id = dataset.id
        else:
            dataset_id = dataset
        
        if not properties:
            raise ValueError("No dataset properties to modify were provided. Example of providing properties: update_dataset(dataset, target_storage_mode='PremiumFiles')")

        # TODO: Check what is actually supported. Not all Dataset properties will be modifiable from this endpoint.
        supported_properties = ["target_storage_mode",]

        for k in properties.keys():
            if k not in supported_properties:
                raise ValueError(f"Unsupported option supplied: {k}. Supported options are: {supported_properties}")
        
        payload = {to_camel_case(k):v for k, v in properties.items()}
        
        resource = f"https://api.powerbi.com/v1.0/myorg/datasets/{dataset_id}"
        response = self.client.session.patch(resource, json=payload)

        if response.status_code != 200:
            raise HTTPError(f"Encountered problem updating dataset. Response details: {response}")
    
    def update_dataset_in_group(self, group, dataset, **properties):
        """
        Updates the properties for the specified dataset from My workspace.

        Parameters
        ----------
        `group` : `Union[str, Group]`
            Group Id or `Group` object where the dataset resides.
        `dataset` : `Union[str, Dataset]`
            Dataset or `Dataset` object to update properties for.
        `**properties`
            The property or properties of the dataset to modify, e.g.,
            `target_storage_mode = "PremiumFiles"`.

        Raises
        ------
        `ValueError`
            If no dataset properties are provided.
        `ValueError`
            If unsupported properties provided.
        `HTTPError`
            If api response code is not equal to 200 (OK).
        """

        if isinstance(group, Group):
            group_id = group.id
        else:
            group_id = group

        if isinstance(dataset, Dataset):
            dataset_id = dataset.id
        else:
            dataset_id = dataset
        
        if not properties:
            raise ValueError("No dataset properties to modify were provided. Example of providing properties: update_dataset(group, datasets, target_storage_mode='PremiumFiles')")

        # TODO: Check what is actually supported. Not all Dataset properties will be modifiable from this endpoint.
        supported_properties = ["target_storage_mode",]

        for k in properties.keys():
            if k not in supported_properties:
                raise ValueError(f"Unsupported option supplied: {k}. Supported options are: {supported_properties}")
        
        payload = {to_camel_case(k):v for k, v in properties.items()}
        
        resource = f"https://api.powerbi.com/v1.0/myorg/groups/{group_id}/datasets/{dataset_id}"
        response = self.client.session.patch(resource, json=payload)

        if response.status_code != 200:
            raise HTTPError(f"Encountered problem updating dataset. Response details: {response}")
    
    def update_datasources(self, dataset, update_details:list[dict]):
        """
        Updates the data sources of the specified dataset from My workspace.

        Parameters
        ----------
        `dataset` : `Union[str, Dataset]`
            Dataset or `Dataset` object to update datasources for.
        `update_details` : `list[dict]`
            List of updates to make to the datasources. Updates take the 
            form of a list of dicts.

            For examples what the update dict should look like see: 
            https://learn.microsoft.com/en-us/rest/api/power-bi/datasets/update-datasources#example

        Raises
        ------
        `ValueError`
            If update_details is empty list.
        `HTTPError`
            If api response code was not equal to 200 (OK).
        """

        if isinstance(dataset, Dataset):
            dataset_id = dataset.id
        else:
            dataset_id = dataset
        
        if not update_details:
            raise ValueError("Update details is an empty list. Please provide update_details.")
        
        # TODO: Add some validation to the content?
        payload = {"updateDetails": update_details}

        resource = f"https://api.powerbi.com/v1.0/myorg/datasets/{dataset_id}/Default.UpdateDatasources"
        response = self.client.session.post(resource, json=payload)

        if response.status_code != 200:
            raise HTTPError(f"Encountered problem updating datasources. Response details: {response}")
    
    def update_datasources_in_group(self, group, dataset, update_details:list[dict]):
        """
        Updates the data sources of the specified dataset from My workspace.

        Parameters
        ----------
        `group` : `Union[str, Group]`
            Group Id or `Group` object where the dataset resides.
        `dataset` : `Union[str, Dataset]`
            Dataset or `Dataset` object to update datasources for.
        `update_details` : `list[dict]`
            List of updates to make to the datasources. Updates take the 
            form of a list of dicts.

            For examples what the update dict should look like see: 
            https://learn.microsoft.com/en-us/rest/api/power-bi/datasets/update-datasources#example

        Raises
        ------
        `ValueError`
            If update_details is empty list.
        `HTTPError`
            If api response code was not equal to 200 (OK).
        """
        
        if isinstance(group, Group):
            group_id = group.id
        else:
            group_id = group

        if isinstance(dataset, Dataset):
            dataset_id = dataset.id
        else:
            dataset_id = dataset
        
        if not update_details:
            raise ValueError("Update details is an empty list. Please provide update_details.")
        
        # TODO: Add some validation to the content?
        payload = {"updateDetails": update_details}

        resource = f"https://api.powerbi.com/v1.0/myorg/groups/{group_id}/datasets/{dataset_id}/Default.UpdateDatasources"
        response = self.client.session.post(resource, json=payload)

        if response.status_code != 200:
            raise HTTPError(f"Encountered problem updating datasources. Response details: {response}")
    
    def update_direct_query_refresh_schedule(self, dataset, **options):
        """
        Updates the refresh schedule for a specified DirectQuery or LiveConnection 
        dataset from My workspace.

        Parameters
        ----------
        `dataset` : `Union[str, Dataset]`
            Dataset Id or `Dataset` object to update the refresh schedule for.
        `**options`
            Extra options to update on the refresh schedule. Supported options are:
            `enabled`,
            `days`,
            `frequency`,
            `local_time_zone_id`,
            `times`

        Raises
        ------
        `ValueError`
            Unsupported options were provided.
        `HTTPError`
            If api response status code is not equal to 200 (OK).
        """

        supported_options = ["enabled", "days", "frequency", "local_time_zone_id", "times"]

        for k in options.keys():
            if k not in supported_options:
                raise ValueError(f"Unsupported option supplied: {k}. Supported options are: {supported_options}")
        
        payload = {"value": {to_camel_case(k):v for k,v in options.items()}}
        
        if isinstance(dataset, Dataset):
            dataset_id = dataset.id
        else:
            dataset_id = dataset
        
        resource = f"https://api.powerbi.com/v1.0/myorg/datasets/{dataset_id}/directQueryRefreshSchedule"
        response = self.client.session.patch(resource, json=payload)

        if response.status_code != 200:
            raise HTTPError(f"Encountered problem updating direct query refresh schedule. Response details: {response}")

    def update_direct_query_refresh_schedule_in_group(self, group, dataset, **options):
        """
        Updates the refresh schedule for a specified DirectQuery or LiveConnection 
        dataset from My workspace.

        Parameters
        ----------
        `group` : `Union[str, Group]`
            Group Id or `Group` object where the dataset resides.
        `dataset` : `Union[str, Dataset]`
            Dataset Id or `Dataset` object to update the refresh schedule for.
        `**options`
            Extra options to update on the refresh schedule. Supported options are:
            `enabled`,
            `days`,
            `frequency`,
            `local_time_zone_id`,
            `times`

        Raises
        ------
        `ValueError`
            Unsupported options were provided.
        `HTTPError`
            If api response status code is not equal to 200 (OK).
        """

        supported_options = ["enabled", "days", "frequency", "local_time_zone_id", "times"]

        for k in options.keys():
            if k not in supported_options:
                raise ValueError(f"Unsupported option supplied: {k}. Supported options are: {supported_options}")
        
        payload = {"value": {to_camel_case(k):v for k,v in options.items()}}
        
        if isinstance(group, Group):
            group_id = group.id
        else:
            group_id = group
        
        if isinstance(dataset, Dataset):
            dataset_id = dataset.id
        else:
            dataset_id = dataset
        
        resource = f"https://api.powerbi.com/v1.0/myorg/groups/{group_id}/datasets/{dataset_id}/directQueryRefreshSchedule"
        response = self.client.session.patch(resource, json=payload)

        if response.status_code != 200:
            raise HTTPError(f"Encountered problem updating direct query refresh schedule. Response details: {response}")
    
    def execute_queries(self, dataset, queries: Union[str, list], **options):
        """
        Executes Data Analysis Expressions (DAX) queries against the provided 
        dataset. The dataset must reside in My workspace or another workspace.

        Parameters
        ----------
        `dataset` : `Union[str, Dataset]`
            Dataset Id or `Dataset` object to execute the queries against.
        `queries` : `Union[str, list]`
            A single `str` query or `list` of queries. 
            
            If providing multiple queries, this should be provided as a list 
            of dicts in the following form:

            ```
            queries=[
                {"query": "query 1 text"},
                {"query": "query 2 text"}
            ]
            ```

        Returns
        -------
        `dict`
            Results of the executed query.

        Raises
        ------
        `ValueError`
            If unsupported execution options are supplied.
        `HTTPError`
            If the Rest API returns a status code not equal to 200.
        """

        supported_options = ["impersonated_user_name", "serializer_settings"]

        for k in options.keys():
            if k not in supported_options:
                raise ValueError(f"Unsupported option supplied: {k}. Supported options are: {supported_options}")
        
        if isinstance(dataset, Dataset):
            dataset_id = dataset.id
        else:
            dataset_id = dataset
        
        if isinstance(queries, str):
            query_list = [{"query": queries}]
        else:
            query_list = queries
        
        payload = {"queries": query_list}
        payload.update({to_camel_case(k):v for k,v in options.items()})

        resource = f"https://api.powerbi.com/v1.0/myorg/datasets/{dataset_id}/executeQueries"
        response = self.client.session.post(resource, json=payload)

        if response.status_code != 200:
            raise HTTPError(f"Encountered problem executing query. Response details: {response}")
        
        return response.json()
    
    def execute_queries_in_group(self, group, dataset, queries: Union[str, list], **options):
        """
        Executes Data Analysis Expressions (DAX) queries against the provided 
        workspace (group) and dataset.

        Parameters
        ----------
        `group`: `Union[str, Group]`
            Group Id or `Group` object where the supplied Dataset resides.
        `dataset` : `Union[str, Dataset]`
            Dataset Id or `Dataset` object to execute the queries against.
        `queries` : `Union[str, list]`
            A single `str` query or `list` of queries. 
            
            If providing multiple queries, this should be provided as a list 
            of dicts in the following form:

            ```
            queries=[
                {"query": "query 1 text"},
                {"query": "query 2 text"}
            ]
            ```

        Returns
        -------
        `dict`
            Results of the executed query.

        Raises
        ------
        `ValueError`
            If unsupported execution options are supplied.
        `HTTPError`
            If the Rest API returns a status code not equal to 200.
        """

        supported_options = ["impersonated_user_name", "serializer_settings"]

        for k in options.keys():
            if k not in supported_options:
                raise ValueError(f"Unsupported option supplied: {k}. Supported options are: {supported_options}")
        
        if isinstance(group, Group):
            group_id = group.id
        else:
            group_id = group

        if isinstance(dataset, Dataset):
            dataset_id = dataset.id
        else:
            dataset_id = dataset
        
        if isinstance(queries, str):
            query_list = [{"query": queries}]
        else:
            query_list = queries
        
        payload = {"queries": query_list}
        payload.update({to_camel_case(k):v for k,v in options.items()})

        resource = f"https://api.powerbi.com/v1.0/myorg/groups/{group_id}/datasets/{dataset_id}/executeQueries"
        response = self.client.session.post(resource, json=payload)

        if response.status_code != 200:
            raise HTTPError(f"Encountered problem executing query. Response details: {response}")
        
        return response.json()
    
    def update_parameters(self, dataset, update_details:list[dict]):
        """
        Updates the parameters values for the specified dataset from My 
        workspace.

        Parameters
        ----------
        `dataset` : `Union[str, Dataset]`
            Dataset Id or `Dataset` object to update the parameters for.
        `update_details` : `list[dict]`
            A list of dataset parameters to update. e.g.,
        
            ```
            update_details = [
                {
                "name": "DatabaseName",
                "newValue": "NewDB"
                },
                {
                "name": "MaxId",
                "newValue": "5678"
                }
            ]
            ```

        Raises
        ------
        `ValueError`
            If `update_details` is an empty list.
        `HTTPError`
            If api response code is not equal to 200 (OK).
        """

        if isinstance(dataset, Dataset):
            dataset_id = dataset.id
        else:
            dataset_id = dataset
        
        if not update_details:
            raise ValueError("Update details is an empty list. Please provide update_details.")
        
        payload = {"updateDetails": update_details}

        resource = f"https://api.powerbi.com/v1.0/myorg/datasets/{dataset_id}/Default.UpdateParameters"
        response = self.client.session.post(resource, json=payload)

        if response.status_code != 200:
            raise HTTPError(f"Encountered updating parameters. Response details: {response}")
    
    def update_parameters_in_group(self, group, dataset, update_details:list[dict]):
        """
        Updates the parameters values for the specified dataset from the 
        specified workspace.

        Parameters
        ----------
        `group`: `Union[str, Group]`
            Group Id or `Group` object where the supplied Dataset resides.
        `dataset` : `Union[str, Dataset]`
            Dataset Id or `Dataset` object to update the parameters for.
        `update_details` : `list[dict]`
            A list of dataset parameters to update. e.g.,
        
            ```
            update_details = [
                {
                "name": "DatabaseName",
                "newValue": "NewDB"
                },
                {
                "name": "MaxId",
                "newValue": "5678"
                }
            ]
            ```

        Raises
        ------
        `ValueError`
            If `update_details` is an empty list.
        `HTTPError`
            If api response code is not equal to 200 (OK).
        """

        if isinstance(group, Group):
            group_id = group.id
        else:
            group_id = group

        if isinstance(dataset, Dataset):
            dataset_id = dataset.id
        else:
            dataset_id = dataset
        
        if not update_details:
            raise ValueError("Update details is an empty list. Please provide update_details.")
        
        payload = {"updateDetails": update_details}

        resource = f"https://api.powerbi.com/v1.0/myorg/groups/{group_id}/datasets/{dataset_id}/Default.UpdateParameters"
        response = self.client.session.post(resource, json=payload)

        if response.status_code != 200:
            raise HTTPError(f"Encountered updating parameters. Response details: {response}")
    
    def update_refresh_schedule(
            self,
            dataset,
            notify_option:str=None, 
            enabled:bool=None, 
            days:list[str]=None, 
            times:list[str]=None, 
            local_time_zone_id:str=None,
            ):
        """
        Updates the refresh schedule for the specified dataset from My 
        workspace.

        A request that disables the refresh schedule should contain no 
        other changes.

        At least one day must be specified. If no times are specified, 
        then Power BI will use a default single time per day.

        Parameters
        ----------
        `dataset` : `Union[str, Dataset]`
            Dataset or `Dataset` object to update the refresh schedule 
            for.
        `notify_option` : `str`, optional
            The notification option on termination of a scheduled refresh. 
            Service principals only support the `NoNotification` value. 
            Example values: `"MailOnFailure"`, `"NoNotification"`.
        `enabled` : `bool`, optional
            Whether the refresh is enabled.
        `days` : `list[str]`, optional
            The days on which to execute the refresh, e.g., `["Monday", "Tuesday"]`, etc.
        `times` : `list[str]`, optional
            The times of day to execute the refresh, e.g., `["07:00", "16:00"]`.
        `local_time_zone_id` : str, optional
            The ID of the time zone to use, e.g., `"UTC"`.

        Raises
        ------
        `ValueError`
            If no options are provided.
        `HTTPError`
            If the api response status code is not equal to 200.
        """

        if isinstance(dataset, Dataset):
            dataset_id = dataset.id
        else:
            dataset_id = dataset
        
        options = {
            "notifyOption": notify_option,
            "enabled": enabled,
            "days": days,
            "times": times,
            "localTimeZoneId": local_time_zone_id
        }
        prepared_options = {k:v for k,v in options.items() if v is not None}

        if not prepared_options:
            raise ValueError("No options were provided. A request to update a refresh schedule must contain an option to be set.")

        payload = {"value": prepared_options}
        
        resource = f"https://api.powerbi.com/v1.0/myorg/datasets/{dataset_id}/refreshSchedule"
        response = self.client.session.patch(resource, json=payload)

        if response.status_code != 200:
            raise HTTPError(f"Encountered problem updating direct query refresh schedule. Response details: {response.json()}")
    
    def update_refresh_schedule_in_group(self, group, dataset, **options):
        supported_options = ["enabled", "days", "frequency", "local_time_zone_id", "times"]

        for k in options.keys():
            if k not in supported_options:
                raise ValueError(f"Unsupported option supplied: {k}. Supported options are: {supported_options}")
        
        payload = {"value": {to_camel_case(k):v for k,v in options.items()}}
        
        if isinstance(group, Group):
            group_id = group.id
        else:
            group_id = group

        if isinstance(dataset, Dataset):
            dataset_id = dataset.id
        else:
            dataset_id = dataset
        
        resource = f"https://api.powerbi.com/v1.0/myorg/groups/{group_id}/datasets/{dataset_id}/refreshSchedule"
        response = self.client.session.patch(resource, json=payload)

        if response.status_code != 200:
            raise HTTPError(f"Encountered problem updating refresh schedule. Response details: {response}")