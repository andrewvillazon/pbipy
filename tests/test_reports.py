from io import BytesIO
from pathlib import Path
from unittest.mock import mock_open, patch

import pytest
import requests
import responses
from responses import matchers

from pbipy.embedtokens import EmbedToken
from pbipy.groups import Group
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


@pytest.fixture
def report():
    raw = {
        "id": "879445d6-3a9e-4a74-b5ae-7c0ddabf0f11",
        "name": "SalesMarketing",
        "reportType": "PowerBIReport",
    }

    report = Report(
        id=raw["id"],
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


@responses.activate
def test_pages(report, get_pages):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/reports/879445d6-3a9e-4a74-b5ae-7c0ddabf0f11/pages",
        body=get_pages,
        content_type="application/json",
    )

    pages = report.pages()

    assert isinstance(pages, list)
    assert all(isinstance(page, dict) for page in pages)
    assert len(pages) == 2


@responses.activate
def test_rebind_call(report):
    json_params = {"datasetId": "cfafbeb1-8037-4d0c-896e-a46fb27ff229"}

    responses.post(
        "https://api.powerbi.com/v1.0/myorg/reports/879445d6-3a9e-4a74-b5ae-7c0ddabf0f11/Rebind",
        match=[
            matchers.json_params_matcher(json_params),
        ],
    )

    report.rebind("cfafbeb1-8037-4d0c-896e-a46fb27ff229")


@responses.activate
def test_take_over_call(report_with_group):
    responses.post(
        "https://api.powerbi.com/v1.0/myorg/groups/f089354e-8366-4e18-aea3-4cb4a3a50b48/reports/cfafbeb1-8037-4d0c-896e-a46fb27ff229/Default.TakeOver"
    )

    report_with_group.take_over()


def test_take_over_raises_type_error(report):
    with pytest.raises(TypeError):
        report.take_over()


@responses.activate
def test_update_datasources_call_single(report):
    json_params = [
        {
            "datasourceName": "SqlDatasource",
            "connectionDetails": {
                "server": "New-Sql-Server",
                "database": "New-Sql-Database",
            },
        },
    ]

    responses.post(
        "https://api.powerbi.com/v1.0/myorg/reports/879445d6-3a9e-4a74-b5ae-7c0ddabf0f11/Default.UpdateDatasources",
        match=[
            matchers.json_params_matcher(json_params),
        ],
    )

    details = {
        "datasourceName": "SqlDatasource",
        "connectionDetails": {
            "server": "New-Sql-Server",
            "database": "New-Sql-Database",
        },
    }

    report.update_datasources(details)


@responses.activate
def test_update_datasources_call_multiple(report):
    json_params = [
        {
            "datasourceName": "SqlDatasource",
            "connectionDetails": {
                "server": "New-Sql-Server",
                "database": "New-Sql-Database",
            },
        },
        {
            "datasourceName": "SqlAzureDatasource",
            "connectionDetails": {
                "server": "New-SqlAzure-Server.windows.net",
                "database": "New-SqlAzure-Database",
            },
        },
    ]

    responses.post(
        "https://api.powerbi.com/v1.0/myorg/reports/879445d6-3a9e-4a74-b5ae-7c0ddabf0f11/Default.UpdateDatasources",
        match=[
            matchers.json_params_matcher(json_params),
        ],
    )

    details = [
        {
            "datasourceName": "SqlDatasource",
            "connectionDetails": {
                "server": "New-Sql-Server",
                "database": "New-Sql-Database",
            },
        },
        {
            "datasourceName": "SqlAzureDatasource",
            "connectionDetails": {
                "server": "New-SqlAzure-Server.windows.net",
                "database": "New-SqlAzure-Database",
            },
        },
    ]

    report.update_datasources(details)


@responses.activate
def test_update_content_report_object(report):
    json_params = {
        "sourceReport": {
            "sourceReportId": "8e4d5880-81d6-4804-ab97-054665050799",
            "sourceWorkspaceId": "2f42a406-a075-4a15-bbf2-97ef958c94cb",
        },
        "sourceType": "ExistingReport",
    }

    responses.post(
        "https://api.powerbi.com/v1.0/myorg/reports/879445d6-3a9e-4a74-b5ae-7c0ddabf0f11/UpdateReportContent",
        match=[
            matchers.json_params_matcher(json_params),
        ],
    )

    source_report = Report(
        id="8e4d5880-81d6-4804-ab97-054665050799",
        group_id="2f42a406-a075-4a15-bbf2-97ef958c94cb",
        session=requests.Session(),
    )

    report.update_content(source_report)


