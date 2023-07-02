import pytest
import requests
import responses
from requests.exceptions import HTTPError
from pbipy.apps import App

from pbipy.groups import Group
from pbipy.reports import Report


@responses.activate
def test_get_dataset_calls_correct_get_dataset_url(powerbi, get_dataset):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229",
        body=get_dataset,
        content_type="application/json",
    )

    powerbi.dataset("cfafbeb1-8037-4d0c-896e-a46fb27ff229")


@responses.activate
def test_get_dataset_calls_correct_get_dataset_in_group_url(powerbi, get_dataset):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/groups/f089354e-8366-4e18-aea3-4cb4a3a50b48/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229",
        body=get_dataset,
        content_type="application/json",
    )

    powerbi.dataset(
        "cfafbeb1-8037-4d0c-896e-a46fb27ff229",
        group="f089354e-8366-4e18-aea3-4cb4a3a50b48",
    )


@responses.activate
def test_get_dataset_properties_are_set(powerbi, get_dataset):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229",
        body=get_dataset,
        content_type="application/json",
    )

    dataset = powerbi.dataset("cfafbeb1-8037-4d0c-896e-a46fb27ff229")

    assert dataset.id == "cfafbeb1-8037-4d0c-896e-a46fb27ff229"
    assert dataset.name == "SalesMarketing"
    assert dataset.add_rows_api_enabled == False
    assert dataset.configured_by == "john@contoso.com"
    assert dataset.group_id == None
    assert dataset.is_refreshable == True


@responses.activate
def test_get_dataset_group_property_is_set(powerbi, get_dataset):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/groups/f089354e-8366-4e18-aea3-4cb4a3a50b48/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229",
        body=get_dataset,
        content_type="application/json",
    )

    dataset = powerbi.dataset(
        "cfafbeb1-8037-4d0c-896e-a46fb27ff229",
        group="f089354e-8366-4e18-aea3-4cb4a3a50b48",
    )

    assert dataset.group_id == "f089354e-8366-4e18-aea3-4cb4a3a50b48"


@responses.activate
def test_get_datasets_calls_correct_get_datasets_url(powerbi, get_datasets):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/datasets",
        body=get_datasets,
        content_type="application/json",
    )

    powerbi.datasets()


@responses.activate
def test_get_datasets_calls_correct_get_datasets_in_group_url(powerbi, get_datasets):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/groups/f089354e-8366-4e18-aea3-4cb4a3a50b48/datasets",
        body=get_datasets,
        content_type="application/json",
    )

    powerbi.datasets(group="f089354e-8366-4e18-aea3-4cb4a3a50b48")


@responses.activate
def test_get_datasets_sets_group_property(powerbi, get_datasets):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/groups/f089354e-8366-4e18-aea3-4cb4a3a50b48/datasets",
        body=get_datasets,
        content_type="application/json",
    )

    datasets = powerbi.datasets(group="f089354e-8366-4e18-aea3-4cb4a3a50b48")

    assert all(hasattr(dataset, "group_id") for dataset in datasets)
    assert all(
        getattr(dataset, "group_id") == "f089354e-8366-4e18-aea3-4cb4a3a50b48"
        for dataset in datasets
    )


@responses.activate
def test_get_datasets_sets_js_property(powerbi, get_datasets):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/groups/f089354e-8366-4e18-aea3-4cb4a3a50b48/datasets",
        body=get_datasets,
        content_type="application/json",
    )

    datasets = powerbi.datasets(group="f089354e-8366-4e18-aea3-4cb4a3a50b48")

    assert all(hasattr(dataset, "raw") for dataset in datasets)


@responses.activate
def test_delete_dataset_call(powerbi):
    responses.delete(
        "https://api.powerbi.com/v1.0/myorg/groups/f089354e-8366-4e18-aea3-4cb4a3a50b48/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229"
    )

    powerbi.delete_dataset(
        "cfafbeb1-8037-4d0c-896e-a46fb27ff229",
        group="f089354e-8366-4e18-aea3-4cb4a3a50b48",
    )


@responses.activate
def test_delete_dataset_raises_http_error(powerbi):
    responses.delete(
        "https://api.powerbi.com/v1.0/myorg/groups/f089354e-8366-4e18-aea3-4cb4a3a50b48/datasets/cfafbeb1-8037-4d0c-896e-a46fb27ff229",
        status=400,
        body="{}",
    )

    with pytest.raises(HTTPError):
        powerbi.delete_dataset(
            "cfafbeb1-8037-4d0c-896e-a46fb27ff229",
            group="f089354e-8366-4e18-aea3-4cb4a3a50b48",
        )


@responses.activate
def test_groups_call_with_params(powerbi, get_groups):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/groups?$filter=contains(name,'marketing')%20or%20name%20eq%20'contoso'",
        body=get_groups,
        content_type="application/json",
    )

    powerbi.groups(filter="contains(name,'marketing') or name eq 'contoso'")


@responses.activate
def test_groups_result(powerbi, get_groups):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/groups",
        body=get_groups,
        content_type="application/json",
    )

    groups = powerbi.groups()

    assert isinstance(groups, list)
    assert all(isinstance(group, Group) for group in groups)


@responses.activate
def test_group(powerbi, get_group):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/groups?$filter=id%20eq%20'a2f89923-421a-464e-bf4c-25eab39bb09f'",
        body=get_group,
        content_type="application/json",
    )

    powerbi.group("a2f89923-421a-464e-bf4c-25eab39bb09f")


@responses.activate
def test_group_raises(powerbi):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/groups?$filter=id%20eq%20'a2f89923-421a-464e-bf4c-25eab39bb09f'",
        body="{value:[]}",
        content_type="application/json",
    )

    with pytest.raises(ValueError):
        powerbi.group("a2f89923-421a-464e-bf4c-25eab39bb09f")


