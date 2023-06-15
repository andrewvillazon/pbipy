import pytest
import requests
import responses
from requests.exceptions import HTTPError
from responses import matchers

from pbipy.resources import Dataset


@responses.activate
def test_get_dataset_calls_correct_get_dataset_url(powerbi, get_dataset):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229",
        body=get_dataset,
        content_type="application/json",
    )

    powerbi.get_dataset("cfafbeb1-8037-4d0c-896e-a46fb27ff229")


@responses.activate
def test_get_dataset_calls_correct_get_dataset_in_group_url(powerbi, get_dataset):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/groups/f089354e-8366-4e18-aea3-4cb4a3a50b48/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229",
        body=get_dataset,
        content_type="application/json",
    )

    powerbi.get_dataset(
        "cfafbeb1-8037-4d0c-896e-a46fb27ff229",
        group="f089354e-8366-4e18-aea3-4cb4a3a50b48",
    )


@responses.activate
def test_get_dataset_properties_are_set(powerbi, get_dataset):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229",
        body=get_dataset,
        content_type="application/json",
    )

    dataset = powerbi.get_dataset("cfafbeb1-8037-4d0c-896e-a46fb27ff229")

    assert dataset.id == "cfafbeb1-8037-4d0c-896e-a46fb27ff229"
    assert dataset.name == "SalesMarketing"
    assert dataset.add_rows_api_enabled == False
    assert dataset.configured_by == "john@contoso.com"
    assert dataset.group_id == None
    assert dataset.is_refreshable == True


@responses.activate
def test_get_dataset_group_property_is_set(powerbi, get_dataset):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/groups/f089354e-8366-4e18-aea3-4cb4a3a50b48/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229",
        body=get_dataset,
        content_type="application/json",
    )

    dataset = powerbi.get_dataset(
        "cfafbeb1-8037-4d0c-896e-a46fb27ff229",
        group="f089354e-8366-4e18-aea3-4cb4a3a50b48",
    )

    assert dataset.group_id == "f089354e-8366-4e18-aea3-4cb4a3a50b48"


@responses.activate
def test_get_datasets_calls_correct_get_datasets_url(powerbi, get_datasets):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/datasets",
        body=get_datasets,
        content_type="application/json",
    )

    powerbi.get_datasets()


@responses.activate
def test_get_datasets_calls_correct_get_datasets_in_group_url(powerbi, get_datasets):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/groups/f089354e-8366-4e18-aea3-4cb4a3a50b48/datasets",
        body=get_datasets,
        content_type="application/json",
    )

    powerbi.get_datasets(group="f089354e-8366-4e18-aea3-4cb4a3a50b48")


@responses.activate
def test_get_datasets_sets_group_property(powerbi, get_datasets):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/groups/f089354e-8366-4e18-aea3-4cb4a3a50b48/datasets",
        body=get_datasets,
        content_type="application/json",
    )

    datasets = powerbi.get_datasets(group="f089354e-8366-4e18-aea3-4cb4a3a50b48")

    assert all(hasattr(dataset, "group_id") for dataset in datasets)
    assert all(
        getattr(dataset, "group_id") == "f089354e-8366-4e18-aea3-4cb4a3a50b48"
        for dataset in datasets
    )


@responses.activate
def test_get_datasets_sets_js_property(powerbi, get_datasets):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/groups/f089354e-8366-4e18-aea3-4cb4a3a50b48/datasets",
        body=get_datasets,
        content_type="application/json",
    )

    datasets = powerbi.get_datasets(group="f089354e-8366-4e18-aea3-4cb4a3a50b48")

    assert all(hasattr(dataset, "raw") for dataset in datasets)


@responses.activate
def test_delete_dataset_call(powerbi):
    responses.delete(
        "https://api.powerbi.com/v1.0/myorg/groups/f089354e-8366-4e18-aea3-4cb4a3a50b48/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229"
    )

    powerbi.delete_dataset(
        "cfafbeb1-8037-4d0c-896e-a46fb27ff229",
        group="f089354e-8366-4e18-aea3-4cb4a3a50b48",
    )


@responses.activate
def test_delete_dataset_raises_http_error(powerbi):
    responses.delete(
        "https://api.powerbi.com/v1.0/myorg/groups/f089354e-8366-4e18-aea3-4cb4a3a50b48/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229",
        status=400,
        body="{}",
    )

    with pytest.raises(HTTPError):
        powerbi.delete_dataset(
            "cfafbeb1-8037-4d0c-896e-a46fb27ff229",
            group="f089354e-8366-4e18-aea3-4cb4a3a50b48",
        )


