from datetime import datetime

import pytest
import requests
import responses
from responses import matchers
from responses.registries import OrderedRegistry

from pbipy.apps import App
from pbipy.dashboards import Dashboard, Tile
from pbipy.dataflows import Dataflow
from pbipy.datasets import Dataset
from pbipy.groups import Group
from pbipy.reports import Report


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


@responses.activate
def test_dataflow_users(admin, get_dataflow_users_as_admin):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/admin/dataflows/cfafbeb1-8037-4d0c-896e-a46fb27ff229/users",
        body=get_dataflow_users_as_admin,
        content_type="application/json",
    )

    users = admin.dataflow_users(dataflow="cfafbeb1-8037-4d0c-896e-a46fb27ff229")

    assert isinstance(users, list)
    assert all(isinstance(user, dict) for user in users)


@responses.activate
def test_dataflow_upstream_dataflows(admin, get_upstream_dataflows_in_group_as_admin):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/admin/groups/f089354e-8366-4e18-aea3-4cb4a3a50b48/dataflows/cfafbeb1-8037-4d0c-896e-a46fb27ff229/upstreamDataflows",
        body=get_upstream_dataflows_in_group_as_admin,
        content_type="application/json",
    )

    upstream_dataflows = admin.dataflow_upstream_dataflows(
        dataflow="cfafbeb1-8037-4d0c-896e-a46fb27ff229",
        group="f089354e-8366-4e18-aea3-4cb4a3a50b48",
    )

    assert isinstance(upstream_dataflows, list)
    assert all(
        isinstance(upstream_dataflow, dict) for upstream_dataflow in upstream_dataflows
    )


@responses.activate
def test_dataset_upstream_dataflows(
    admin,
    get_dataset_to_dataflow_links_in_group_as_admin,
):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/admin/groups/f089354e-8366-4e18-aea3-4cb4a3a50b48/datasets/upstreamDataflows",
        body=get_dataset_to_dataflow_links_in_group_as_admin,
        content_type="application/json",
    )

    upstream_dataflows = admin.datasets_upstream_dataflows(
        group="f089354e-8366-4e18-aea3-4cb4a3a50b48"
    )

    assert isinstance(upstream_dataflows, list)
    assert all(
        isinstance(upstream_dataflow, dict) for upstream_dataflow in upstream_dataflows
    )


@responses.activate
def test_dataset_users(admin, get_dataset_users_as_admin):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/admin/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229/users",
        body=get_dataset_users_as_admin,
        content_type="application/json",
    )

    dataset = Dataset(
        id="cfafbeb1-8037-4d0c-896e-a46fb27ff229",
        session=requests.Session(),
    )

    users = admin.dataset_users(dataset=dataset)

    assert isinstance(users, list)
    assert all(isinstance(user, dict) for user in users)


@responses.activate
def test_datasets(admin, get_datasets_as_admin):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/admin/datasets",
        body=get_datasets_as_admin,
        match=[
            matchers.query_param_matcher(None),
        ],
        content_type="application/json",
    )

    datasets = admin.datasets()


@responses.activate
def test_datasets_with_params(admin, get_datasets_as_admin):
    params = {
        "$top": 2,
        "$filter": "contains(name,'marketing')",
    }

    responses.get(
        "https://api.powerbi.com/v1.0/myorg/admin/datasets",
        body=get_datasets_as_admin,
        match=[
            matchers.query_param_matcher(params),
        ],
        content_type="application/json",
    )

    datasets = admin.datasets(filter="contains(name,'marketing')", top=2)


@responses.activate
def test_datasets_results(admin, get_datasets_as_admin):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/admin/datasets",
        body=get_datasets_as_admin,
        match=[
            matchers.query_param_matcher(None),
        ],
        content_type="application/json",
    )

    datasets = admin.datasets()

    assert isinstance(datasets, list)
    assert all(isinstance(dataset, Dataset) for dataset in datasets)
    assert datasets[0].group_id is not None
    assert datasets[0].group_id == datasets[0].workspace_id


@responses.activate
def test_datasets_with_group(admin, get_datasets_in_group_as_admin):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/admin/groups/f089354e-8366-4e18-aea3-4cb4a3a50b48/datasets",
        body=get_datasets_in_group_as_admin,
        content_type="application/json",
    )

    datasets = admin.datasets(group="f089354e-8366-4e18-aea3-4cb4a3a50b48")

    assert datasets[0].group_id == "f089354e-8366-4e18-aea3-4cb4a3a50b48"
    assert not hasattr(datasets[0], "workspace_id")


