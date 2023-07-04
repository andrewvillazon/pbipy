import pytest
import requests

from pbipy.dataflows import Dataflow


@pytest.fixture
def dataflow():
    raw = {
        "objectId": "bd32e5c0-363f-430b-a03b-5535a4804b9b",
        "name": "AdventureWorks",
        "description": "Our Adventure Works",
        "modelUrl": "https://MyDataflowStorageAccount.dfs.core.windows.net/powerbi/contoso/AdventureWorks/model.json",
    }

    dataflow = Dataflow(
        id=raw.get("objectId"),
        session=requests.Session(),
        group_id="a2f89923-421a-464e-bf4c-25eab39bb09f",
        raw=raw,
    )

    return dataflow


def test_dataflow_creation(dataflow):
    assert isinstance(dataflow, Dataflow)
    assert dataflow.id == "bd32e5c0-363f-430b-a03b-5535a4804b9b"
    assert dataflow.name == "AdventureWorks"
    assert dataflow.description == "Our Adventure Works"
