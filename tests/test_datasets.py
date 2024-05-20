import pytest
import requests
import responses
from requests.exceptions import HTTPError
from responses import matchers

from pbipy.datasets import Dataset, DatasetRefreshError


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

    refresh_history = dataset.refresh_history(top=2)

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

    dataset.refresh_history(top=2)


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
        dataset.refresh_history()


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

    dataset.add_user("john@contoso.com", "User", "Read")


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
        dataset.add_user("john@contoso.com", "User", "Read")


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

    dataset.bind_to_gateway(gateway_object_id="1f69e798-5852-4fdd-ab01-33bb14b6e934")


@responses.activate
def test_cancel_refresh():
    responses.delete(
        "https://api.powerbi.com/v1.0/myorg/groups/fdb91b8f-0a9b-44c1-b6c0-0cb185c6ebfb/datasets/f7fc6510-e151-42a3-850b-d0805a391db0/refreshes/87f31ef7-1e3a-4006-9b0b-191693e79e9e"
    )

    dataset = Dataset(
        id="f7fc6510-e151-42a3-850b-d0805a391db0",
        session=requests.Session(),
        group_id="fdb91b8f-0a9b-44c1-b6c0-0cb185c6ebfb",
    )

    dataset.cancel_refresh("87f31ef7-1e3a-4006-9b0b-191693e79e9e")


@responses.activate
def test_discover_gateways():
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229/Default.DiscoverGateways",
        body="""
        {
            "value": [
                {
                "id": "1f69e798-5852-4fdd-ab01-33bb14b6e934",
                "name": "ContosoGateway",
                "type": "Resource",
                "publicKey": {
                    "exponent": "AQAB",
                    "modulus": "o6j2....cLk="
                }
                }
            ]
        }
        """,
        content_type="application/json",
    )

    dataset = Dataset(
        id="cfafbeb1-8037-4d0c-896e-a46fb27ff229",
        session=requests.Session(),
    )

    gateways = dataset.discover_gateways()

    assert isinstance(gateways, list)
    assert all(isinstance(gateway, dict) for gateway in gateways)


@responses.activate
def test_discover_gateways_call():
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229/Default.DiscoverGateways",
        body='{"value": []}',
        content_type="application/json",
    )

    dataset = Dataset(
        id="cfafbeb1-8037-4d0c-896e-a46fb27ff229",
        session=requests.Session(),
    )
    dataset.discover_gateways()


@responses.activate
def test_execute_queries_call(execute_queries):
    json_params = {
        "queries": [
            {
                "query": "EVALUATE VALUES(MyTable)",
            },
        ],
        "impersonatedUserName": "someuser@mycompany.com",
    }

    responses.post(
        "https://api.powerbi.com/v1.0/myorg/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229/executeQueries",
        match=[
            matchers.json_params_matcher(json_params),
        ],
        body=execute_queries,
    )

    dataset = Dataset(
        id="cfafbeb1-8037-4d0c-896e-a46fb27ff229",
        session=requests.Session(),
    )

    query = "EVALUATE VALUES(MyTable)"

    dataset.execute_queries(
        query,
        impersonated_user_name="someuser@mycompany.com",
    )


@responses.activate
def test_execute_queries_call_multi_query(execute_queries):
    json_params = {
        "queries": [
            {
                "query": "EVALUATE VALUES(MyTable)",
            },
            {
                "query": "EVALUATE VALUES(MyTable)",
            },
        ],
        "impersonatedUserName": "someuser@mycompany.com",
    }

    responses.post(
        "https://api.powerbi.com/v1.0/myorg/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229/executeQueries",
        match=[
            matchers.json_params_matcher(json_params),
        ],
        body=execute_queries,
    )

    dataset = Dataset(
        id="cfafbeb1-8037-4d0c-896e-a46fb27ff229",
        session=requests.Session(),
    )

    queries = [
        "EVALUATE VALUES(MyTable)",
        "EVALUATE VALUES(MyTable)",
    ]

    dataset.execute_queries(
        queries,
        impersonated_user_name="someuser@mycompany.com",
    )


