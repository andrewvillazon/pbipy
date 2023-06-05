import pytest
from requests import HTTPError
import responses

from pbipy.models import Dataset, DatasetRefreshDetail, DatasetUserAccess, Gateway, MashupParameter


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
def test_get_refresh_history_in_group(powerbi,get_refresh_history_in_group_failed):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/groups/f089354e-8366-4e18-aea3-4cb4a3a50b48/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229/refreshes?$top=1",
        body=get_refresh_history_in_group_failed,
        content_type="application/json",
    )

    refresh_history = powerbi.datasets.get_refresh_history_in_group("f089354e-8366-4e18-aea3-4cb4a3a50b48", "cfafbeb1-8037-4d0c-896e-a46fb27ff229", top=1)

    assert isinstance(refresh_history, list)
    assert len(refresh_history) == 1
    assert refresh_history[0].status == "Failed"


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


@responses.activate
def test_get_direct_query_refresh_schedule_with_dataset_id(powerbi, get_direct_query_refresh_schedule):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229/directQueryRefreshSchedule",
        body=get_direct_query_refresh_schedule,
        content_type="application/json"
    )

    dataset_id = "cfafbeb1-8037-4d0c-896e-a46fb27ff229"
    schedule=powerbi.datasets.get_direct_query_refresh_schedule(dataset_id)

    assert isinstance(schedule.days, list)
    assert len(schedule.days) == 3
    assert isinstance(schedule.times, list)
    assert len(schedule.times) == 4
    assert schedule.local_time_zone_id == "UTC"
    assert schedule.days[0] == "Sunday"


@responses.activate
def test_get_direct_query_refresh_schedule_with_dataset_object(powerbi, dataset ,get_direct_query_refresh_schedule):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229/directQueryRefreshSchedule",
        body=get_direct_query_refresh_schedule,
        content_type="application/json"
    )

    schedule=powerbi.datasets.get_direct_query_refresh_schedule(dataset)

    assert isinstance(schedule.days, list)
    assert len(schedule.days) == 3
    assert isinstance(schedule.times, list)
    assert len(schedule.times) == 4
    assert schedule.local_time_zone_id == "UTC"
    assert schedule.days[0] == "Sunday"


@responses.activate
def test_get_direct_query_refresh_schedule_in_group_from_ids(powerbi, get_direct_query_refresh_schedule):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/groups/f089354e-8366-4e18-aea3-4cb4a3a50b48/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229/directQueryRefreshSchedule",
        body=get_direct_query_refresh_schedule,
        content_type="application/json"
    )

    group_id = "f089354e-8366-4e18-aea3-4cb4a3a50b48"
    dataset_id = "cfafbeb1-8037-4d0c-896e-a46fb27ff229"

    schedule = powerbi.datasets.get_direct_query_refresh_schedule_in_group(group_id, dataset_id)

    assert isinstance(schedule.days, list)
    assert len(schedule.days) == 3
    assert isinstance(schedule.times, list)
    assert len(schedule.times) == 4
    assert schedule.local_time_zone_id == "UTC"
    assert schedule.days[0] == "Sunday"


@responses.activate
def test_get_direct_query_refresh_schedule_in_group_from_objects(powerbi, group, dataset, get_direct_query_refresh_schedule):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/groups/3d9b93c6-7b6d-4801-a491-1738910904fd/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229/directQueryRefreshSchedule",
        body=get_direct_query_refresh_schedule,
        content_type="application/json"
    )

    schedule = powerbi.datasets.get_direct_query_refresh_schedule_in_group(group, dataset)

    assert isinstance(schedule.days, list)
    assert len(schedule.days) == 3
    assert isinstance(schedule.times, list)
    assert len(schedule.times) == 4
    assert schedule.local_time_zone_id == "UTC"
    assert schedule.days[0] == "Sunday"


@responses.activate
def test_get_parameters_from_dataset_id(powerbi, get_parameters):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229/parameters",
        body=get_parameters,
        content_type="application/json"
    )

    dataset_id = "cfafbeb1-8037-4d0c-896e-a46fb27ff229"

    parameters = powerbi.datasets.get_parameters(dataset_id)

    assert isinstance(parameters, list)
    assert isinstance(parameters[0], MashupParameter)
    assert parameters[3].is_required
    assert len(parameters) == 6
    assert parameters[2].type == "DateTime"
    assert parameters[2].name == "FromDate"


