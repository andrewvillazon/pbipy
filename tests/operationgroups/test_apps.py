import re

from datetime import datetime
import responses

from pbipy.models import App, Report, Dashboard, Tile


any_url = re.compile(".*")


@responses.activate
def test_get_apps(powerbi, get_apps):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/apps",
        body=get_apps,
        content_type="application/json",
    )

    apps = powerbi.apps.get_apps()

    assert len(apps) == 2
    assert all(isinstance(app, App) for app in apps)
    assert apps[0].name == "Finance"
    assert hasattr(apps[1], "users")
    assert not apps[1].users


@responses.activate
def test_get_reports_from_app_id(powerbi, app_from_raw, get_reports):
    responses.get(
        f"https://api.powerbi.com/v1.0/myorg/apps/{app_from_raw.id}/reports",
        body=get_reports,
        content_type="application/json",
    )

    reports = powerbi.apps.get_reports(app_from_raw.id)

    assert len(reports) == 2
    assert all(isinstance(report, Report) for report in reports)
    assert reports[0].name == "SalesMarketing"
    assert hasattr(reports[0], "dataset_id")
    assert hasattr(reports[0], "web_url")
    assert hasattr(reports[0], "embed_url")
    assert not reports[0].users
    assert isinstance(reports, list)


@responses.activate
def test_get_reports_from_app(powerbi, app_from_raw, get_reports):
    responses.get(
        f"https://api.powerbi.com/v1.0/myorg/apps/{app_from_raw.id}/reports",
        body=get_reports,
        content_type="application/json",
    )

    reports = powerbi.apps.get_reports(app_from_raw)

    assert not reports[1].is_owned_by_me
    assert reports[1].embed_url
    assert not len(reports[1].subscriptions)


@responses.activate
def test_get_app(powerbi, get_app):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/apps/f089354e-8366-4e18-aea3-4cb4a3a50b48",
        body=get_app,
        content_type="application/json",
    )

    app = powerbi.apps.get_app("f089354e-8366-4e18-aea3-4cb4a3a50b48")

    assert app.id == "f089354e-8366-4e18-aea3-4cb4a3a50b48"
    assert app.name == "Finance"
    assert isinstance(app.last_update, datetime)
    assert hasattr(app, "workspace_id")
    assert not app.users


@responses.activate
def test_get_dashboard_using_app_id_and_dashboard_id(powerbi, get_dashboard):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/apps/3d9b93c6-7b6d-4801-a491-1738910904fd/dashboards/03dac094-2ff8-47e8-b2b9-dedbbc4d22ac",
        body=get_dashboard,
        content_type="application/json",
    )

    dashboard = powerbi.apps.get_dashboard(
        "3d9b93c6-7b6d-4801-a491-1738910904fd", "03dac094-2ff8-47e8-b2b9-dedbbc4d22ac"
    )

    assert isinstance(dashboard, Dashboard)
    assert dashboard.display_name == "SalesMarketing"
    assert not dashboard.is_read_only
    assert not dashboard.users
    assert not isinstance(dashboard.subscriptions, list)


@responses.activate
def test_get_dashboard_using_app_and_dashboard_id(powerbi, app_from_raw, get_dashboard):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/apps/3d9b93c6-7b6d-4801-a491-1738910904fd/dashboards/03dac094-2ff8-47e8-b2b9-dedbbc4d22ac",
        body=get_dashboard,
        content_type="application/json",
    )

    dashboard = powerbi.apps.get_dashboard(
        app_from_raw, "03dac094-2ff8-47e8-b2b9-dedbbc4d22ac"
    )

    assert isinstance(dashboard, Dashboard)
    assert dashboard.display_name == "SalesMarketing"
    assert not dashboard.is_read_only
    assert not dashboard.users
    assert not isinstance(dashboard.subscriptions, list)


@responses.activate
def test_get_dashboards_using_app_id(powerbi, get_dashboards):
    responses.get(
        any_url,
        body=get_dashboards,
        content_type="application/json",
    )

    dashboards = powerbi.apps.get_dashboards("3d9b93c6-7b6d-4801-a491-1738910904fd")

    assert len(dashboards) == 2
    assert all(isinstance(dashboard, Dashboard) for dashboard in dashboards)
    assert dashboards[1].display_name == "FinanceMarketing"
    assert not dashboards[0].is_read_only
    assert dashboards[1].is_read_only


@responses.activate
def test_get_dashboards_using_app(powerbi, get_dashboards, app_from_raw):
    responses.get(
        any_url,
        body=get_dashboards,
        content_type="application/json",
    )

    dashboards = powerbi.apps.get_dashboards(app_from_raw)

    assert len(dashboards) == 2
    assert all(isinstance(dashboard, Dashboard) for dashboard in dashboards)
    assert dashboards[1].display_name == "FinanceMarketing"
    assert not dashboards[0].is_read_only
    assert dashboards[1].is_read_only
    assert all(dashboard.app_id == app_from_raw.id for dashboard in dashboards)


