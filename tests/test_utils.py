import pytest
import requests
from requests.exceptions import HTTPError
import responses
from responses import matchers

from pbipy import utils


def test_to_snake_case():
    assert (utils.to_snake_case("FluffyWuffy")) == "fluffy_wuffy"
    assert (utils.to_snake_case("webURL")) == "web_url"
    assert utils.to_snake_case("AyeBeeCee") == "aye_bee_cee"


def test_to_camel_case():
    assert (
        utils.to_camel_case("dataset_user_access_right")
    ) == "datasetUserAccessRight"
    assert (utils.to_camel_case("identifier")) == "identifier"
    assert (utils.to_camel_case("principal_type")) == "principalType"


def test_remove_no_values():
    test_d = {
        "queries": [
            {
                "query": "EVALUATE VALUES(MyTable)",
            },
        ],
        "serializerSettings": {"includeNulls": None},
        "impersonatedUserName": "someuser@mycompany.com",
    }

    expected_d = {
        "queries": [
            {
                "query": "EVALUATE VALUES(MyTable)",
            },
        ],
        "impersonatedUserName": "someuser@mycompany.com",
    }

    assert utils.remove_no_values(test_d) == expected_d


@pytest.fixture
def request_mixin():
    return utils.RequestsMixin()


@pytest.fixture
def session():
    return requests.Session()


# TODO: Add test for post_raw()


@responses.activate
def test_request_mixin_post(request_mixin, session):
    json_params = {
        "identifier": "john@contoso.com",
        "principalType": "User",
        "datasetUserAccessRight": "Read",
    }

    responses.post(
        "https://api.powerbi.com/v1.0/myorg/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229/users",
        match=[matchers.json_params_matcher(json_params)],
    )

    resource = "https://api.powerbi.com/v1.0/myorg/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229/users"
    payload = {
        "identifier": "john@contoso.com",
        "principalType": "User",
        "datasetUserAccessRight": "Read",
    }

    request_mixin.post(resource, session, payload)


@responses.activate
def test_request_mixin_post_raises(request_mixin, session):
    json_params = {
        "identifier": "john@contoso.com",
        "principalType": "User",
        "datasetUserAccessRight": "Read",
    }

    responses.post(
        "https://api.powerbi.com/v1.0/myorg/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229/users",
        match=[matchers.json_params_matcher(json_params)],
        body="{}",
        status=400,
    )

    resource = "https://api.powerbi.com/v1.0/myorg/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229/users"
    payload = {
        "identifier": "john@contoso.com",
        "principalType": "User",
        "datasetUserAccessRight": "Read",
    }

    with pytest.raises(HTTPError):
        request_mixin.post(resource, session, payload)


@pytest.fixture
def response_body_single_object():
    return """
    {
        "id": "f089354e-8366-4e18-aea3-4cb4a3a50b48",
        "description": "The finance app",
        "name": "Finance",
        "publishedBy": "Bill",
        "lastUpdate": "2019-01-13T09:46:53.094+02:00"
    }
    """


@pytest.fixture
def response_body_multiple_objects():
    return """
    {
        "value": [
            {
            "id": "f089354e-8366-4e18-aea3-4cb4a3a50b48",
            "isReadOnly": false,
            "isOnDedicatedCapacity": false,
            "name": "sample group"
            },
            {
            "id": "3d9b93c6-7b6d-4801-a491-1738910904fd",
            "isReadOnly": false,
            "isOnDedicatedCapacity": false,
            "name": "marketing group"
            },
            {
            "id": "a2f89923-421a-464e-bf4c-25eab39bb09f",
            "isReadOnly": false,
            "isOnDedicatedCapacity": false,
            "name": "contoso",
            "dataflowStorageId": "d692ae06-708c-485e-9987-06ff0fbdbb1f"
            }
        ]
    }
    """


@responses.activate
def test_request_mixin_get_raw_single_object(
    request_mixin,
    session,
    response_body_single_object,
):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/apps/f089354e-8366-4e18-aea3-4cb4a3a50b48",
        body=response_body_single_object,
    )

    resource = (
        "https://api.powerbi.com/v1.0/myorg/apps/f089354e-8366-4e18-aea3-4cb4a3a50b48"
    )
    raw = request_mixin.get_raw(resource, session)

    assert "id" in raw
    assert "description" in raw
    assert "name" in raw
    assert "publishedBy" in raw
    assert "lastUpdate" in raw


@responses.activate
def test_request_mixin_get_raw_single_object(
    request_mixin,
    session,
    response_body_multiple_objects,
):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/apps/f089354e-8366-4e18-aea3-4cb4a3a50b48",
        body=response_body_multiple_objects,
    )

    resource = (
        "https://api.powerbi.com/v1.0/myorg/apps/f089354e-8366-4e18-aea3-4cb4a3a50b48"
    )
    raw = request_mixin.get_raw(resource, session)

    assert isinstance(raw, list)


@responses.activate
def test_request_mixin_get_raw_raises(
    request_mixin,
    session,
):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/apps/f089354e-8366-4e18-aea3-4cb4a3a50b48",
        body="{}",
        status=404,
    )

    resource = (
        "https://api.powerbi.com/v1.0/myorg/apps/f089354e-8366-4e18-aea3-4cb4a3a50b48"
    )

    with pytest.raises(HTTPError):
        request_mixin.get_raw(resource, session)


@responses.activate
def test_request_mixin_put(request_mixin, session):
    json_params = {
        "identifier": "john@contoso.com",
        "principalType": "User",
        "datasetUserAccessRight": "Read",
    }

    responses.put(
        "https://api.powerbi.com/v1.0/myorg/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229/users",
        match=[matchers.json_params_matcher(json_params)],
    )

    resource = "https://api.powerbi.com/v1.0/myorg/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229/users"
    payload = {
        "identifier": "john@contoso.com",
        "principalType": "User",
        "datasetUserAccessRight": "Read",
    }

    request_mixin.put(resource, session, payload)


@responses.activate
def test_request_mixin_put_raises(request_mixin, session):
    json_params = {
        "identifier": "john@contoso.com",
        "principalType": "User",
        "datasetUserAccessRight": "Read",
    }

    responses.put(
        "https://api.powerbi.com/v1.0/myorg/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229/users",
        match=[matchers.json_params_matcher(json_params)],
        body="{}",
        status=400,
    )

    resource = "https://api.powerbi.com/v1.0/myorg/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229/users"
    payload = {
        "identifier": "john@contoso.com",
        "principalType": "User",
        "datasetUserAccessRight": "Read",
    }

    with pytest.raises(HTTPError):
        request_mixin.put(resource, session, payload)
