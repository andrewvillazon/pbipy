import pytest
import requests

from pbipy.dashboards import Dashboard


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


def test_dashboard_creation(dashboard_with_group):
    assert isinstance(dashboard_with_group, Dashboard)
    assert dashboard_with_group.id == "69ffaa6c-b36d-4d01-96f5-1ed67c64d4af"