@responses.activate
def test_get_report_using_app_id(powerbi, get_report):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/apps/3d9b93c6-7b6d-4801-a491-1738910904fd/reports/66b2570c-d9d3-40b2-83d9-1095c6700041",
        body=get_report,
        content_type="application/json",
    )

    report = powerbi.apps.get_report(
        "3d9b93c6-7b6d-4801-a491-1738910904fd", "66b2570c-d9d3-40b2-83d9-1095c6700041"
    )

    assert isinstance(report, Report)
    assert report.name == "SalesMarketing"
    assert report.id == "66b2570c-d9d3-40b2-83d9-1095c6700041"
    assert not report.is_owned_by_me
    assert report.subscriptions is None
    assert report.users is None


@responses.activate
def test_get_report_using_app(powerbi, get_report, app_from_raw):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/apps/3d9b93c6-7b6d-4801-a491-1738910904fd/reports/66b2570c-d9d3-40b2-83d9-1095c6700041",
        body=get_report,
        content_type="application/json",
    )

    report = powerbi.apps.get_report(
        app_from_raw, "66b2570c-d9d3-40b2-83d9-1095c6700041"
    )

    assert isinstance(report, Report)
    assert report.name == "SalesMarketing"
    assert report.id == "66b2570c-d9d3-40b2-83d9-1095c6700041"
    assert not report.is_owned_by_me
    assert report.subscriptions is None
    assert report.users is None


@responses.activate
def test_get_tile_using_app_id_and_dashboard_id(powerbi, get_tile):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/apps/3d9b93c6-7b6d-4801-a491-1738910904fd/dashboards/03dac094-2ff8-47e8-b2b9-dedbbc4d22ac/tiles/312fbfe9-2eda-44e0-9ed0-ab5dc571bb4b",
        body=get_tile,
        content_type="application/json",
    )

    tile = powerbi.apps.get_tile("3d9b93c6-7b6d-4801-a491-1738910904fd", "03dac094-2ff8-47e8-b2b9-dedbbc4d22ac", "312fbfe9-2eda-44e0-9ed0-ab5dc571bb4b")

    assert isinstance(tile, Tile)
    assert tile.id == "312fbfe9-2eda-44e0-9ed0-ab5dc571bb4b"
    assert tile.row_span == 0
    assert tile.col_span == 0
    assert tile.title == "SalesMarketingTile"
    assert tile.sub_title == "SalesMarketing"


@responses.activate
def test_get_tile_using_app_and_dashboard(powerbi, app_from_raw, dashboard_from_raw, get_tile):
    responses.get(
        f"https://api.powerbi.com/v1.0/myorg/apps/{app_from_raw.id}/dashboards/{dashboard_from_raw.id}/tiles/312fbfe9-2eda-44e0-9ed0-ab5dc571bb4b",
        body=get_tile,
        content_type="application/json",
    )

    tile = powerbi.apps.get_tile(app_from_raw, dashboard_from_raw, "312fbfe9-2eda-44e0-9ed0-ab5dc571bb4b")

    assert isinstance(tile, Tile)
    assert tile.id == "312fbfe9-2eda-44e0-9ed0-ab5dc571bb4b"
    assert tile.row_span == 0
    assert tile.col_span == 0
    assert tile.title == "SalesMarketingTile"
    assert tile.sub_title == "SalesMarketing"


@responses.activate
def test_get_tiles_using_app_id_and_dashboard_id(powerbi, get_tiles):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/apps/3d9b93c6-7b6d-4801-a491-1738910904fd/dashboards/03dac094-2ff8-47e8-b2b9-dedbbc4d22ac/tiles",
        body=get_tiles,
        content_type="application/json",
    )

    tiles = powerbi.apps.get_tiles("3d9b93c6-7b6d-4801-a491-1738910904fd","03dac094-2ff8-47e8-b2b9-dedbbc4d22ac")

    assert isinstance(tiles, list)
    assert all(isinstance(tile, Tile) for tile in tiles)
    assert len(tiles) == 1


@responses.activate
def test_get_tiles_using_app_and_dashboard(powerbi, app_from_raw, dashboard_from_raw, get_tiles):
    responses.get(
        f"https://api.powerbi.com/v1.0/myorg/apps/{app_from_raw.id}/dashboards/{dashboard_from_raw.id}/tiles",
        body=get_tiles,
        content_type="application/json",
    )

    tiles = powerbi.apps.get_tiles(app_from_raw, dashboard_from_raw)

    assert isinstance(tiles, list)
    assert all(isinstance(tile, Tile) for tile in tiles)
    assert len(tiles) == 1