import pytest
import responses

from pbipy.models import Dataset, DatasetUserAccess


@responses.activate
def test_get_dataset(powerbi, get_dataset):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229",
        body=get_dataset,
        content_type="application/json",
    )

    dataset = powerbi.datasets.get_dataset("cfafbeb1-8037-4d0c-896e-a46fb27ff229")

    assert dataset.id == "cfafbeb1-8037-4d0c-896e-a46fb27ff229"
    assert dataset.name == "SalesMarketing"
    assert not dataset.add_rows_api_enabled
    assert dataset.is_refreshable


@responses.activate
def test_get_dataset_in_group_using_group_id(powerbi, get_dataset_in_group):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/groups/f089354e-8366-4e18-aea3-4cb4a3a50b48/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229",
        body=get_dataset_in_group,
        content_type="application/json",
    )

    dataset = powerbi.datasets.get_dataset_in_group(
        "f089354e-8366-4e18-aea3-4cb4a3a50b48", "cfafbeb1-8037-4d0c-896e-a46fb27ff229"
    )

    assert isinstance(dataset, Dataset)
    assert dataset.id == "cfafbeb1-8037-4d0c-896e-a46fb27ff229"
    assert dataset.name == "SalesMarketing"
    assert dataset.configured_by == "john@contoso.com"
    assert dataset.is_refreshable
    assert not dataset.is_effective_identity_required
    assert not dataset.is_effective_identity_roles_required
    assert not dataset.is_on_prem_gateway_required

    # Keys not in the API response are set to None
    assert dataset.target_storage_mode == None
    assert dataset.users == None


@responses.activate
def test_get_dataset_in_group_using_group_object(powerbi, group, get_dataset_in_group):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/groups/3d9b93c6-7b6d-4801-a491-1738910904fd/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229",
        body=get_dataset_in_group,
        content_type="application/json",
    )

    dataset = powerbi.datasets.get_dataset_in_group(
        group, "cfafbeb1-8037-4d0c-896e-a46fb27ff229"
    )

    assert isinstance(dataset, Dataset)
    assert dataset.id == "cfafbeb1-8037-4d0c-896e-a46fb27ff229"
    assert dataset.name == "SalesMarketing"
    assert dataset.configured_by == "john@contoso.com"
    assert dataset.is_refreshable
    assert not dataset.is_effective_identity_required
    assert not dataset.is_effective_identity_roles_required
    assert not dataset.is_on_prem_gateway_required
    assert len(dataset.upstream_datasets) == 0

    # Keys not in the API response are set to None
    assert dataset.target_storage_mode == None
    assert dataset.users == None


@responses.activate
def test_get_datasets_in_group_using_group_id(powerbi, get_datasets_in_group):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/groups/f089354e-8366-4e18-aea3-4cb4a3a50b48/datasets",
        body=get_datasets_in_group,
        content_type="application/json",
    )

    datasets = powerbi.datasets.get_datasets_in_group(
        "f089354e-8366-4e18-aea3-4cb4a3a50b48"
    )

    assert len(datasets) == 1
    assert datasets[0].id == "cfafbeb1-8037-4d0c-896e-a46fb27ff229"
    assert hasattr(datasets[0], "is_effective_identity_roles_required")
    assert not datasets[0].is_effective_identity_roles_required


@responses.activate
def test_get_datasets_in_group_using_group_object(
    powerbi, group, get_datasets_in_group
):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/groups/3d9b93c6-7b6d-4801-a491-1738910904fd/datasets",
        body=get_datasets_in_group,
        content_type="application/json",
    )

    datasets = powerbi.datasets.get_datasets_in_group(group)

    assert len(datasets) == 1
    assert datasets[0].id == "cfafbeb1-8037-4d0c-896e-a46fb27ff229"
    assert hasattr(datasets[0], "is_effective_identity_roles_required")
    assert not datasets[0].is_effective_identity_roles_required


