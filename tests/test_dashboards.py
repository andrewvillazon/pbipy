import pytest
import requests
import responses
from responses import matchers

from pbipy.dashboards import Dashboard, Tile


@pytest.fixture
def dashboard_with_group():
    raw = {
        "id": "69ffaa6c-b36d-4d01-96f5-1ed67c64d4af",
        "displayName": "SalesMarketing",
        "embedUrl": "https://app.powerbi.com/dashboardEmbed?dashboardId=69ffaa6c-b36d-4d01-96f5-1ed67c64d4af",
        "isReadOnly": False,
    }

    dashboard = Dashboard(
        id=raw.get("id"),
        group_id="f089354e-8366-4e18-aea3-4cb4a3a50b48",
        session=requests.Session(),
        raw=raw,
    )

    return dashboard


@pytest.fixture
def tile():
    raw = {
        "id": "312fbfe9-2eda-44e0-9ed0-ab5dc571bb4b",
        "title": "SalesMarketingTile",
        "embedUrl": "https://app.powerbi.com/embed?dashboardId=69ffaa6c-b36d-4d01-96f5-1ed67c64d4af&tileId=312fbfe9-2eda-44e0-9ed0-ab5dc571bb4b&groupId=f089354e-8366-4e18-aea3-4cb4a3a50b48",
        "rowSpan": 0,
        "colSpan": 0,
        "reportId": "5b218778-e7a5-4d73-8187-f10824047715",
        "datasetId": "cfafbeb1-8037-4d0c-896e-a46fb27ff229",
    }

    tile = Tile(
        id=raw.get("id"),
        dashboard_id="69ffaa6c-b36d-4d01-96f5-1ed67c64d4af",
        session=requests.Session(),
        raw=raw,
    )

    return tile


def test_dashboard_creation(dashboard_with_group):
    assert isinstance(dashboard_with_group, Dashboard)
    assert dashboard_with_group.id == "69ffaa6c-b36d-4d01-96f5-1ed67c64d4af"


def test_tile_creation(tile):
    assert isinstance(tile, Tile)
    assert tile.row_span == 0
    assert tile.col_span == 0
    assert tile.report_id == "5b218778-e7a5-4d73-8187-f10824047715"
    assert tile.title == "SalesMarketingTile"


@responses.activate
def test_add_dashboard(powerbi, add_dashboard):
    json_params = {"name": "SalesMarketing"}

    responses.post(
        "https://api.powerbi.com/v1.0/myorg/dashboards",
        body=add_dashboard,
        match=[
            matchers.json_params_matcher(json_params),
        ],
        content_type="application/json",
    )

    dashboard = powerbi.add_dashboard("SalesMarketing")

    assert isinstance(dashboard, Dashboard)
    assert dashboard.group_id is None
    assert dashboard.id == "69ffaa6c-b36d-4d01-96f5-1ed67c64d4af"


@responses.activate
def test_add_dashboard_with_group(powerbi, add_dashboard):
    json_params = {"name": "SalesMarketing"}

    responses.post(
        "https://api.powerbi.com/v1.0/myorg/groups/f089354e-8366-4e18-aea3-4cb4a3a50b48/dashboards",
        body=add_dashboard,
        match=[
            matchers.json_params_matcher(json_params),
        ],
        content_type="application/json",
    )

    dashboard = powerbi.add_dashboard(
        "SalesMarketing",
        group="f089354e-8366-4e18-aea3-4cb4a3a50b48",
    )

    assert isinstance(dashboard, Dashboard)
    assert dashboard.group_id == "f089354e-8366-4e18-aea3-4cb4a3a50b48"
    assert dashboard.id == "69ffaa6c-b36d-4d01-96f5-1ed67c64d4af"
