import requests

from pbipy.reports import Report


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
