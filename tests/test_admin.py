import pytest
import requests
import responses
from responses import matchers

from pbipy.apps import App
from pbipy.dashboards import Dashboard
from pbipy.groups import Group


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


@responses.activate
def test_dashboards(admin, get_dashboards_as_admin):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/admin/dashboards",
        body=get_dashboards_as_admin,
        match=[
            matchers.query_param_matcher(None),
        ],
        content_type="application/json",
    )

    dashboards = admin.dashboards()


@responses.activate
def test_dashboards_with_params(admin, get_dashboards_as_admin):
    params = {
        "$skip": 1,
        "$top": 3,
        "$filter": "contains(name,'marketing')",
    }

    responses.get(
        "https://api.powerbi.com/v1.0/myorg/admin/dashboards",
        body=get_dashboards_as_admin,
        match=[
            matchers.query_param_matcher(params),
        ],
        content_type="application/json",
    )

    dashboards = admin.dashboards(
        skip=1,
        top=3,
        filter="contains(name,'marketing')",
    )


@responses.activate
def test_dashboards_result(admin, get_dashboards_as_admin):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/admin/dashboards",
        body=get_dashboards_as_admin,
        match=[
            matchers.query_param_matcher(None),
        ],
        content_type="application/json",
    )

    dashboards = admin.dashboards()

    assert isinstance(dashboards, list)
    assert all(isinstance(dashboard, Dashboard) for dashboard in dashboards)


@responses.activate
def test_dashboards_with_group(admin, get_dashboards_as_admin):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/admin/groups/f089354e-8366-4e18-aea3-4cb4a3a50b48/dashboards",
        body=get_dashboards_as_admin,
        match=[
            matchers.query_param_matcher(None),
        ],
        content_type="application/json",
    )
    group = Group(
        id="f089354e-8366-4e18-aea3-4cb4a3a50b48",
        session=requests.Session(),
    )
    dashboards = admin.dashboards(group=group)


# TODO: Need to add response body for ExportDataflowAsAdmin endpoint
@responses.activate
def test_dataflow(admin):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/admin/dataflows/928228ba-008d-4fd9-864a-92d2752ee5ce/export",
        body="{}",
        content_type="application/json",
    )

    admin.dataflow(dataflow="928228ba-008d-4fd9-864a-92d2752ee5ce")


@responses.activate
def test_dataflow_datasources(admin, get_dataflow_datasources_as_admin):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/admin/dataflows/cfafbeb1-8037-4d0c-896e-a46fb27ff229/datasources",
        body=get_dataflow_datasources_as_admin,
        content_type="application/json",
    )

    datasources = admin.dataflow_datasources(
        dataflow="cfafbeb1-8037-4d0c-896e-a46fb27ff229"
    )

    assert isinstance(datasources, list)
    assert all(isinstance(datasource, dict) for datasource in datasources)
