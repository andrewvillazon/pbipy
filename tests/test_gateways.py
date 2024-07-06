import pytest
import responses
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