@responses.activate
def test_get_refresh_history_from_dataset_object(powerbi, dataset, get_refresh_history):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229/refreshes",
        body=get_refresh_history,
        content_type="application/json",
    )

    refresh_history = powerbi.datasets.get_refresh_history(dataset)

    assert len(refresh_history) == 2
    assert not refresh_history[0].service_exception_json
    assert refresh_history[1].service_exception_json


@responses.activate
def test_get_refresh_history_from_dataset_id(powerbi, get_dataset, get_refresh_history):
    """Test get_refresh_history retrieves the Dataset details before retrieving the refresh history."""

    dataset_get_request = responses.get(
        "https://api.powerbi.com/v1.0/myorg/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229",
        body=get_dataset,
        content_type="application/json",
    )

    responses.get(
        "https://api.powerbi.com/v1.0/myorg/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229/refreshes",
        body=get_refresh_history,
        content_type="application/json",
    )

    dataset_id = "cfafbeb1-8037-4d0c-896e-a46fb27ff229"

    refresh_history = powerbi.datasets.get_refresh_history(dataset_id)

    assert dataset_get_request.call_count == 1
    assert len(refresh_history) == 2
    assert not refresh_history[0].service_exception_json
    assert refresh_history[1].service_exception_json


@responses.activate
def test_get_dataset_to_dataflow_links_in_group_from_group_id(
    powerbi, get_dataset_to_dataflow_links_in_group
):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/groups/f089354e-8366-4e18-aea3-4cb4a3a50b48/datasets/upstreamDataflows",
        body=get_dataset_to_dataflow_links_in_group,
        content_type="application/json",
    )

    group_id = "f089354e-8366-4e18-aea3-4cb4a3a50b48"
    dataflow_links = powerbi.datasets.get_dataset_to_dataflow_links_in_group(group_id)

    assert len(dataflow_links) == 1
    assert hasattr(dataflow_links[0], "workspace_object_id")
    assert (
        dataflow_links[0].workspace_object_id == "f089354e-8366-4e18-aea3-4cb4a3a50b48"
    )


@responses.activate
def test_get_dataset_to_dataflow_links_in_group_from_group_object(powerbi, group, get_dataset_to_dataflow_links_in_group):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/groups/3d9b93c6-7b6d-4801-a491-1738910904fd/datasets/upstreamDataflows",
        body=get_dataset_to_dataflow_links_in_group,
        content_type="application/json",
    )

    dataflow_links = powerbi.datasets.get_dataset_to_dataflow_links_in_group(group)

    assert len(dataflow_links) == 1
    assert hasattr(dataflow_links[0], "workspace_object_id")
    assert (
        dataflow_links[0].workspace_object_id == "f089354e-8366-4e18-aea3-4cb4a3a50b48"
    )


@responses.activate
def test_get_dataset_users_from_dataset_id(powerbi, get_dataset_users):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229/users",
        body=get_dataset_users,
        content_type="application/json",
    )

    dataset_id = "cfafbeb1-8037-4d0c-896e-a46fb27ff229"
    dataset_users = powerbi.datasets.get_dataset_users(dataset_id)

    assert len(dataset_users) == 3
    assert hasattr(dataset_users[0], "identifier")
    assert hasattr(dataset_users[1], "principal_type")
    assert hasattr(dataset_users[2], "dataset_user_access_right")
    assert isinstance(dataset_users[1], DatasetUserAccess)
    assert dataset_users[0].identifier == "john@contoso.com"
    assert dataset_users[1].principal_type == "Group"
    assert dataset_users[2].dataset_user_access_right == "ReadWriteReshareExplore"


