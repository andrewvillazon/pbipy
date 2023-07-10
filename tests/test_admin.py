import pytest
import responses
from responses import matchers

from pbipy.apps import App


@pytest.fixture
def admin(powerbi):
    return powerbi.admin()


@responses.activate
def test_app_users(admin, get_app_users_as_admin):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/admin/apps/f089354e-8366-4e18-aea3-4cb4a3a50b48/users",
        body=get_app_users_as_admin,
        content_type="application/json",
    )

    users = admin.app_users("f089354e-8366-4e18-aea3-4cb4a3a50b48")

    assert isinstance(users, list)
    assert all(isinstance(user, dict) for user in users)


@responses.activate
def test_apps(admin, get_apps_as_admin):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/admin/apps",
        body=get_apps_as_admin,
        match=[
            matchers.query_param_matcher(None),
        ],
        content_type="application/json",
    )

    apps = admin.apps()


@responses.activate
def test_apps_params(admin, get_apps_as_admin):
    params = {"$top": 1}
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/admin/apps",
        body=get_apps_as_admin,
        match=[
            matchers.query_param_matcher(params),
        ],
        content_type="application/json",
    )

    apps = admin.apps(top=1)


@responses.activate
def test_apps_result(admin, get_apps_as_admin):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/admin/apps",
        body=get_apps_as_admin,
        match=[
            matchers.query_param_matcher(None),
        ],
        content_type="application/json",
    )

    apps = admin.apps()

    assert isinstance(apps, list)
    assert all(isinstance(app, App) for app in apps)