@responses.activate
def test_datasets_with_group_obj(admin, get_datasets_in_group_as_admin):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/admin/groups/f089354e-8366-4e18-aea3-4cb4a3a50b48/datasets",
        body=get_datasets_in_group_as_admin,
        content_type="application/json",
    )
    group = Group(
        id="f089354e-8366-4e18-aea3-4cb4a3a50b48",
        session=requests.Session(),
    )
    datasets = admin.datasets(group=group)

    assert datasets[0].group_id == "f089354e-8366-4e18-aea3-4cb4a3a50b48"
    assert not hasattr(datasets[0], "workspace_id")


@responses.activate
def test_dataflows(admin, get_dataflows_as_admin):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/admin/dataflows",
        body=get_dataflows_as_admin,
        match=[
            matchers.query_param_matcher(None),
        ],
        content_type="application/json",
    )

    dataflows = admin.dataflows()

    assert isinstance(dataflows, list)
    assert all(isinstance(dataflow, Dataflow) for dataflow in dataflows)

    assert dataflows[0].id == "bd32e5c0-363f-430b-a03b-5535a4804b9b"
    assert dataflows[0].name
    assert dataflows[0].description
    assert dataflows[0].model_url
    assert dataflows[0].configured_by
    assert dataflows[0].group_id == dataflows[0].workspace_id


@responses.activate
def test_dataflows_with_group(admin, get_dataflows_in_group_as_admin):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/admin/groups/f089354e-8366-4e18-aea3-4cb4a3a50b48/dataflows",
        body=get_dataflows_in_group_as_admin,
        match=[
            matchers.query_param_matcher(None),
        ],
        content_type="application/json",
    )

    dataflows = admin.dataflows(group="f089354e-8366-4e18-aea3-4cb4a3a50b48")

    assert isinstance(dataflows, list)
    assert all(isinstance(dataflow, Dataflow) for dataflow in dataflows)

    assert dataflows[0].id
    assert dataflows[0].group_id == "f089354e-8366-4e18-aea3-4cb4a3a50b48"
    assert not hasattr(dataflows[0], "workspace_id")


@responses.activate
def test_dataflows_with_params(admin, get_dataflows_as_admin):
    params = {"$top": 1, "$skip": 3}

    responses.get(
        "https://api.powerbi.com/v1.0/myorg/admin/dataflows",
        body=get_dataflows_as_admin,
        match=[
            matchers.query_param_matcher(params),
        ],
        content_type="application/json",
    )

    dataflows = admin.dataflows(top=1, skip=3)


@responses.activate
def test_add_encryption_key(admin, add_power_bi_encryption_key):
    json_params = {
        "name": "Contoso Sales",
        "keyVaultKeyIdentifier": "https://contoso-vault2.vault.azure.net/keys/ContosoKeyVault/b2ab4ba1c7b341eea5ecaaa2wb54c4d2",
        "activate": True,
        "isDefault": True,
    }

    responses.post(
        "https://api.powerbi.com/v1.0/myorg/admin/tenantKeys",
        body=add_power_bi_encryption_key,
        match=[
            matchers.json_params_matcher(json_params),
        ],
        content_type="application/json",
    )

    encryption_key = admin.add_encryption_key(
        name="Contoso Sales",
        key_vault_identifier="https://contoso-vault2.vault.azure.net/keys/ContosoKeyVault/b2ab4ba1c7b341eea5ecaaa2wb54c4d2",
        activate=True,
        is_default=True,
    )

    assert isinstance(encryption_key, dict)


@responses.activate
def test_dashboard_subscriptions(admin, get_dashboard_subscriptions_as_admin):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/admin/dashboards/69ffaa6c-b36d-4d01-96f5-1ed67c64d4af/subscriptions",
        body=get_dashboard_subscriptions_as_admin,
        content_type="application/json",
    )

    subscriptions = admin.dashboard_subscriptions(
        dashboard="69ffaa6c-b36d-4d01-96f5-1ed67c64d4af"
    )

    assert isinstance(subscriptions, list)
    assert all(isinstance(subscription, dict) for subscription in subscriptions)


