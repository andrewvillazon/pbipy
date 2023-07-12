import pytest
import requests
import responses
from responses import matchers

from pbipy.apps import App
from pbipy.dashboards import Dashboard
from pbipy.dataflows import Dataflow
from pbipy.datasets import Dataset
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