@responses.activate
def test_get_dataset_users_from_dataset_object(powerbi, dataset, get_dataset_users):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229/users",
        body=get_dataset_users,
        content_type="application/json",
    )

    dataset_users = powerbi.datasets.get_dataset_users(dataset)

    assert len(dataset_users) == 3
    assert hasattr(dataset_users[0], "identifier")
    assert hasattr(dataset_users[1], "principal_type")
    assert hasattr(dataset_users[2], "dataset_user_access_right")
    assert isinstance(dataset_users[1], DatasetUserAccess)
    assert dataset_users[0].identifier == "john@contoso.com"
    assert dataset_users[1].principal_type == "Group"
    assert dataset_users[2].dataset_user_access_right == "ReadWriteReshareExplore"


@responses.activate
def test_get_datasources_from_dataset_id(powerbi, get_datasources):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229/datasources",
        body=get_datasources,
        content_type="application/json"
    )

    dataset_id = "cfafbeb1-8037-4d0c-896e-a46fb27ff229"
    datasources = powerbi.datasets.get_datasources(dataset_id)

    assert isinstance(datasources, list)
    assert len(datasources) == 11
    assert isinstance(datasources[0].connection_details, dict)
    assert datasources[1].datasource_type == "AzureBlobs"
    assert any(datasource.datasource_type == "SharePointList" for datasource in datasources)
    assert getattr(datasources[0], "datasource_id")
    assert getattr(datasources[0], "gateway_id")
    assert getattr(datasources[0], "datasource_type")


@responses.activate
def test_get_datasources_from_dataset_object(powerbi, dataset, get_datasources):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229/datasources",
        body=get_datasources,
        content_type="application/json"
    )

    datasources = powerbi.datasets.get_datasources(dataset)

    assert isinstance(datasources, list)
    assert len(datasources) == 11
    assert isinstance(datasources[0].connection_details, dict)
    assert datasources[1].datasource_type == "AzureBlobs"
    assert any(datasource.datasource_type == "SharePointList" for datasource in datasources)
    assert getattr(datasources[0], "datasource_id")
    assert getattr(datasources[0], "gateway_id")
    assert getattr(datasources[0], "datasource_type")
    assert getattr(datasources[0], "connection_details")


@responses.activate
def test_get_datasources_in_group_from_ids(powerbi, get_datasources):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/groups/f089354e-8366-4e18-aea3-4cb4a3a50b48/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229/datasources",
        body=get_datasources,
        content_type="application/json"
    )

    group_id = "f089354e-8366-4e18-aea3-4cb4a3a50b48"
    dataset_id = "cfafbeb1-8037-4d0c-896e-a46fb27ff229"

    datasources = powerbi.datasets.get_datasources_in_group(group_id, dataset_id)

    assert isinstance(datasources, list)
    assert len(datasources) == 11
    assert isinstance(datasources[0].connection_details, dict)
    assert datasources[1].datasource_type == "AzureBlobs"
    assert any(datasource.datasource_type == "SharePointList" for datasource in datasources)
    assert getattr(datasources[0], "datasource_id")
    assert getattr(datasources[0], "gateway_id")
    assert getattr(datasources[0], "datasource_type")
    assert getattr(datasources[0], "connection_details")


@responses.activate
def test_get_datasources_in_group_from_objects(powerbi, get_datasources, group, dataset):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/groups/3d9b93c6-7b6d-4801-a491-1738910904fd/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229/datasources",
        body=get_datasources,
        content_type="application/json"
    )

    datasources = powerbi.datasets.get_datasources_in_group(group, dataset)

    assert isinstance(datasources, list)
    assert len(datasources) == 11
    assert isinstance(datasources[0].connection_details, dict)
    assert datasources[1].datasource_type == "AzureBlobs"
    assert any(datasource.datasource_type == "SharePointList" for datasource in datasources)
    assert getattr(datasources[0], "datasource_id")
    assert getattr(datasources[0], "gateway_id")
    assert getattr(datasources[0], "datasource_type")
    assert getattr(datasources[0], "connection_details")



def test_get_refresh_history_raises_type_error_on_not_refreshable_dataset(
    powerbi, dataset_not_refreshable
):
    with pytest.raises(TypeError):
        powerbi.datasets.get_refresh_history(dataset_not_refreshable)