@responses.activate
def test_dashboard_users(admin, get_dashboard_users_as_admin):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/admin/dashboards/69ffaa6c-b36d-4d01-96f5-1ed67c64d4af/users",
        body=get_dashboard_users_as_admin,
        content_type="application/json",
    )

    users = admin.dashboard_users(dashboard="69ffaa6c-b36d-4d01-96f5-1ed67c64d4af")

    assert isinstance(users, list)
    assert all(isinstance(user, dict) for user in users)


@responses.activate
def test_dashboard_tiles(admin, get_tiles_as_admin):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/admin/dashboards/69ffaa6c-b36d-4d01-96f5-1ed67c64d4af/tiles",
        body=get_tiles_as_admin,
        content_type="application/json",
    )

    dashboard = Dashboard(
        id="69ffaa6c-b36d-4d01-96f5-1ed67c64d4af",
        session=requests.Session(),
    )

    tiles = admin.dashboard_tiles(dashboard)

    assert isinstance(tiles, list)
    assert all(isinstance(tile, Tile) for tile in tiles)


@responses.activate
def test_dataset_datasources(admin, get_datasources_as_admin):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/admin/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229/datasources",
        body=get_datasources_as_admin,
        content_type="application/json",
    )

    datasources = admin.dataset_datasources("cfafbeb1-8037-4d0c-896e-a46fb27ff229")

    assert isinstance(datasources, list)
    assert all(isinstance(datasource, dict) for datasource in datasources)


@responses.activate
def test_encryption_keys(admin, get_power_bi_encryption_keys):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/admin/tenantKeys",
        body=get_power_bi_encryption_keys,
        content_type="application/json",
    )

    encryption_keys = admin.encryption_keys()

    assert isinstance(encryption_keys, list)
    assert all(isinstance(encryption_key, dict) for encryption_key in encryption_keys)


@responses.activate
def test_add_group_user(admin):
    json_params = {
        "identifier": "john@contoso.com",
        "principalType": "User",
        "groupUserAccessRight": "Admin",
    }

    responses.post(
        "https://api.powerbi.com/v1.0/myorg/admin/groups/206d27ca-94e8-4a69-855b-5c32bdd458a8/users",
        match=[
            matchers.json_params_matcher(json_params),
        ],
    )

    admin.add_group_user(
        group="206d27ca-94e8-4a69-855b-5c32bdd458a8",
        identifier="john@contoso.com",
        principal_type="User",
        group_user_access_right="Admin",
    )


@responses.activate
def test_add_group_user_with_optional_params(admin):
    json_params = {
        "identifier": "john@contoso.com",
        "principalType": "User",
        "groupUserAccessRight": "Admin",
        "emailAddress": "john@contoso.com",
    }

    responses.post(
        "https://api.powerbi.com/v1.0/myorg/admin/groups/206d27ca-94e8-4a69-855b-5c32bdd458a8/users",
        match=[
            matchers.json_params_matcher(json_params),
        ],
    )

    admin.add_group_user(
        group="206d27ca-94e8-4a69-855b-5c32bdd458a8",
        identifier="john@contoso.com",
        principal_type="User",
        group_user_access_right="Admin",
        email_address="john@contoso.com",
    )


@responses.activate
def test_delete_group_user(admin):
    responses.delete(
        "https://api.powerbi.com/v1.0/myorg/admin/groups/f7d76f5a-7190-43c6-bf12-7a135c6c2d69/users/john@contoso.com"
    )

    admin.delete_group_user(
        "f7d76f5a-7190-43c6-bf12-7a135c6c2d69",
        "john@contoso.com",
    )


@responses.activate
def test_delete_group_user_with_params(admin):
    params = {"profileId": "154aef10-47b8-48c4-ab97-f0bf9d5f8fcf"}

    responses.delete(
        "https://api.powerbi.com/v1.0/myorg/admin/groups/f7d76f5a-7190-43c6-bf12-7a135c6c2d69/users/john@contoso.com",
        match=[
            matchers.query_param_matcher(params),
        ],
    )

    admin.delete_group_user(
        "f7d76f5a-7190-43c6-bf12-7a135c6c2d69",
        "john@contoso.com",
        profile_id="154aef10-47b8-48c4-ab97-f0bf9d5f8fcf",
    )


@responses.activate
def test_group(admin):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/admin/groups/a2f89923-421a-464e-bf4c-25eab39bb09f",
        body="""{"id": "a2f89923-421a-464e-bf4c-25eab39bb09f"}""",
        content_type="application/json",
    )

    group = admin.group("a2f89923-421a-464e-bf4c-25eab39bb09f")

    assert isinstance(group, Group)


