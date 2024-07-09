import pytest
import responses
from responses import matchers
import requests

from pbipy.gateways import Gateway


@pytest.fixture
def gateway():
    raw = {
        "id": "1f69e798-5852-4fdd-ab01-33bb14b6e934",
        "name": "My_Sample_Gateway",
        "type": "Resource",
        "publicKey": {
            "exponent": "AQAB",
            "modulus": "o6j2....cLk=",
        },
    }

    gateway = Gateway(
        id=raw.get("id"),
        session=requests.Session(),
        raw=raw,
    )

    return gateway


@responses.activate
def test_datasources(gateway, gateways_get_datasources):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/gateways/1f69e798-5852-4fdd-ab01-33bb14b6e934/datasources",
        body=gateways_get_datasources,
        content_type="application/json",
    )

    datasources = gateway.datasources()

    assert isinstance(datasources, list)
    assert len(datasources) == 2


@responses.activate
def test_datasource(gateway, gateways_get_datasource):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/gateways/1f69e798-5852-4fdd-ab01-33bb14b6e934/datasources/252b9de8-d915-4788-aaeb-ec8c2395f970",
        body=gateways_get_datasource,
        content_type="application/json",
    )

    datasource = gateway.datasource("252b9de8-d915-4788-aaeb-ec8c2395f970")

    assert datasource["datasourceType"] == "Sql"
    assert datasource["gatewayId"] == "1f69e798-5852-4fdd-ab01-33bb14b6e934"
    assert isinstance(datasource["connectionDetails"], str)


@responses.activate
def test_datasource_status(gateway):
    # TODO: Test requires a response body.

    responses.get(
        "https://api.powerbi.com/v1.0/myorg/gateways/1f69e798-5852-4fdd-ab01-33bb14b6e934/datasources/252b9de8-d915-4788-aaeb-ec8c2395f970/status",
        body="{}",
    )

    gateway.datasource_status("252b9de8-d915-4788-aaeb-ec8c2395f970")


@responses.activate
def test_datasource_users(gateway, gateways_get_datasource_users):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/gateways/1f69e798-5852-4fdd-ab01-33bb14b6e934/datasources/252b9de8-d915-4788-aaeb-ec8c2395f970/users",
        body=gateways_get_datasource_users,
        content_type="application/json",
    )

    users = gateway.datasource_users("252b9de8-d915-4788-aaeb-ec8c2395f970")

    assert len(users) == 2
    assert all(isinstance(user, dict) for user in users)
    assert users[0]["emailAddress"] == "john@contoso.com"
    assert users[1]["principalType"] == "App"


@responses.activate
def test_delete_datasource_user(gateway):
    responses.delete(
        "https://api.powerbi.com/v1.0/myorg/gateways/1f69e798-5852-4fdd-ab01-33bb14b6e934/datasources/252b9de8-d915-4788-aaeb-ec8c2395f970/users/john@contoso.com"
    )

    gateway.delete_datasource_user(
        "252b9de8-d915-4788-aaeb-ec8c2395f970",
        "john@contoso.com",
    )


@responses.activate
def test_create_datasource(gateway, gateways_get_datasource):
    json_params = {
        "dataSourceType": "AnalysisServices",
        "connectionDetails": '{"server":"MyServer","database":"MyDatabase"}',
        "dataSourceName": "Sample Datasource",
        "credentialDetails": {
            "credentialType": "Windows",
            "credentials": "AB....EF==",
            "encryptedConnection": "Encrypted",
            "encryptionAlgorithm": "RSA-OAEP",
            "privacyLevel": "None",
        },
    }

    responses.post(
        "https://api.powerbi.com/v1.0/myorg/gateways/1f69e798-5852-4fdd-ab01-33bb14b6e934/datasources",
        body=gateways_get_datasource,
        match=[
            matchers.json_params_matcher(json_params),
        ],
    )

    credential_details = {
        "credentialType": "Windows",
        "credentials": "AB....EF==",
        "encryptedConnection": "Encrypted",
        "encryptionAlgorithm": "RSA-OAEP",
        "privacyLevel": "None",
    }

    new_datasource = gateway.create_datasource(
        connection_details='{"server":"MyServer","database":"MyDatabase"}',
        credential_details=credential_details,
        datasource_name="Sample Datasource",
        datasource_type="AnalysisServices",
    )


@responses.activate
def test_add_datasource_user_identity(gateway):
    json_params = {
        "identifier": "3d9b93c6-7b6d-4801-a491-1738910904fd",
        "datasourceAccessRight": "ReadOverrideEffectiveIdentity",
    }

    responses.post(
        "https://api.powerbi.com/v1.0/myorg/gateways/1f69e798-5852-4fdd-ab01-33bb14b6e934/datasources/252b9de8-d915-4788-aaeb-ec8c2395f970/users",
        match=[matchers.json_params_matcher(json_params)],
    )

    gateway.add_datasource_user(
        datasource="252b9de8-d915-4788-aaeb-ec8c2395f970",
        datasource_access_right="ReadOverrideEffectiveIdentity",
        identifier="3d9b93c6-7b6d-4801-a491-1738910904fd",
    )


@responses.activate
def test_add_datasource_user_email(gateway):
    json_params = {
        "emailAddress": "john@contoso.com",
        "datasourceAccessRight": "Read",
    }

    responses.post(
        "https://api.powerbi.com/v1.0/myorg/gateways/1f69e798-5852-4fdd-ab01-33bb14b6e934/datasources/252b9de8-d915-4788-aaeb-ec8c2395f970/users",
        match=[matchers.json_params_matcher(json_params)],
    )

    gateway.add_datasource_user(
        datasource="252b9de8-d915-4788-aaeb-ec8c2395f970",
        datasource_access_right="Read",
        email_address="john@contoso.com",
    )


def test_add_datasource_user_raises(gateway):
    with pytest.raises(ValueError):
        gateway.add_datasource_user(
            datasource="252b9de8-d915-4788-aaeb-ec8c2395f970",
            datasource_access_right="Read",
        )
