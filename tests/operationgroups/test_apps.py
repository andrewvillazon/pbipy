import responses

from pbipy.models import App


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
    assert hasattr(apps[1],"users")
    assert not apps[1].users