@responses.activate
def test_groups(admin, get_groups_as_admin):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/admin/groups?$top=1",
        body=get_groups_as_admin,
        content_type="application/json",
    )

    groups = admin.groups(top=1)

    assert isinstance(groups, list)
    assert all(isinstance(group, Group) for group in groups)


@responses.activate
def test_groups_without_top(admin, get_groups_as_admin):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/admin/groups",
        body=get_groups_as_admin,
        content_type="application/json",
        match=[
            matchers.query_param_matcher({"$top": 5000}),
        ],
    )

    groups = admin.groups()

    assert isinstance(groups, list)
    assert all(isinstance(group, Group) for group in groups)


@responses.activate
def test_groups_with_params(admin, get_groups_as_admin_with_expand):
    params = {
        "$expand": "dashboards",
        "$top": 100,
    }

    responses.get(
        "https://api.powerbi.com/v1.0/myorg/admin/groups",
        body=get_groups_as_admin_with_expand,
        match=[
            matchers.query_param_matcher(params),
        ],
        content_type="application/json",
    )

    groups = admin.groups(expand="dashboards", top=100)

    assert isinstance(groups, list)
    assert all(isinstance(group, Group) for group in groups)
    assert hasattr(groups[0], "dashboards")
    assert isinstance(groups[0].dashboards, list)


@responses.activate
def test_group_users(admin, get_group_users_as_admin):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/admin/groups/f089354e-8366-4e18-aea3-4cb4a3a50b48/users",
        body=get_group_users_as_admin,
        content_type="application/json",
    )

    users = admin.group_users("f089354e-8366-4e18-aea3-4cb4a3a50b48")

    assert isinstance(users, list)
    assert all(isinstance(user, dict) for user in users)


@responses.activate
def test_restore_group(admin):
    json_params = {
        "name": "Restored Workspace",
        "emailAddress": "john@contoso.com",
    }

    responses.post(
        "https://api.powerbi.com/v1.0/myorg/admin/groups/3bec11ee-48a9-490c-8e4d-1ebba90d491a/restore",
        match=[
            matchers.json_params_matcher(json_params),
        ],
    )

    admin.restore_group(
        "3bec11ee-48a9-490c-8e4d-1ebba90d491a",
        email_address="john@contoso.com",
        name="Restored Workspace",
    )


@responses.activate
def test_update_group_log_analytics_workspace_none(admin):
    json_params = {
        "logAnalyticsWorkspace": None,
    }

    responses.patch(
        "https://api.powerbi.com/v1.0/myorg/admin/groups/e2284830-c8dc-416b-b19a-8cdcd2729332",
        match=[
            matchers.json_params_matcher(json_params),
        ],
    )

    admin.update_group(
        group="e2284830-c8dc-416b-b19a-8cdcd2729332",
        log_analytics_workspace=None,
    )


@responses.activate
def test_update_group_multi(admin):
    json_params = {
        "name": "New Group Name",
        "logAnalyticsWorkspace": None,
    }

    responses.patch(
        "https://api.powerbi.com/v1.0/myorg/admin/groups/e2284830-c8dc-416b-b19a-8cdcd2729332",
        match=[
            matchers.json_params_matcher(json_params),
        ],
    )

    admin.update_group(
        group="e2284830-c8dc-416b-b19a-8cdcd2729332",
        name="New Group Name",
        log_analytics_workspace=None,
    )


def test_update_group_raises(admin):
    with pytest.raises(ValueError):
        admin.update_group(group="e2284830-c8dc-416b-b19a-8cdcd2729332")


@responses.activate
def test_report_subscriptions_call(admin, get_report_subscriptions_as_admin):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/admin/reports/5b218778-e7a5-4d73-8187-f10824047715/subscriptions",
        body=get_report_subscriptions_as_admin,
        content_type="application/json",
    )

    subscriptions = admin.report_subscriptions("5b218778-e7a5-4d73-8187-f10824047715")

    assert isinstance(subscriptions, list)
    assert all(isinstance(subscription, dict) for subscription in subscriptions)


@responses.activate
def test_report_users(admin, get_report_users_as_admin):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/admin/reports/5b218778-e7a5-4d73-8187-f10824047715/users",
        body=get_report_users_as_admin,
        content_type="application/json",
    )

    users = admin.report_users("5b218778-e7a5-4d73-8187-f10824047715")

    assert isinstance(users, list)
    assert all(isinstance(user, dict) for user in users)