@responses.activate
def test_execute_queries_call_result(execute_queries):
    json_params = {
        "queries": [
            {
                "query": "EVALUATE VALUES(MyTable)",
            },
        ],
        "impersonatedUserName": "someuser@mycompany.com",
    }

    responses.post(
        "https://api.powerbi.com/v1.0/myorg/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229/executeQueries",
        match=[
            matchers.json_params_matcher(json_params),
        ],
        body=execute_queries,
    )

    dataset = Dataset(
        id="cfafbeb1-8037-4d0c-896e-a46fb27ff229",
        session=requests.Session(),
    )

    queries = "EVALUATE VALUES(MyTable)"

    result = dataset.execute_queries(
        queries,
        impersonated_user_name="someuser@mycompany.com",
    )

    assert isinstance(result, dict)
    assert "results" in result


@responses.activate
def test_users_call(get_dataset_users):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/groups/f089354e-8366-4e18-aea3-4cb4a3a50b48/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229/users",
        body=get_dataset_users,
        content_type="application/json",
    )

    dataset = Dataset(
        id="cfafbeb1-8037-4d0c-896e-a46fb27ff229",
        group_id="f089354e-8366-4e18-aea3-4cb4a3a50b48",
        session=requests.Session(),
    )

    dataset.users()


@responses.activate
def test_users_result(get_dataset_users):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/groups/f089354e-8366-4e18-aea3-4cb4a3a50b48/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229/users",
        body=get_dataset_users,
        content_type="application/json",
    )

    dataset = Dataset(
        id="cfafbeb1-8037-4d0c-896e-a46fb27ff229",
        group_id="f089354e-8366-4e18-aea3-4cb4a3a50b48",
        session=requests.Session(),
    )

    users = dataset.users()

    assert isinstance(users, list)
    assert len(users) == 3


@responses.activate
def test_datasources_call(get_datasources):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229/datasources",
        body=get_datasources,
        content_type="application/json",
    )

    dataset = Dataset(
        id="cfafbeb1-8037-4d0c-896e-a46fb27ff229",
        session=requests.Session(),
    )

    dataset.datasources()


@responses.activate
def test_datasources_result(get_datasources):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229/datasources",
        body=get_datasources,
        content_type="application/json",
    )

    dataset = Dataset(
        id="cfafbeb1-8037-4d0c-896e-a46fb27ff229",
        session=requests.Session(),
    )

    datasources = dataset.datasources()

    assert isinstance(datasources, list)
    assert len(datasources) == 3


@responses.activate
def test_refresh_schedule_call(get_refresh_schedule):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229/refreshSchedule",
        body=get_refresh_schedule,
        content_type="application/json",
    )

    dataset = Dataset(
        id="cfafbeb1-8037-4d0c-896e-a46fb27ff229",
        session=requests.Session(),
    )

    dataset.refresh_schedule()


@responses.activate
def test_refresh_schedule_result(get_refresh_schedule):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229/refreshSchedule",
        body=get_refresh_schedule,
        content_type="application/json",
    )

    dataset = Dataset(
        id="cfafbeb1-8037-4d0c-896e-a46fb27ff229",
        session=requests.Session(),
    )

    refresh_schedule = dataset.refresh_schedule()

    assert isinstance(refresh_schedule, dict)


@responses.activate
def test_refresh_schedule_direct_query_call(get_direct_query_refresh_schedule):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229/directQueryRefreshSchedule",
        body=get_direct_query_refresh_schedule,
        content_type="application/json",
    )

    dataset = Dataset(
        id="cfafbeb1-8037-4d0c-896e-a46fb27ff229",
        session=requests.Session(),
    )

    dataset.refresh_schedule(direct_query=True)


