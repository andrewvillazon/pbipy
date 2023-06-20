import pytest
import requests
import responses

from pbipy.reports import Report


@pytest.fixture
def report_with_group():
    raw = {
        "datasetId": "cfafbeb1-8037-4d0c-896e-a46fb27ff229",
        "id": "cfafbeb1-8037-4d0c-896e-a46fb27ff229",
        "name": "SalesMarketing",
        "webUrl": "https://app.powerbi.com//reports/5b218778-e7a5-4d73-8187-f10824047715",
        "embedUrl": "https://app.powerbi.com/reportEmbed?reportId=5b218778-e7a5-4d73-8187-f10824047715",
    }

    report = Report(
        id=raw["id"],
        group_id="f089354e-8366-4e18-aea3-4cb4a3a50b48",
        session=requests.Session(),
        raw=raw,
    )

    return report


def test_report_creation_from_raw():
    raw = {
        "datasetId": "cfafbeb1-8037-4d0c-896e-a46fb27ff229",
        "id": "5b218778-e7a5-4d73-8187-f10824047715",
        "name": "SalesMarketing",
        "webUrl": "https://app.powerbi.com/groups/f089354e-8366-4e18-aea3-4cb4a3a50b48/reports/5b218778-e7a5-4d73-8187-f10824047715",
        "embedUrl": "https://app.powerbi.com/reportEmbed?reportId=5b218778-e7a5-4d73-8187-f10824047715&groupId=f089354e-8366-4e18-aea3-4cb4a3a50b48",
    }

    report = Report(raw.get("id"), session=requests.Session(), raw=raw)

    assert report.id == "5b218778-e7a5-4d73-8187-f10824047715"
    assert report.name == "SalesMarketing"


@responses.activate
def test_datasources(report_with_group, get_datasources_in_group):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/groups/f089354e-8366-4e18-aea3-4cb4a3a50b48/reports/cfafbeb1-8037-4d0c-896e-a46fb27ff229/datasources",
        body=get_datasources_in_group,
        content_type="application/json",
    )

    datasources = report_with_group.datasources()

    assert isinstance(datasources, list)
    assert all(isinstance(datasource, dict) for datasource in datasources)
    assert len(datasources) == 1
    assert datasources[0]["datasourceId"] == "f8c56590-43cb-43bf-8daa-233ba2520f55"


@responses.activate
def test_page(get_page):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/reports/879445d6-3a9e-4a74-b5ae-7c0ddabf0f11/pages/ReportSection",
        body=get_page,
        content_type="application/json",
    )

    report = Report(
        id="879445d6-3a9e-4a74-b5ae-7c0ddabf0f11",
        session=requests.Session(),
    )

    page = report.page("ReportSection")

    assert isinstance(page, dict)
    assert page["displayName"] == "Regional Sales Analysis"