@responses.activate
def test_get_parameters_from_dataset_object(powerbi, get_parameters, dataset):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229/parameters",
        body=get_parameters,
        content_type="application/json"
    )

    parameters = powerbi.datasets.get_parameters(dataset)

    assert isinstance(parameters, list)
    assert isinstance(parameters[0], MashupParameter)
    assert parameters[3].is_required
    assert len(parameters) == 6
    assert parameters[2].type == "DateTime"
    assert parameters[2].name == "FromDate"


@responses.activate
def test_get_parameters_in_group_from_group_object_and_dataset_object(powerbi, get_parameters, group_from_raw, dataset_from_raw):
    responses.get(
        f"https://api.powerbi.com/v1.0/myorg/groups/{group_from_raw.id}/datasets/{dataset_from_raw.id}/parameters",
        body=get_parameters,
        content_type="application/json",
    )

    parameters = powerbi.datasets.get_parameters_in_group(group_from_raw, dataset_from_raw)

    assert isinstance(parameters, list)
    assert len(parameters) == 6
    assert all(isinstance(parameter, MashupParameter) for parameter in parameters)


@responses.activate
def test_get_parameters_in_group_from_group_id_and_dataset_id(powerbi, get_parameters, group_from_raw, dataset_from_raw):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/groups/f089354e-8366-4e18-aea3-4cb4a3a50b48/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229/parameters",
        body=get_parameters,
        content_type="application/json",
    )

    parameters = powerbi.datasets.get_parameters_in_group("f089354e-8366-4e18-aea3-4cb4a3a50b48", "cfafbeb1-8037-4d0c-896e-a46fb27ff229")

    assert isinstance(parameters, list)
    assert len(parameters) == 6
    assert all(isinstance(parameter, MashupParameter) for parameter in parameters)


def test_get_refresh_history_raises_type_error_on_not_refreshable_dataset(
    powerbi, dataset_not_refreshable
):
    with pytest.raises(TypeError):
        powerbi.datasets.get_refresh_history(dataset_not_refreshable)


@responses.activate
def test_discover_gateways_using_dataset_id(powerbi, discover_gateways):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229/Default.DiscoverGateways",
        body=discover_gateways,
        content_type="application/json",
    )

    gateways = powerbi.datasets.discover_gateways("cfafbeb1-8037-4d0c-896e-a46fb27ff229")

    assert isinstance(gateways, list)
    assert len(gateways) == 2
    assert all(isinstance(gateway, Gateway) for gateway in gateways)


@responses.activate
def test_discover_gateways_using_dataset(powerbi, discover_gateways, dataset_from_raw):
    responses.get(
        f"https://api.powerbi.com/v1.0/myorg/datasets/{dataset_from_raw.id}/Default.DiscoverGateways",
        body=discover_gateways,
        content_type="application/json",
    )

    gateways = powerbi.datasets.discover_gateways(dataset_from_raw)

    assert isinstance(gateways, list)
    assert len(gateways) == 2
    assert all(isinstance(gateway, Gateway) for gateway in gateways)


@responses.activate
def test_discover_gateways_no_gateways_using_dataset_id(powerbi, discover_gateways_no_gateways, dataset_from_raw):
    responses.get(
        f"https://api.powerbi.com/v1.0/myorg/datasets/{dataset_from_raw.id}/Default.DiscoverGateways",
        body=discover_gateways_no_gateways,
        content_type="application/json",
    )

    gateways = powerbi.datasets.discover_gateways(dataset_from_raw)

    assert isinstance(gateways, list)
    assert len(gateways) == 0


@responses.activate
def test_cancel_refresh(powerbi):
    delete_response = responses.delete(
        "https://api.powerbi.com/v1.0/myorg/datasets/f7fc6510-e151-42a3-850b-d0805a391db0/refreshes/87f31ef7-1e3a-4006-9b0b-191693e79e9e"
        ,status=200
    )

    powerbi.datasets.cancel_refresh("f7fc6510-e151-42a3-850b-d0805a391db0", "87f31ef7-1e3a-4006-9b0b-191693e79e9e")

    assert delete_response.call_count == 1


@responses.activate
def test_cancel_refresh_raises_error(powerbi):
    responses.delete(
        "https://api.powerbi.com/v1.0/myorg/datasets/f7fc6510-e151-42a3-850b-d0805a391db0/refreshes/87f31ef7-1e3a-4006-9b0b-191693e79e9e"
        ,status=404
    )

    with pytest.raises(HTTPError):
        powerbi.datasets.cancel_refresh("f7fc6510-e151-42a3-850b-d0805a391db0", "87f31ef7-1e3a-4006-9b0b-191693e79e9e")