@responses.activate
def test_refresh_schedule_direct_query_result(get_direct_query_refresh_schedule):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229/directQueryRefreshSchedule",
        body=get_direct_query_refresh_schedule,
        content_type="application/json",
    )

    dataset = Dataset(
        id="cfafbeb1-8037-4d0c-896e-a46fb27ff229",
        session=requests.Session(),
    )

    refresh_schedule = dataset.refresh_schedule(direct_query=True)

    assert isinstance(refresh_schedule, dict)


@responses.activate
def test_parameters_call(get_parameters):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229/parameters",
        body=get_parameters,
        content_type="application/json",
    )

    dataset = Dataset(
        id="cfafbeb1-8037-4d0c-896e-a46fb27ff229",
        session=requests.Session(),
    )

    dataset.parameters()


@responses.activate
def test_parameters_result(get_parameters):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229/parameters",
        body=get_parameters,
        content_type="application/json",
    )

    dataset = Dataset(
        id="cfafbeb1-8037-4d0c-896e-a46fb27ff229",
        session=requests.Session(),
    )

    parameters = dataset.parameters()

    assert isinstance(parameters, list)
    assert all(isinstance(parameter, dict) for parameter in parameters)
    assert len(parameters) == 6


@responses.activate
def test_refresh_details_call(get_refresh_execution_details):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/datasets/f7fc6510-e151-42a3-850b-d0805a391db0/refreshes/87f31ef7-1e3a-4006-9b0b-191693e79e9e",
        body=get_refresh_execution_details,
        content_type="application/json",
    )

    dataset = Dataset(
        id="f7fc6510-e151-42a3-850b-d0805a391db0",
        session=requests.Session(),
    )

    dataset.refresh_details("87f31ef7-1e3a-4006-9b0b-191693e79e9e")


@responses.activate
def test_refresh_details_result(get_refresh_execution_details):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/datasets/f7fc6510-e151-42a3-850b-d0805a391db0/refreshes/87f31ef7-1e3a-4006-9b0b-191693e79e9e",
        body=get_refresh_execution_details,
        content_type="application/json",
    )

    dataset = Dataset(
        id="f7fc6510-e151-42a3-850b-d0805a391db0",
        session=requests.Session(),
    )

    refresh_detail = dataset.refresh_details("87f31ef7-1e3a-4006-9b0b-191693e79e9e")

    assert isinstance(refresh_detail, dict)
    assert len(refresh_detail["objects"]) == 18


@pytest.fixture
def sleepless(monkeypatch):
    """Patches time.sleep to make unit tests complete without delay."""

    import time

    def sleep(seconds):
        pass

    monkeypatch.setattr(time, "sleep", sleep)


@responses.activate
def test_refresh_and_wait_success(
    get_refresh_execution_details_in_progress,
    get_refresh_execution_details,
    sleepless,
):
    dataset_id = "cfafbeb1-8037-4d0c-896e-a46fb27ff229"
    request_id = "03f22bb5-2e98-4ae8-8113-329bec3987b1"

    dataset = Dataset(
        id=dataset_id,
        session=requests.Session(),
    )

    json_params = {"type": "Full"}

    responses.post(
        f"https://api.powerbi.com/v1.0/myorg/datasets/{dataset_id}/refreshes",
        match=[
            matchers.json_params_matcher(json_params),
        ],
        headers={"RequestId": request_id},
    )

    responses.get(
        f"https://api.powerbi.com/v1.0/myorg/datasets/{dataset_id}/refreshes/{request_id}",
        body=get_refresh_execution_details_in_progress,
        content_type="application/json",
    )

    responses.get(
        f"https://api.powerbi.com/v1.0/myorg/datasets/{dataset_id}/refreshes/{request_id}",
        body=get_refresh_execution_details,
        content_type="application/json",
    )

    dataset.refresh_and_wait(type="Full", check_interval=60)
    assert len(responses.calls) == 3


