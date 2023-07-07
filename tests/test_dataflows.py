import pytest
import requests
import responses

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