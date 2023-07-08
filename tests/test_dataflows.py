import pytest
import requests
import responses
from responses import matchers

from pbipy.dataflows import Dataflow


@pytest.fixture
def dataflow():
    raw = {
        "objectId": "928228ba-008d-4fd9-864a-92d2752ee5ce",
        "name": "AdventureWorks",
        "description": "Our Adventure Works",
        "modelUrl": "https://MyDataflowStorageAccount.dfs.core.windows.net/powerbi/contoso/AdventureWorks/model.json",
    }

    dataflow = Dataflow(
        id=raw.get("objectId"),
        session=requests.Session(),
        group_id="51e47fc5-48fd-4826-89f0-021bd3a80abd",
        raw=raw,
    )

    return dataflow


def test_dataflow_creation(dataflow):
    assert isinstance(dataflow, Dataflow)
    assert dataflow.id == "928228ba-008d-4fd9-864a-92d2752ee5ce"
    assert dataflow.name == "AdventureWorks"
    assert dataflow.description == "Our Adventure Works"


@responses.activate
def test_datasources(dataflow, get_dataflow_datasources):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/groups/51e47fc5-48fd-4826-89f0-021bd3a80abd/dataflows/928228ba-008d-4fd9-864a-92d2752ee5ce/datasources",
        body=get_dataflow_datasources,
        content_type="application/json",
    )

    datasources = dataflow.datasources()

    assert isinstance(datasources, list)
    assert all(isinstance(datasource, dict) for datasource in datasources)


@responses.activate
def test_transactions(dataflow, get_dataflow_transactions):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/groups/51e47fc5-48fd-4826-89f0-021bd3a80abd/dataflows/928228ba-008d-4fd9-864a-92d2752ee5ce/transactions",
        body=get_dataflow_transactions,
        content_type="application/json",
    )

    transactions = dataflow.transactions()

    assert isinstance(transactions, list)
    assert all(isinstance(transaction, dict) for transaction in transactions)
    assert len(transactions) == 2


# TODO: Add test that includes response body
@responses.activate
def test_upstream_dataflows(dataflow):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/groups/51e47fc5-48fd-4826-89f0-021bd3a80abd/dataflows/928228ba-008d-4fd9-864a-92d2752ee5ce/upstreamDataflows",
        body='{"value":[]}',
    )

    dataflow.upstream_dataflows()


@responses.activate
def test_refresh_no_params(dataflow):
    json_params = {"notifyOption": "MailOnCompletion"}

    responses.post(
        "https://api.powerbi.com/v1.0/myorg/groups/51e47fc5-48fd-4826-89f0-021bd3a80abd/dataflows/928228ba-008d-4fd9-864a-92d2752ee5ce/refreshes",
        match=[
            matchers.json_params_matcher(json_params),
        ],
    )

    dataflow.refresh(notify_option="MailOnCompletion")


@responses.activate
def test_refresh_params(dataflow):
    json_params = {"notifyOption": "MailOnCompletion"}

    responses.post(
        "https://api.powerbi.com/v1.0/myorg/groups/51e47fc5-48fd-4826-89f0-021bd3a80abd/dataflows/928228ba-008d-4fd9-864a-92d2752ee5ce/refreshes?processType=default",
        match=[
            matchers.json_params_matcher(json_params),
        ],
    )

    dataflow.refresh(notify_option="MailOnCompletion", process_type="default")


@responses.activate
def test_update_call(dataflow):
    json_params = {
        "name": "New Dataflow Name",
        "allowNativeQueries": True,
    }

    responses.patch(
        "https://api.powerbi.com/v1.0/myorg/groups/51e47fc5-48fd-4826-89f0-021bd3a80abd/dataflows/928228ba-008d-4fd9-864a-92d2752ee5ce",
        match=[
            matchers.json_params_matcher(json_params),
        ],
    )

    dataflow.update(
        name="New Dataflow Name",
        allow_native_queries=True,
    )


def test_update_raises(dataflow):
    with pytest.raises(ValueError):
        dataflow.update()


@responses.activate
def test_update_refresh_schedule(dataflow):
    json_params = {
        "value": {
            "days": [
                "Monday",
                "Wednesday",
            ],
            "times": [
                "10:00",
                "16:00",
            ],
            "notifyOption": "NoNotification",
        }
    }

    responses.patch(
        "https://api.powerbi.com/v1.0/myorg/groups/51e47fc5-48fd-4826-89f0-021bd3a80abd/dataflows/928228ba-008d-4fd9-864a-92d2752ee5ce/refreshSchedule",
        match=[
            matchers.json_params_matcher(json_params),
        ],
    )

    dataflow.update_refresh_schedule(
        days=["Monday", "Wednesday"],
        times=["10:00", "16:00"],
        notify_option="NoNotification",
    )


def test_update_refresh_schedule_raises(dataflow):
    with pytest.raises(ValueError):
        dataflow.update_refresh_schedule()
