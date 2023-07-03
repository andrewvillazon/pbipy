import pytest
import requests

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