@responses.activate
def test_reports(admin, get_reports_as_admin):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/admin/reports",
        body=get_reports_as_admin,
        content_type="application/json",
    )

    reports = admin.reports()

    assert isinstance(reports, list)
    assert all(isinstance(report, Report) for report in reports)

    assert reports[0].group_id == "278e22a3-2aee-4057-886d-c3225423bc10"
    assert reports[0].group_id == reports[0].workspace_id


@responses.activate
def test_reports_with_group(admin, get_reports_in_group_as_admin):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/admin/groups/f089354e-8366-4e18-aea3-4cb4a3a50b48/reports",
        body=get_reports_in_group_as_admin,
        content_type="application/json",
    )

    reports = admin.reports(group="f089354e-8366-4e18-aea3-4cb4a3a50b48")

    assert isinstance(reports, list)
    assert all(isinstance(report, Report) for report in reports)

    assert reports[0].group_id == "f089354e-8366-4e18-aea3-4cb4a3a50b48"
    assert not hasattr(reports[0], "workspace_id")


@responses.activate(registry=OrderedRegistry)
def test_activity_events(admin, get_activity_events):
    initial_response = responses.get(
        "https://api.powerbi.com/v1.0/myorg/admin/activityevents",
        body=get_activity_events[0],
        match=[
            matchers.query_param_matcher(
                {
                    "startDateTime": "'2019-08-31T00:00:00'",
                    "endDateTime": "'2019-08-31T23:59:59'",
                }
            )
        ],
        content_type="application/json",
    )

    next_response_1 = responses.get(
        "https://api.powerbi.com/v1.0/myorg/admin/activityevents",
        body=get_activity_events[1],
        match=[
            matchers.query_param_matcher(
                {
                    "continuationToken": "'%2BRID%3A244SAKlHY7YQAAAAAAAAAA%3D%3D%23RT%3A1%23TRC%3A5%23FPC%3AARAAAAAAAAAAFwAAAAAAAAA%3D'"
                }
            )
        ],
        content_type="application/json",
    )

    next_response_2 = responses.get(
        "https://api.powerbi.com/v1.0/myorg/admin/activityevents",
        body=get_activity_events[2],
        match=[
            matchers.query_param_matcher(
                {
                    "continuationToken": "'%2BRID%$4Z244SAKlHY7YQAAAAAAAAAA%3D%3D%23RT%3A1%23TRC%3A5%23FPC%3AARAAAAAAAAAAFwAAAAAAAAA%3D'"
                }
            )
        ],
        content_type="application/json",
    )

    start = datetime(2019, 8, 31, 0, 0, 0)
    end = datetime(2019, 8, 31, 23, 59, 59)

    activity_events = admin.activity_events(start, end)

    assert initial_response.call_count == 1
    assert next_response_1.call_count == 1
    assert next_response_2.call_count == 1

    assert isinstance(activity_events, list)
    assert all(isinstance(activity_event, dict) for activity_event in activity_events)
    assert len(activity_events) == 6
    assert activity_events[5]["Id"] == "1db4c464-3e5d-4a89-b412-c2ce6fbae88e"


@responses.activate
def test_workspaces(admin, get_modified_workspaces):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/admin/workspaces/modified",
        body=get_modified_workspaces,
        content_type="application/json",
    )

    workspaces = admin.workspaces()

    assert isinstance(workspaces, list)
    assert len(workspaces) == 2
    assert all(workspace.get("Id") for workspace in workspaces)
    assert workspaces[0].get("Id") == "3740504d-1f93-42f9-8e9d-c8ba9b787a3b"


@responses.activate
def test_workspaces_modified_since(admin, get_modified_workspaces):
    params = {"modifiedSince": "2020-10-02T05:51:30.0000000Z"}

    responses.get(
        "https://api.powerbi.com/v1.0/myorg/admin/workspaces/modified",
        body=get_modified_workspaces,
        content_type="application/json",
        match=[
            matchers.query_param_matcher(params),
        ],
    )

    modified_since = datetime(2020, 10, 2, 5, 51, 30)

    workspaces = admin.workspaces(modified_since=modified_since)

    assert isinstance(workspaces, list)
    assert len(workspaces) == 2
    assert all(workspace.get("Id") for workspace in workspaces)
    assert workspaces[0].get("Id") == "3740504d-1f93-42f9-8e9d-c8ba9b787a3b"


