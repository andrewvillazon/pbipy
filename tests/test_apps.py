import pytest
import requests
import responses

from pbipy.apps import App
from pbipy.dashboards import Dashboard, Tile
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


@responses.activate
def test_reports(app_get_reports, app):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/apps/f089354e-8366-4e18-aea3-4cb4a3a50b48/reports",
        body=app_get_reports,
        content_type="application/json",
    )

    reports = app.reports()

    assert isinstance(reports, list)
    assert all(isinstance(report, Report) for report in reports)
    assert len(reports) == 1
    assert all(hasattr(report, "app_id") for report in reports)


@responses.activate
def test_dashboard(app_get_dashboard, app):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/apps/f089354e-8366-4e18-aea3-4cb4a3a50b48/dashboards/03dac094-2ff8-47e8-b2b9-dedbbc4d22ac",
        body=app_get_dashboard,
        content_type="application/json",
    )

    dashboard = app.dashboard("03dac094-2ff8-47e8-b2b9-dedbbc4d22ac")

    assert isinstance(dashboard, Dashboard)
    assert dashboard.app_id == "3d9b93c6-7b6d-4801-a491-1738910904fd"


@responses.activate
def test_dashboards(app_get_dashboards, app):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/apps/f089354e-8366-4e18-aea3-4cb4a3a50b48/dashboards",
        body=app_get_dashboards,
        content_type="application/json",
    )

    dashboards = app.dashboards()

    assert isinstance(dashboards, list)
    assert all(isinstance(dashboard, Dashboard) for dashboard in dashboards)
    assert all(hasattr(dashboard, "app_id") for dashboard in dashboards)


@responses.activate
def test_tile(app, app_get_tile):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/apps/f089354e-8366-4e18-aea3-4cb4a3a50b48/dashboards/3d9b93c6-7b6d-4801-a491-1738910904fd/tiles/312fbfe9-2eda-44e0-9ed0-ab5dc571bb4b",
        body=app_get_tile,
        content_type="application/json",
    )

    tile = app.tile(
        "312fbfe9-2eda-44e0-9ed0-ab5dc571bb4b",
        dashboard="3d9b93c6-7b6d-4801-a491-1738910904fd",
    )


@responses.activate
def test_tiles(app, app_get_tiles):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/apps/f089354e-8366-4e18-aea3-4cb4a3a50b48/dashboards/3d9b93c6-7b6d-4801-a491-1738910904fd/tiles",
        body=app_get_tiles,
        content_type="application/json",
    )

    tiles = app.tiles(dashboard="3d9b93c6-7b6d-4801-a491-1738910904fd")

    assert isinstance(tiles, list)
    assert all(isinstance(tile, Tile) for tile in tiles)
    assert len(tiles) == 1