@responses.activate
def test_update_content_report_no_group(report):
    json_params = {
        "sourceReport": {
            "sourceReportId": "8e4d5880-81d6-4804-ab97-054665050799",
        },
        "sourceType": "ExistingReport",
    }

    responses.post(
        "https://api.powerbi.com/v1.0/myorg/reports/879445d6-3a9e-4a74-b5ae-7c0ddabf0f11/UpdateReportContent",
        match=[
            matchers.json_params_matcher(json_params),
        ],
    )

    source_report = Report(
        id="8e4d5880-81d6-4804-ab97-054665050799",
        session=requests.Session(),
    )

    report.update_content(source_report)


@responses.activate
def test_update_content_report_str_group_object(report):
    json_params = {
        "sourceReport": {
            "sourceReportId": "8e4d5880-81d6-4804-ab97-054665050799",
            "sourceWorkspaceId": "2f42a406-a075-4a15-bbf2-97ef958c94cb",
        },
        "sourceType": "ExistingReport",
    }

    responses.post(
        "https://api.powerbi.com/v1.0/myorg/reports/879445d6-3a9e-4a74-b5ae-7c0ddabf0f11/UpdateReportContent",
        match=[
            matchers.json_params_matcher(json_params),
        ],
    )

    group = Group(
        id="2f42a406-a075-4a15-bbf2-97ef958c94cb",
        session=requests.Session(),
    )

    report.update_content(
        "8e4d5880-81d6-4804-ab97-054665050799",
        group,
    )


@responses.activate
def test_update_content_report_str_group_str(report):
    json_params = {
        "sourceReport": {
            "sourceReportId": "8e4d5880-81d6-4804-ab97-054665050799",
            "sourceWorkspaceId": "2f42a406-a075-4a15-bbf2-97ef958c94cb",
        },
        "sourceType": "ExistingReport",
    }

    responses.post(
        "https://api.powerbi.com/v1.0/myorg/reports/879445d6-3a9e-4a74-b5ae-7c0ddabf0f11/UpdateReportContent",
        match=[
            matchers.json_params_matcher(json_params),
        ],
    )

    report.update_content(
        "8e4d5880-81d6-4804-ab97-054665050799",
        "2f42a406-a075-4a15-bbf2-97ef958c94cb",
    )


@responses.activate
def test_update_content_ignores_group(report):
    # Report has no group, should ignore group id and not pass in as param.
    json_params = {
        "sourceReport": {
            "sourceReportId": "8e4d5880-81d6-4804-ab97-054665050799",
        },
        "sourceType": "ExistingReport",
    }

    responses.post(
        "https://api.powerbi.com/v1.0/myorg/reports/879445d6-3a9e-4a74-b5ae-7c0ddabf0f11/UpdateReportContent",
        match=[
            matchers.json_params_matcher(json_params),
        ],
    )

    source_report = Report(
        id="8e4d5880-81d6-4804-ab97-054665050799",
        session=requests.Session(),
    )

    report.update_content(source_report, "2f42a406-a075-4a15-bbf2-97ef958c94cb")


@responses.activate
def test_update_content_report_str_only_no_group(report):
    json_params = {
        "sourceReport": {
            "sourceReportId": "8e4d5880-81d6-4804-ab97-054665050799",
        },
        "sourceType": "ExistingReport",
    }

    responses.post(
        "https://api.powerbi.com/v1.0/myorg/reports/879445d6-3a9e-4a74-b5ae-7c0ddabf0f11/UpdateReportContent",
        match=[
            matchers.json_params_matcher(json_params),
        ],
    )

    report.update_content("8e4d5880-81d6-4804-ab97-054665050799")