@responses.activate
def test_refresh_and_wait_success_longer(
    get_refresh_execution_details_in_progress,
    get_refresh_execution_details,
    sleepless,
):
    dataset_id = "cfafbeb1-8037-4d0c-896e-a46fb27ff229"
    request_id = "03f22bb5-2e98-4ae8-8113-329bec3987b1"

    dataset = Dataset(
        id=dataset_id,
        session=requests.Session(),
    )

    json_params = {"type": "Full", "retryCount": 3}

    responses.post(
        f"https://api.powerbi.com/v1.0/myorg/datasets/{dataset_id}/refreshes",
        match=[
            matchers.json_params_matcher(json_params),
        ],
        headers={"RequestId": request_id},
    )

    responses.get(
        f"https://api.powerbi.com/v1.0/myorg/datasets/{dataset_id}/refreshes/{request_id}",
        body=get_refresh_execution_details_in_progress,
        content_type="application/json",
    )

    responses.get(
        f"https://api.powerbi.com/v1.0/myorg/datasets/{dataset_id}/refreshes/{request_id}",
        body=get_refresh_execution_details_in_progress,
        content_type="application/json",
    )

    responses.get(
        f"https://api.powerbi.com/v1.0/myorg/datasets/{dataset_id}/refreshes/{request_id}",
        body=get_refresh_execution_details_in_progress,
        content_type="application/json",
    )

    responses.get(
        f"https://api.powerbi.com/v1.0/myorg/datasets/{dataset_id}/refreshes/{request_id}",
        body=get_refresh_execution_details,
        content_type="application/json",
    )

    dataset.refresh_and_wait(type="Full", retry_count=3)
    assert len(responses.calls) == 5


def test_refresh_and_wait_raises_ValueError():
    dataset_id = "cfafbeb1-8037-4d0c-896e-a46fb27ff229"

    dataset = Dataset(
        id=dataset_id,
        session=requests.Session(),
    )

    with pytest.raises(ValueError):
        dataset.refresh_and_wait()


@responses.activate
def test_refresh_and_wait_failed_raises_RefreshDatasetError(
    get_refresh_execution_details_in_progress,
    get_refresh_execution_details_failed,
    sleepless,
):
    dataset_id = "cfafbeb1-8037-4d0c-896e-a46fb27ff229"
    request_id = "03f22bb5-2e98-4ae8-8113-329bec3987b1"

    dataset = Dataset(
        id=dataset_id,
        session=requests.Session(),
    )

    json_params = {"type": "Full"}

    responses.post(
        f"https://api.powerbi.com/v1.0/myorg/datasets/{dataset_id}/refreshes",
        match=[
            matchers.json_params_matcher(json_params),
        ],
        headers={"RequestId": request_id},
    )

    responses.get(
        f"https://api.powerbi.com/v1.0/myorg/datasets/{dataset_id}/refreshes/{request_id}",
        body=get_refresh_execution_details_in_progress,
        content_type="application/json",
    )

    responses.get(
        f"https://api.powerbi.com/v1.0/myorg/datasets/{dataset_id}/refreshes/{request_id}",
        body=get_refresh_execution_details_failed,
        content_type="application/json",
    )

    with pytest.raises(DatasetRefreshError):
        dataset.refresh_and_wait(type="Full", check_interval=60)

    assert len(responses.calls) == 3


