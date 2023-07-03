import pytest
import requests
import responses

from pbipy.apps import App
from pbipy.reports import Report


@pytest.fixture
def app():
    raw = {
        "id": "f089354e-8366-4e18-aea3-4cb4a3a50b48",
        "description": "The finance app",
        "name": "Finance",
        "publishedBy": "Bill",
        "lastUpdate": "2019-01-13T09:46:53.094+02:00",
    }

    app = App(
        id=raw["id"],
        session=requests.Session(),
        raw=raw,
    )

    return app


def test_app_creation(app):
    assert isinstance(app, App)
    assert app.id == "f089354e-8366-4e18-aea3-4cb4a3a50b48"
    assert app.description == "The finance app"


@responses.activate
def test_report(app_get_report, app):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/apps/f089354e-8366-4e18-aea3-4cb4a3a50b48/reports/66b2570c-d9d3-40b2-83d9-1095c6700041",
        body=app_get_report,
        content_type="application/json",
    )

    report = app.report("66b2570c-d9d3-40b2-83d9-1095c6700041")

    assert isinstance(report, Report)
    assert report.app_id == "3d9b93c6-7b6d-4801-a491-1738910904fd"