@responses.activate
def test_clone_report_call_with_group(report_with_group):
    json_params = {
        "name": "Attack of the clones",
        "targetWorkspaceId": "2f42a406-a075-4a15-bbf2-97ef958c94cb",
    }

    responses.post(
        "https://api.powerbi.com/v1.0/myorg/groups/f089354e-8366-4e18-aea3-4cb4a3a50b48/reports/cfafbeb1-8037-4d0c-896e-a46fb27ff229/Clone",
        match=[
            matchers.json_params_matcher(json_params),
        ],
    )

    report_with_group.clone(
        "Attack of the clones",
        target_group="2f42a406-a075-4a15-bbf2-97ef958c94cb",
    )


@responses.activate
def test_clone_report_call_with_no_group(report_with_group):
    json_params = {
        "name": "Attack of the clones",
    }

    responses.post(
        "https://api.powerbi.com/v1.0/myorg/groups/f089354e-8366-4e18-aea3-4cb4a3a50b48/reports/cfafbeb1-8037-4d0c-896e-a46fb27ff229/Clone",
        match=[
            matchers.json_params_matcher(json_params),
        ],
    )

    report_with_group.clone("Attack of the clones")


@responses.activate
def test_clone_report_call_with_group_and_dataset(report_with_group):
    json_params = {
        "name": "Attack of the clones",
        "targetModelId": "8e4d5880-81d6-4804-ab97-054665050799",
        "targetWorkspaceId": "2f42a406-a075-4a15-bbf2-97ef958c94cb",
    }

    responses.post(
        "https://api.powerbi.com/v1.0/myorg/groups/f089354e-8366-4e18-aea3-4cb4a3a50b48/reports/cfafbeb1-8037-4d0c-896e-a46fb27ff229/Clone",
        match=[
            matchers.json_params_matcher(json_params),
        ],
    )

    report_with_group.clone(
        "Attack of the clones",
        target_group="2f42a406-a075-4a15-bbf2-97ef958c94cb",
        target_dataset="8e4d5880-81d6-4804-ab97-054665050799",
    )


@patch("pbipy.reports.urlopen")
def test_download(mock_urlopen, report):
    mock_urlopen.return_value = BytesIO()
    mo = mock_open()

    with patch("builtins.open", mo):
        report.download()

    expected_url = "https://api.powerbi.com/v1.0/myorg/reports/879445d6-3a9e-4a74-b5ae-7c0ddabf0f11/Export"
    actual_url = mock_urlopen.call_args.args[0].full_url
    expected_path = Path("SalesMarketing.pbix")

    assert actual_url == expected_url
    mo.assert_called_with(expected_path, "wb")


@patch("pbipy.reports.urlopen")
def test_download_with_dir(mock_urlopen, report):
    mock_urlopen.return_value = BytesIO()
    mo = mock_open()

    with patch("builtins.open", mo):
        report.download(save_to="C:/temp", file_name="NotSalesMarketing")

    expected_url = "https://api.powerbi.com/v1.0/myorg/reports/879445d6-3a9e-4a74-b5ae-7c0ddabf0f11/Export"
    actual_url = mock_urlopen.call_args.args[0].full_url
    expected_path = Path("C:/temp/NotSalesMarketing.pbix")

    assert actual_url == expected_url
    mo.assert_called_with(expected_path, "wb")


@responses.activate
def test_export_request_call(report, export_to_file):
    responses.post(
        "https://api.powerbi.com/v1.0/myorg/reports/879445d6-3a9e-4a74-b5ae-7c0ddabf0f11/ExportTo",
        match=[
            matchers.json_params_matcher(
                {"format": "PDF"},
            ),
        ],
        body=export_to_file,
        status=202,
    )

    report.export_request("pdf")


@responses.activate
def test_export_request_result(report, export_to_file):
    responses.post(
        "https://api.powerbi.com/v1.0/myorg/reports/879445d6-3a9e-4a74-b5ae-7c0ddabf0f11/ExportTo",
        match=[
            matchers.json_params_matcher(
                {"format": "PDF"},
            ),
        ],
        body=export_to_file,
        status=202,
    )

    export_job = report.export_request("pdf")

    assert isinstance(export_job, dict)
    assert export_job.get("percentComplete") == 70
    assert export_job.get("status") == "Running"