@responses.activate
def test_delete_group_call_with_group_object(powerbi):
    responses.delete(
        "https://api.powerbi.com/v1.0/myorg/groups/f089354e-8366-4e18-aea3-4cb4a3a50b48"
    )

    group = Group(
        "f089354e-8366-4e18-aea3-4cb4a3a50b48",
        session=requests.Session(),
    )

    powerbi.delete_group(group)


@responses.activate
def test_delete_group_call(powerbi):
    responses.delete(
        "https://api.powerbi.com/v1.0/myorg/groups/f089354e-8366-4e18-aea3-4cb4a3a50b48"
    )

    powerbi.delete_group("f089354e-8366-4e18-aea3-4cb4a3a50b48")


@responses.activate
def test_report_call(powerbi, get_report):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/reports/5b218778-e7a5-4d73-8187-f10824047715",
        body=get_report,
        content_type="application/json",
    )

    powerbi.report("5b218778-e7a5-4d73-8187-f10824047715")


@responses.activate
def test_report_call_with_group(powerbi, get_report):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/groups/f089354e-8366-4e18-aea3-4cb4a3a50b48/reports/5b218778-e7a5-4d73-8187-f10824047715",
        body=get_report,
        content_type="application/json",
    )

    powerbi.report(
        report="5b218778-e7a5-4d73-8187-f10824047715",
        group="f089354e-8366-4e18-aea3-4cb4a3a50b48",
    )


@responses.activate
def test_report_call_result(powerbi, get_report):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/groups/f089354e-8366-4e18-aea3-4cb4a3a50b48/reports/5b218778-e7a5-4d73-8187-f10824047715",
        body=get_report,
        content_type="application/json",
    )

    report = powerbi.report(
        report="5b218778-e7a5-4d73-8187-f10824047715",
        group="f089354e-8366-4e18-aea3-4cb4a3a50b48",
    )

    assert isinstance(report, Report)
    assert hasattr(report, "group_id")
    assert report.group_id == "f089354e-8366-4e18-aea3-4cb4a3a50b48"
    assert report.name == "SalesMarketing"


@responses.activate
def test_reports_call(powerbi, get_reports_in_group):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/groups/f089354e-8366-4e18-aea3-4cb4a3a50b48/reports",
        body=get_reports_in_group,
        content_type="application/json",
    )

    powerbi.reports(group="f089354e-8366-4e18-aea3-4cb4a3a50b48")


@responses.activate
def test_reports_call_group_object(powerbi, get_reports_in_group):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/groups/f089354e-8366-4e18-aea3-4cb4a3a50b48/reports",
        body=get_reports_in_group,
        content_type="application/json",
    )

    group = Group(
        "f089354e-8366-4e18-aea3-4cb4a3a50b48",
        requests.Session(),
    )

    powerbi.reports(group=group)


@responses.activate
def test_reports_result(powerbi, get_reports_in_group):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/groups/f089354e-8366-4e18-aea3-4cb4a3a50b48/reports",
        body=get_reports_in_group,
        content_type="application/json",
    )

    reports = powerbi.reports(group="f089354e-8366-4e18-aea3-4cb4a3a50b48")

    assert isinstance(reports, list)
    assert all(isinstance(report, Report) for report in reports)


@responses.activate
def test_delete_report_call_report_str_no_group(powerbi):
    responses.delete(
        "https://api.powerbi.com/v1.0/myorg/reports/5b218778-e7a5-4d73-8187-f10824047715",
    )

    powerbi.delete_report("5b218778-e7a5-4d73-8187-f10824047715")


@responses.activate
def test_delete_report_call_report_object_ignore_group(powerbi):
    responses.delete(
        "https://api.powerbi.com/v1.0/myorg/reports/5b218778-e7a5-4d73-8187-f10824047715",
    )

    report = Report(
        id="5b218778-e7a5-4d73-8187-f10824047715",
        session=requests.Session(),
    )

    powerbi.delete_report(
        report,
        group="f089354e-8366-4e18-aea3-4cb4a3a50b48",
    )


@responses.activate
def test_delete_report_call_report_str_group_object(powerbi):
    responses.delete(
        "https://api.powerbi.com/v1.0/myorg/groups/f089354e-8366-4e18-aea3-4cb4a3a50b48/reports/5b218778-e7a5-4d73-8187-f10824047715",
    )

    group = Group(
        "f089354e-8366-4e18-aea3-4cb4a3a50b48",
        requests.Session(),
    )

    powerbi.delete_report(
        "5b218778-e7a5-4d73-8187-f10824047715",
        group=group,
    )


@responses.activate
def test_delete_report_call_report_object_with_group_ignore_group_id(powerbi):
    responses.delete(
        "https://api.powerbi.com/v1.0/myorg/groups/f089354e-8366-4e18-aea3-4cb4a3a50b48/reports/5b218778-e7a5-4d73-8187-f10824047715",
    )

    report = Report(
        id="5b218778-e7a5-4d73-8187-f10824047715",
        group_id="f089354e-8366-4e18-aea3-4cb4a3a50b48",
        session=requests.Session(),
    )

    powerbi.delete_report(
        report,
        group="3d9b93c6-7b6d-4801-a491-1738910904fd",
    )


@responses.activate
def test_app(get_app, powerbi):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/apps/f089354e-8366-4e18-aea3-4cb4a3a50b48",
        body=get_app,
        content_type="application/json"
    )

    app = powerbi.app("f089354e-8366-4e18-aea3-4cb4a3a50b48")

    assert isinstance(app, App)
    assert app.id == "f089354e-8366-4e18-aea3-4cb4a3a50b48"