@responses.activate
def test_refresh_and_wait_cancelled_raises_RefreshDatasetError(
    get_refresh_execution_details_in_progress,
    get_refresh_execution_details_cancelled,
    sleepless,
):
    dataset_id = "cfafbeb1-8037-4d0c-896e-a46fb27ff229"
    request_id = "03f22bb5-2e98-4ae8-8113-329bec3987b1"

    dataset = Dataset(
        id=dataset_id,
        session=requests.Session(),
    )

    json_params = {"type": "Full"}

    responses.post(
        f"https://api.powerbi.com/v1.0/myorg/datasets/{dataset_id}/refreshes",
        match=[
            matchers.json_params_matcher(json_params),
        ],
        headers={"RequestId": request_id},
    )

    responses.get(
        f"https://api.powerbi.com/v1.0/myorg/datasets/{dataset_id}/refreshes/{request_id}",
        body=get_refresh_execution_details_in_progress,
        content_type="application/json",
    )

    responses.get(
        f"https://api.powerbi.com/v1.0/myorg/datasets/{dataset_id}/refreshes/{request_id}",
        body=get_refresh_execution_details_cancelled,
        content_type="application/json",
    )

    with pytest.raises(DatasetRefreshError):
        dataset.refresh_and_wait(type="Full", check_interval=60)

    assert len(responses.calls) == 3


