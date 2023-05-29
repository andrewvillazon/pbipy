import responses

from pbipy.models import App, Report


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
    assert any(isinstance(report, Report) for report in reports)
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