@responses.activate
def test_export_status_raw_only(report, get_export_to_file_status):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/reports/879445d6-3a9e-4a74-b5ae-7c0ddabf0f11/exports/Mi9C5419i....PS4=",
        body=get_export_to_file_status,
    )

    status = report.export_status("Mi9C5419i....PS4=")

    assert isinstance(status, dict)
    assert status.get("id") == "Mi9C5419i....PS4="
    assert status.get("status") == "Succeeded"
    assert status.get("percentComplete") == 100


@responses.activate
def test_export_status_retry_after(report, get_export_to_file_status):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/reports/879445d6-3a9e-4a74-b5ae-7c0ddabf0f11/exports/Mi9C5419i....PS4=",
        body=get_export_to_file_status,
        headers={"Retry-After": "5"},
    )

    status = report.export_status("Mi9C5419i....PS4=", include_retry_after=True)

    export_status, retry_after = status

    assert isinstance(status, tuple)
    assert isinstance(export_status, dict)
    assert isinstance(retry_after, int)


@responses.activate
def test_export_status_no_retry_after(report, get_export_to_file_status):
    responses.get(
        "https://api.powerbi.com/v1.0/myorg/reports/879445d6-3a9e-4a74-b5ae-7c0ddabf0f11/exports/Mi9C5419i....PS4=",
        body=get_export_to_file_status,
    )

    status = report.export_status("Mi9C5419i....PS4=", include_retry_after=True)

    export_status, retry_after = status

    assert isinstance(status, tuple)
    assert isinstance(export_status, dict)
    assert retry_after is None


@responses.activate
def test_download_export():
    response_file = BytesIO(b"file contents").read()

    responses.get(
        "https://api.powerbi.com/v1.0/myorg/reports/cfafbeb1-8037-4d0c-896e-a46fb27ff229/exports/Mi9C5419i....PS4=/file",
        body=response_file,
        content_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
    )

    raw = {
        "id": "cfafbeb1-8037-4d0c-896e-a46fb27ff229",
        "name": "SalesMarketing",
        "reportType": "PowerBIReport",
    }

    report = Report(
        id="cfafbeb1-8037-4d0c-896e-a46fb27ff229",
        session=requests.Session(),
        raw=raw,
    )

    m = mock_open()
    with patch("builtins.open", m):
        report.download_export("Mi9C5419i....PS4=")

    m.assert_called_with(Path("SalesMarketing.pptx"), "wb")
    m.return_value.write.assert_called_once_with(response_file)


@responses.activate
def test_download_export_pdf():
    response_file = BytesIO(b"file contents").read()

    responses.get(
        "https://api.powerbi.com/v1.0/myorg/reports/cfafbeb1-8037-4d0c-896e-a46fb27ff229/exports/Mi9C5419i....PS4=/file",
        body=response_file,
        content_type="application/pdf",
    )

    raw = {
        "id": "cfafbeb1-8037-4d0c-896e-a46fb27ff229",
        "name": "SalesMarketing",
        "reportType": "PowerBIReport",
    }

    report = Report(
        id="cfafbeb1-8037-4d0c-896e-a46fb27ff229",
        session=requests.Session(),
        raw=raw,
    )

    m = mock_open()
    with patch("builtins.open", m):
        report.download_export("Mi9C5419i....PS4=", "C:/temp")

    m.assert_called_with(Path("C:/temp/SalesMarketing.pdf"), "wb")
    m.return_value.write.assert_called_once_with(response_file)


@responses.activate
def test_generate_token(
    report_with_group,
    reports_generate_token_in_group,
):
    json_params = {
        "accessLevel": "Edit",
        "allowSaveAs": True,
    }

    responses.post(
        "https://api.powerbi.com/v1.0/myorg/groups/f089354e-8366-4e18-aea3-4cb4a3a50b48/reports/cfafbeb1-8037-4d0c-896e-a46fb27ff229/GenerateToken",
        body=reports_generate_token_in_group,
        content_type="application/json",
        match=[
            matchers.json_params_matcher(json_params),
        ],
    )

    token = report_with_group.generate_token(
        access_level="Edit",
        allow_save_as=True,
    )

    assert isinstance(token, EmbedToken)
    assert token.token == "H4sI....AAA="
    assert token.token_id == "49ae3742-54c0-4c29-af52-619ff93b5c80"


def test_generate_token_raises_TypeError(report):
    with pytest.raises(TypeError):
        report.generate_token()