@responses.activate
def test_update_user_call():
    json_params = {
        "datasetUserAccessRight": "Read",
        "identifier": "john@contoso.com",
        "principalType": "User",
    }

    responses.put(
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

    dataset.update_user("john@contoso.com", "User", "Read")


@responses.activate
def test_update_user_raises_http_error():
    json_params = {
        "datasetUserAccessRight": "Read",
        "identifier": "john@contoso.com",
        "principalType": "User",
    }

    responses.put(
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
        dataset.update_user("john@contoso.com", "User", "Read")


@responses.activate
def test_refresh_call_simple():
    request_id = "request_id"

    json_parms = {
        "notifyOption": "MailOnFailure",
    }

    responses.post(
        "https://api.powerbi.com/v1.0/myorg/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229/refreshes",
        match=[
            matchers.json_params_matcher(json_parms),
        ],
        headers={"requestId": request_id},
    )

    dataset = Dataset(
        id="cfafbeb1-8037-4d0c-896e-a46fb27ff229",
        session=requests.Session(),
    )

    refresh_id = dataset.refresh(notify_option="MailOnFailure")

    assert refresh_id == request_id


@responses.activate
def test_refresh_call_complex():
    request_id = "request_id"

    json_parms = {
        "notifyOption": "MailOnFailure",
        "retryCount": 3,
        "type": "full",
        "commitMode": "transactional",
        "objects": [
            {
                "table": "Customer",
                "partition": "Robert",
            },
        ],
        "applyRefreshPolicy": False,
    }

    responses.post(
        "https://api.powerbi.com/v1.0/myorg/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229/refreshes",
        match=[
            matchers.json_params_matcher(json_parms),
        ],
        headers={"requestId": request_id},
    )

    dataset = Dataset(
        id="cfafbeb1-8037-4d0c-896e-a46fb27ff229",
        session=requests.Session(),
    )

    refresh_id = dataset.refresh(
        notify_option="MailOnFailure",
        retry_count=3,
        type="full",
        commit_mode="transactional",
        apply_refresh_policy=False,
        objects=[
            {
                "table": "Customer",
                "partition": "Robert",
            },
        ],
    )

    assert refresh_id == request_id


@responses.activate
def test_take_over_call():
    responses.post(
        "https://api.powerbi.com/v1.0/myorg/groups/f089354e-8366-4e18-aea3-4cb4a3a50b48/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229/Default.TakeOver",
    )

    dataset = Dataset(
        id="cfafbeb1-8037-4d0c-896e-a46fb27ff229",
        group_id="f089354e-8366-4e18-aea3-4cb4a3a50b48",
        session=requests.Session(),
    )

    dataset.take_over()


@responses.activate
def test_take_over_raises_type_error():
    responses.post(
        "https://api.powerbi.com/v1.0/myorg/groups/f089354e-8366-4e18-aea3-4cb4a3a50b48/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229/Default.TakeOver",
    )

    dataset = Dataset(
        id="cfafbeb1-8037-4d0c-896e-a46fb27ff229",
        session=requests.Session(),
    )

    with pytest.raises(TypeError):
        dataset.take_over()


@responses.activate
def test_update_call():
    json_params = {"targetStorageMode": "PremiumFiles"}

    responses.patch(
        "https://api.powerbi.com/v1.0/myorg/groups/f089354e-8366-4e18-aea3-4cb4a3a50b48/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229",
        match=[
            matchers.json_params_matcher(json_params),
        ],
    )

    dataset = Dataset(
        id="cfafbeb1-8037-4d0c-896e-a46fb27ff229",
        group_id="f089354e-8366-4e18-aea3-4cb4a3a50b48",
        session=requests.Session(),
    )

    dataset.update(target_storage_mode="PremiumFiles")


@responses.activate
def test_update_datasources_single():
    json_params = {
        "updateDetails": [
            {
                "datasourceSelector": {
                    "datasourceType": "Sql",
                    "connectionDetails": {
                        "server": "My-Sql-Server",
                        "database": "My-Sql-Database",
                    },
                },
                "connectionDetails": {
                    "server": "New-Sql-Server",
                    "database": "New-Sql-Database",
                },
            },
        ]
    }

    responses.post(
        "https://api.powerbi.com/v1.0/myorg/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229/Default.UpdateDatasources",
        match=[
            matchers.json_params_matcher(json_params),
        ],
    )

    dataset = Dataset(
        id="cfafbeb1-8037-4d0c-896e-a46fb27ff229",
        session=requests.Session(),
    )

    update_details = {
        "datasourceSelector": {
            "datasourceType": "Sql",
            "connectionDetails": {
                "server": "My-Sql-Server",
                "database": "My-Sql-Database",
            },
        },
        "connectionDetails": {
            "server": "New-Sql-Server",
            "database": "New-Sql-Database",
        },
    }

    dataset.update_datasources(update_details=update_details)


@responses.activate
def test_update_datasources_multi():
    json_params = {
        "updateDetails": [
            {
                "datasourceSelector": {
                    "datasourceType": "Sql",
                    "connectionDetails": {
                        "server": "My-Sql-Server",
                        "database": "My-Sql-Database",
                    },
                },
                "connectionDetails": {
                    "server": "New-Sql-Server",
                    "database": "New-Sql-Database",
                },
            },
            {
                "datasourceSelector": {
                    "datasourceType": "OData",
                    "connectionDetails": {
                        "url": "http://services.odata.org/V4/Northwind/Northwind.svc"
                    },
                },
                "connectionDetails": {
                    "url": "http://services.odata.org/V4/Odata/Northwind.svc"
                },
            },
        ]
    }

    responses.post(
        "https://api.powerbi.com/v1.0/myorg/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229/Default.UpdateDatasources",
        match=[
            matchers.json_params_matcher(json_params),
        ],
    )

    dataset = Dataset(
        id="cfafbeb1-8037-4d0c-896e-a46fb27ff229",
        session=requests.Session(),
    )

    update_details = [
        {
            "datasourceSelector": {
                "datasourceType": "Sql",
                "connectionDetails": {
                    "server": "My-Sql-Server",
                    "database": "My-Sql-Database",
                },
            },
            "connectionDetails": {
                "server": "New-Sql-Server",
                "database": "New-Sql-Database",
            },
        },
        {
            "datasourceSelector": {
                "datasourceType": "OData",
                "connectionDetails": {
                    "url": "http://services.odata.org/V4/Northwind/Northwind.svc"
                },
            },
            "connectionDetails": {
                "url": "http://services.odata.org/V4/Odata/Northwind.svc"
            },
        },
    ]

    dataset.update_datasources(update_details=update_details)


@responses.activate
def test_update_refresh_schedule():
    json_params = {
        "value": {
            "days": [
                "Sunday",
                "Tuesday",
                "Friday",
                "Saturday",
            ],
            "times": [
                "07:00",
                "11:30",
                "16:00",
                "23:30",
            ],
            "localTimeZoneId": "UTC",
        }
    }

    responses.patch(
        "https://api.powerbi.com/v1.0/myorg/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229/refreshSchedule",
        match=[
            matchers.json_params_matcher(json_params),
        ],
    )

    dataset = Dataset(
        id="cfafbeb1-8037-4d0c-896e-a46fb27ff229",
        session=requests.Session(),
    )

    dataset.update_refresh_schedule(
        days=[
            "Sunday",
            "Tuesday",
            "Friday",
            "Saturday",
        ],
        times=[
            "07:00",
            "11:30",
            "16:00",
            "23:30",
        ],
        local_time_zone_id="UTC",
    )


@responses.activate
def test_update_refresh_schedule_direct_query():
    json_params = {
        "value": {
            "days": [
                "Sunday",
                "Tuesday",
                "Friday",
                "Saturday",
            ],
            "frequency": 15,
            "localTimeZoneId": "UTC",
        }
    }

    responses.patch(
        "https://api.powerbi.com/v1.0/myorg/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229/directQueryRefreshSchedule",
        match=[
            matchers.json_params_matcher(json_params),
        ],
    )

    dataset = Dataset(
        id="cfafbeb1-8037-4d0c-896e-a46fb27ff229",
        session=requests.Session(),
    )

    dataset.update_refresh_schedule(
        direct_query=True,
        days=[
            "Sunday",
            "Tuesday",
            "Friday",
            "Saturday",
        ],
        frequency=15,
        local_time_zone_id="UTC",
    )


@responses.activate
def test_update_refresh_schedule_raises():
    responses.patch(
        "https://api.powerbi.com/v1.0/myorg/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229/directQueryRefreshSchedule",
    )

    dataset = Dataset(
        id="cfafbeb1-8037-4d0c-896e-a46fb27ff229",
        session=requests.Session(),
    )
    with pytest.raises(ValueError):
        dataset.update_refresh_schedule()


@responses.activate
def test_update_parameters_single():
    json_params = {
        "updateDetails": [
            {
                "name": "DatabaseName",
                "newValue": "NewDB",
            },
        ]
    }

    responses.post(
        "https://api.powerbi.com/v1.0/myorg/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229/Default.UpdateParameters",
        match=[
            matchers.json_params_matcher(json_params),
        ],
    )

    dataset = Dataset(
        id="cfafbeb1-8037-4d0c-896e-a46fb27ff229",
        session=requests.Session(),
    )

    update_details = {
        "name": "DatabaseName",
        "newValue": "NewDB",
    }

    dataset.update_parameters(update_details)


@responses.activate
def test_update_parameters_multiple():
    json_params = {
        "updateDetails": [
            {
                "name": "DatabaseName",
                "newValue": "NewDB",
            },
            {
                "name": "MaxId",
                "newValue": "5678",
            },
        ]
    }

    responses.post(
        "https://api.powerbi.com/v1.0/myorg/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229/Default.UpdateParameters",
        match=[
            matchers.json_params_matcher(json_params),
        ],
    )

    dataset = Dataset(
        id="cfafbeb1-8037-4d0c-896e-a46fb27ff229",
        session=requests.Session(),
    )

    update_details = [
        {
            "name": "DatabaseName",
            "newValue": "NewDB",
        },
        {
            "name": "MaxId",
            "newValue": "5678",
        },
    ]

    dataset.update_parameters(update_details)


@responses.activate
def test_refresh():
    responses.post(
        "https://api.powerbi.com/v1.0/myorg/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229/refreshes",
        headers={"RequestId": "03f22bb5-2e98-4ae8-8113-329bec3987b1"},
    )

    dataset = Dataset(
        id="cfafbeb1-8037-4d0c-896e-a46fb27ff229",
        session=requests.Session(),
    )

    refresh_id = dataset.refresh()

    assert refresh_id == "03f22bb5-2e98-4ae8-8113-329bec3987b1"