@responses.activate
def test_cancel_refresh_in_group(powerbi):
    delete_response = responses.delete(
        "https://api.powerbi.com/v1.0/myorg/groups/fdb91b8f-0a9b-44c1-b6c0-0cb185c6ebfb/datasets/f7fc6510-e151-42a3-850b-d0805a391db0/refreshes/87f31ef7-1e3a-4006-9b0b-191693e79e9e"
        ,status=200
    )

    powerbi.datasets.cancel_refresh_in_group("f7fc6510-e151-42a3-850b-d0805a391db0", "87f31ef7-1e3a-4006-9b0b-191693e79e9e", "fdb91b8f-0a9b-44c1-b6c0-0cb185c6ebfb")

    assert delete_response.call_count == 1


@responses.activate
def test_cancel_refresh_in_group_raises(powerbi):
    responses.delete(
        "https://api.powerbi.com/v1.0/myorg/groups/fdb91b8f-0a9b-44c1-b6c0-0cb185c6ebfb/datasets/f7fc6510-e151-42a3-850b-d0805a391db0/refreshes/87f31ef7-1e3a-4006-9b0b-191693e79e9e"
        ,status=301
    )

    with pytest.raises(HTTPError):
        powerbi.datasets.cancel_refresh_in_group("f7fc6510-e151-42a3-850b-d0805a391db0", "87f31ef7-1e3a-4006-9b0b-191693e79e9e", "fdb91b8f-0a9b-44c1-b6c0-0cb185c6ebfb")


@responses.activate
def test_delete_dataset_using_dataset_object(powerbi, dataset_from_raw):
    delete_response = responses.delete(
        "https://api.powerbi.com/v1.0/myorg/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229"
        ,status=200
    )

    powerbi.datasets.delete_dataset(dataset_from_raw)

    assert delete_response.call_count == 1


@responses.activate
def test_delete_dataset_using_dataset_object_raises(powerbi, dataset_from_raw):
    responses.delete(
        "https://api.powerbi.com/v1.0/myorg/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229"
        ,status=501
    )

    with pytest.raises(HTTPError):
        powerbi.datasets.delete_dataset(dataset_from_raw)


@responses.activate
def test_delete_dataset_in_group(powerbi):
    delete_response = responses.delete(
        "https://api.powerbi.com/v1.0/myorg/groups/f089354e-8366-4e18-aea3-4cb4a3a50b48/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229"
        ,status=200
    )

    powerbi.datasets.delete_dataset_in_group("cfafbeb1-8037-4d0c-896e-a46fb27ff229", "f089354e-8366-4e18-aea3-4cb4a3a50b48")

    assert delete_response.call_count == 1


@responses.activate
def test_delete_dataset_in_group_raises(powerbi):
    responses.delete(
        "https://api.powerbi.com/v1.0/myorg/groups/f089354e-8366-4e18-aea3-4cb4a3a50b48/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229"
        ,status=501
    )

    with pytest.raises(HTTPError):
        powerbi.datasets.delete_dataset_in_group("cfafbeb1-8037-4d0c-896e-a46fb27ff229", "f089354e-8366-4e18-aea3-4cb4a3a50b48")


@responses.activate
def test_get_refresh_execution_details_using_dataset_object_and_refresh_id(powerbi, get_refresh_execution_details, dataset_from_raw):
    responses.get(
        f"https://api.powerbi.com/v1.0/myorg/datasets/{dataset_from_raw.id}/refreshes/87f31ef7-1e3a-4006-9b0b-191693e79e9e",
        body=get_refresh_execution_details,
        content_type="application/json",
    )

    dataset_refresh_detail = powerbi.datasets.get_refresh_execution_details(dataset_from_raw, "87f31ef7-1e3a-4006-9b0b-191693e79e9e")

    assert isinstance(dataset_refresh_detail, DatasetRefreshDetail)


@responses.activate
def test_get_refresh_execution_details_in_group(powerbi, get_refresh_execution_details):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/groups/fdb91b8f-0a9b-44c1-b6c0-0cb185c6ebfb/datasets/f7fc6510-e151-42a3-850b-d0805a391db0/refreshes/87f31ef7-1e3a-4006-9b0b-191693e79e9e",
        body=get_refresh_execution_details,
        content_type="application/json",
    )

    dataset_refresh_detail = powerbi.datasets.get_refresh_execution_details_in_group("f7fc6510-e151-42a3-850b-d0805a391db0", "fdb91b8f-0a9b-44c1-b6c0-0cb185c6ebfb", "87f31ef7-1e3a-4006-9b0b-191693e79e9e")

    assert isinstance(dataset_refresh_detail, DatasetRefreshDetail)