@responses.activate
def test_workspaces_params(admin, get_modified_workspaces):
    params = params = {
        "modifiedSince": "2020-10-02T05:51:30.0000000Z",
        "excludeInActiveWorkspaces": False,
        "excludePersonalWorkspaces": True,
    }

    responses.get(
        "https://api.powerbi.com/v1.0/myorg/admin/workspaces/modified",
        body=get_modified_workspaces,
        content_type="application/json",
        match=[
            matchers.query_param_matcher(params),
        ],
    )

    modified_since = datetime(2020, 10, 2, 5, 51, 30)

    workspaces = admin.workspaces(
        modified_since=modified_since,
        exclude_inactive_workspaces=False,
        exclude_personal_workspaces=True,
    )

    assert isinstance(workspaces, list)
    assert len(workspaces) == 2
    assert all(workspace.get("Id") for workspace in workspaces)
    assert workspaces[0].get("Id") == "3740504d-1f93-42f9-8e9d-c8ba9b787a3b"


@responses.activate
def test_initiate_scan(admin, post_workspace_info):
    json_params = {
        "workspaces": [
            "97d03602-4873-4760-b37e-1563ef5358e3",
        ]
    }

    responses.post(
        "https://api.powerbi.com/v1.0/myorg/admin/workspaces/getInfo",
        body=post_workspace_info,
        match=[
            matchers.json_params_matcher(json_params),
        ],
        content_type="application/json",
    )

    workspaces = "97d03602-4873-4760-b37e-1563ef5358e3"

    scan_request = admin.initiate_scan(workspaces)

    assert isinstance(scan_request, dict)
    assert scan_request["id"] == "e7d03602-4873-4760-b37e-1563ef5358e3"
    assert scan_request["createdDateTime"] == "2020-06-15T16:46:28.0487687Z"
    assert scan_request["status"] == "NotStarted"


@responses.activate
def test_initiate_scan_params(admin, post_workspace_info):
    json_params = {
        "workspaces": [
            "97d03602-4873-4760-b37e-1563ef5358e3",
            "67b7e93a-3fb3-493c-9e41-2c5051008f24",
        ]
    }

    params = {
        "datasetExpressions": True,
        "lineage": True,
        "datasourceDetails": False,
    }

    responses.post(
        "https://api.powerbi.com/v1.0/myorg/admin/workspaces/getInfo",
        body=post_workspace_info,
        match=[
            matchers.json_params_matcher(json_params),
            matchers.query_param_matcher(params),
        ],
        content_type="application/json",
    )

    workspaces = [
        "97d03602-4873-4760-b37e-1563ef5358e3",
        "67b7e93a-3fb3-493c-9e41-2c5051008f24",
    ]

    scan_request = admin.initiate_scan(
        workspaces,
        lineage=True,
        dataset_expressions=True,
        datasource_details=False,
    )

    assert isinstance(scan_request, dict)
    assert scan_request["id"] == "e7d03602-4873-4760-b37e-1563ef5358e3"
    assert scan_request["createdDateTime"] == "2020-06-15T16:46:28.0487687Z"
    assert scan_request["status"] == "NotStarted"


@responses.activate
def test_scan_status(admin, get_scan_status):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/admin/workspaces/scanStatus/e7d03602-4873-4760-b37e-1563ef5358e3",
        body=get_scan_status,
        content_type="application/json",
    )

    scan_status = admin.scan_status("e7d03602-4873-4760-b37e-1563ef5358e3")

    assert isinstance(scan_status, dict)
    assert scan_status["id"] == "e7d03602-4873-4760-b37e-1563ef5358e3"
    assert scan_status["status"] == "Succeeded"


@responses.activate
def test_scan_result(admin, get_scan_result):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/admin/workspaces/scanResult/e7d03602-4873-4760-b37e-1563ef5358e3",
        body=get_scan_result,
        content_type="application/json",
    )

    scan_result = admin.scan_result("e7d03602-4873-4760-b37e-1563ef5358e3")

    assert isinstance(scan_result, dict)
    assert len(scan_result["workspaces"]) == 1
    assert scan_result["workspaces"][0]["id"] == "d507422c-8d6d-4361-ac7a-30074a8cd0a1"
    assert all(
        k in scan_result["workspaces"][0].keys()
        for k in ("reports", "dashboards", "datasets", "dataflows")
    )