@responses.activate
def test_get_refresh_history():
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/groups/f089354e-8366-4e18-aea3-4cb4a3a50b48/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229/refreshes?$top=2",
        body="""
        {
            "value": [
                {
                "refreshType": "ViaApi",
                "startTime": "2017-06-13T09:25:43.153Z",
                "endTime": "2017-06-13T09:31:43.153Z",
                "status": "Completed",
                "requestId": "9399bb89-25d1-44f8-8576-136d7e9014b1"
                }
            ]
        }
        """,
        content_type="application/json",
    )

    dataset = Dataset(
        id="cfafbeb1-8037-4d0c-896e-a46fb27ff229",
        group_id="f089354e-8366-4e18-aea3-4cb4a3a50b48",
        session=requests.Session(),
    )

    refresh_history = dataset.get_refresh_history(top=2)

    assert isinstance(refresh_history, list)
    assert all(isinstance(refresh, dict) for refresh in refresh_history)


@responses.activate
def test_get_refresh_history_calls_correct_url():
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/groups/f089354e-8366-4e18-aea3-4cb4a3a50b48/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229/refreshes?$top=2",
        body='{"value": []}',
        content_type="application/json",
    )

    dataset = Dataset(
        id="cfafbeb1-8037-4d0c-896e-a46fb27ff229",
        group_id="f089354e-8366-4e18-aea3-4cb4a3a50b48",
        session=requests.Session(),
    )

    dataset.get_refresh_history(top=2)


@responses.activate
def test_get_refresh_history_raises_http_error():
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229/refreshes",
        body='{"value": []}',
        content_type="application/json",
        status=400,
    )

    dataset = Dataset(
        id="cfafbeb1-8037-4d0c-896e-a46fb27ff229",
        session=requests.Session(),
    )

    with pytest.raises(HTTPError):
        dataset.get_refresh_history()


@responses.activate
def test_post_dataset_user_call():
    json_params = {
        "datasetUserAccessRight": "Read",
        "identifier": "john@contoso.com",
        "principalType": "User",
    }

    responses.post(
        "https://api.powerbi.com/v1.0/myorg/groups/f089354e-8366-4e18-aea3-4cb4a3a50b48/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229/users",
        match=[
            matchers.json_params_matcher(json_params),
        ],
    )

    dataset = Dataset(
        id="cfafbeb1-8037-4d0c-896e-a46fb27ff229",
        group_id="f089354e-8366-4e18-aea3-4cb4a3a50b48",
        session=requests.Session(),
    )

    dataset.post_dataset_user("john@contoso.com", "User", "Read")


@responses.activate
def test_post_dataset_raises_http_error():
    json_params = {
        "datasetUserAccessRight": "Read",
        "identifier": "john@contoso.com",
        "principalType": "User",
    }

    responses.post(
        "https://api.powerbi.com/v1.0/myorg/groups/f089354e-8366-4e18-aea3-4cb4a3a50b48/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229/users",
        match=[
            matchers.json_params_matcher(json_params),
        ],
        status=400,
        json={
            "error": {
                "code": "InvalidRequest",
                "message": "Parameter identifier is missing or invalid",
            }
        },
    )

    dataset = Dataset(
        id="cfafbeb1-8037-4d0c-896e-a46fb27ff229",
        group_id="f089354e-8366-4e18-aea3-4cb4a3a50b48",
        session=requests.Session(),
    )

    with pytest.raises(HTTPError):
        dataset.post_dataset_user("john@contoso.com", "User", "Read")


# TODO: Tests for request_mixin.delete()
# TODO: Tests for request_mixin.get()


@responses.activate
def test_bind_to_gateway_with_data_source_object_ids():
    json_params = {
        "gatewayObjectId": "1f69e798-5852-4fdd-ab01-33bb14b6e934",
        "datasourceObjectIds": [
            "dc2f2dac-e5e2-4c37-af76-2a0bc10f16cb",
            "3bfe5d33-ab7d-4d24-b0b5-e2bb8eb01cf5",
        ],
    }

    responses.post(
        "https://api.powerbi.com/v1.0/myorg/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229/Default.BindToGateway",
        match=[matchers.json_params_matcher(json_params)],
    )

    dataset = Dataset(
        id="cfafbeb1-8037-4d0c-896e-a46fb27ff229",
        session=requests.Session(),
    )

    datasource_object_ids = [
        "dc2f2dac-e5e2-4c37-af76-2a0bc10f16cb",
        "3bfe5d33-ab7d-4d24-b0b5-e2bb8eb01cf5",
    ]

    dataset.bind_to_gateway(
        gateway_object_id="1f69e798-5852-4fdd-ab01-33bb14b6e934",
        datasource_object_ids=datasource_object_ids,
    )


@responses.activate
def test_bind_to_gateway_without_data_source_object_ids():
    json_params = {
        "gatewayObjectId": "1f69e798-5852-4fdd-ab01-33bb14b6e934",
    }

    responses.post(
        "https://api.powerbi.com/v1.0/myorg/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229/Default.BindToGateway",
        match=[matchers.json_params_matcher(json_params)],
    )

    dataset = Dataset(
        id="cfafbeb1-8037-4d0c-896e-a46fb27ff229",
        session=requests.Session(),
    )

    dataset.bind_to_gateway(
        gateway_object_id="1f69e798-5852-4fdd-ab01-33bb14b6e934"
    )
