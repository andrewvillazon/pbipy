import json

import pytest

from pbipy.models import App, Dashboard, Dataset, DatasetRefreshDetail, Gateway, Group, Refresh, Report, Tile


@pytest.fixture
def refresh_from_raw():
    raw = {
        "refreshType": "ViaApi",
        "startTime": "2017-06-13T09:25:43.153Z",
        "endTime": "2017-06-13T09:31:43.153Z",
        "serviceExceptionJson": '{"errorCode":"ModelRefreshFailed_CredentialsNotSpecified"}',
        "status": "Failed",
        "requestId": "11bf290a-346b-48b7-8973-c5df149337ff",
    }

    return Refresh.from_raw(raw=raw)


@pytest.fixture
def group_from_raw():
    raw = {
        "id": "3d9b93c6-7b6d-4801-a491-1738910904fd",
        "isReadOnly": False,
        "isOnDedicatedCapacity": False,
        "name": "marketing group",
    }

    return Group.from_raw(raw=raw)


@pytest.fixture
def dataset_from_raw():
    raw = {
        "id": "cfafbeb1-8037-4d0c-896e-a46fb27ff229",
        "name": "SalesMarketing",
        "addRowsAPIEnabled": False,
        "configuredBy": "john@contoso.com",
        "isRefreshable": True,
        "isEffectiveIdentityRequired": True,
        "isEffectiveIdentityRolesRequired": True,
        "isOnPremGatewayRequired": False,
        "createdDate": "2017-06-13T09:25:43.153Z",
    }

    return Dataset.from_raw(raw=raw)


@pytest.fixture
def group():
    return Group(id="3d9b93c6-7b6d-4801-a491-1738910904fd", name="marketing group")


@pytest.fixture
def dataset():
    js = json.loads(
        """
        {
        "id": "cfafbeb1-8037-4d0c-896e-a46fb27ff229",
        "name": "SalesMarketing",
        "addRowsAPIEnabled": false,
        "configuredBy": "john@contoso.com",
        "isRefreshable": true,
        "isEffectiveIdentityRequired": true,
        "isEffectiveIdentityRolesRequired": true,
        "isOnPremGatewayRequired": false
        }
        """
    )
    return Dataset.from_raw(js)


@pytest.fixture
def dataset_not_refreshable():
    js = json.loads(
        """
        {
        "id": "cfafbeb1-8037-4d0c-896e-a46fb27ff229",
        "name": "SalesMarketing",
        "addRowsAPIEnabled": false,
        "configuredBy": "john@contoso.com",
        "isRefreshable": false,
        "isEffectiveIdentityRequired": true,
        "isEffectiveIdentityRolesRequired": true,
        "isOnPremGatewayRequired": false
        }
        """
    )
    return Dataset.from_raw(js)


@pytest.fixture
def app_from_raw():
    js = json.loads(
        """
        {
        "id": "3d9b93c6-7b6d-4801-a491-1738910904fd",
        "description": "The marketing app",
        "name": "Marketing",
        "publishedBy": "Ben",
        "lastUpdate": "2018-11-13T09:46:53.094+02:00"
        }
    """
    )

    return App.from_raw(js)


@pytest.fixture
def report_from_raw():
    js = json.loads(
        """
    {
    "appId": "3d9b93c6-7b6d-4801-a491-1738910904fd",
    "datasetId": "cfafbeb1-8037-4d0c-896e-a46fb27ff229",
    "id": "66b2570c-d9d3-40b2-83d9-1095c6700041",
    "name": "SalesMarketing",
    "description":"The Sales and Marketing App",
    "isOwnedByMe": true,
    "webUrl": "https://app.powerbi.com/reports/66b2570c-d9d3-40b2-83d9-1095c6700041",
    "embedUrl": "https://app.powerbi.com/reportEmbed?reportId=66b2570c-d9d3-40b2-83d9-1095c6700041&appId=3d9b93c6-7b6d-4801-a491-1738910904fd&config=eyJjbHVzdGVyVXJsIjoiaHR0cHM6Ly9XQUJJLVNPVVRILUNFTlRSQUwtVVMtcmVkaXJlY3QuYW5hbHlzaXMud2luZG93cy5uZXQifQ",
    "users":[]
    }
    """
    )

    return Report.from_raw(js)


@pytest.fixture
def dashboard_from_raw():
    js = json.loads(
        """
        {
        "appId": "3d9b93c6-7b6d-4801-a491-1738910904fd",
        "id": "03dac094-2ff8-47e8-b2b9-dedbbc4d22ac",
        "displayName": "SalesMarketing",
        "embedUrl": "https://app.powerbi.com/dashboardEmbed?dashboardId=335aee4b-7b38-48fd-9e2f-306c3fd67482&appId=3d9b93c6-7b6d-4801-a491-1738910904fd&config=eyJjbHVzdGVyVXJsIjoiaHR0cHM6Ly9XQUJJLVNPVVRILUNFTlRSQUwtVVMtcmVkaXJlY3QuYW5hbHlzaXMud2luZG93cy5uZXQifQ%3d%3d",
        "isReadOnly": false,
        "users": [],
        "subscriptions": []
        }
        """
    )

    return Dashboard.from_raw(js)


@pytest.fixture
def tile_from_raw():
    js = json.loads(
        """
        {
        "id": "312fbfe9-2eda-44e0-9ed0-ab5dc571bb4b",
        "title": "SalesMarketingTile",
        "embedUrl": "https://app.powerbi.com/embed?dashboardId=69ffaa6c-b36d-4d01-96f5-1ed67c64d4af&tileId=312fbfe9-2eda-44e0-9ed0-ab5dc571bb4b&groupId=f089354e-8366-4e18-aea3-4cb4a3a50b48",
        "rowSpan": 0,
        "colSpan": 0,
        "reportId": "5b218778-e7a5-4d73-8187-f10824047715",
        "datasetId": "cfafbeb1-8037-4d0c-896e-a46fb27ff229"
    }
        """
    )

    return Tile.from_raw(js)

@pytest.fixture
def gateway_from_raw():
    js = json.loads(
        """
        {
        "id": "1f69e798-5852-4fdd-ab01-33bb14b6e934",
        "name": "My_Sample_Gateway",
        "type": "Resource",
        "publicKey": {
            "exponent": "AQAB",
            "modulus": "o6j2....cLk="
            }
        }
        """
    )

    return Gateway.from_raw(js)


@pytest.fixture
def dataset_refresh_detail_200_status_code_from_raw():
    js = json.loads("""
    {
        "startTime": "2021-12-10T08:40:31.57",
        "endTime": "2021-12-10T08:40:43.87",
        "type": "Full",
        "commitMode": "Transactional",
        "status": "Completed",
        "extendedStatus": "Completed",
        "currentRefreshType": "Full",
        "numberOfAttempts": 0,
        "objects": [
            {
            "table": "DateTableTemplate_78e78207-b3fb-41b5-8b95-e5efca989067",
            "partition": "DateTableTemplate_78e78207-b3fb-41b5-8b95-e5efca989067-ae306fb4-3b7e-4a41-824d-cb3b452fedfc",
            "status": "Completed"
            },
            {
            "table": "LocalDateTable_e9d8a66b-4018-4d16-be8c-402b2037c051",
            "partition": "LocalDateTable_e9d8a66b-4018-4d16-be8c-402b2037c051-59bc07f8-85c9-456a-ad36-18e1de4d77ed",
            "status": "Completed"
            },
            {
            "table": "LocalDateTable_55935f6b-04d1-4cfe-8856-ed9f9e73ab2e",
            "partition": "LocalDateTable_55935f6b-04d1-4cfe-8856-ed9f9e73ab2e-d95ae7f7-19c9-48a8-9c16-fcab26558bc2",
            "status": "Completed"
            },
            {
            "table": "LocalDateTable_ff25f80e-eb04-4229-986d-b40223c04f1c",
            "partition": "LocalDateTable_ff25f80e-eb04-4229-986d-b40223c04f1c-6606fc4c-4cda-49e1-8acd-e55a6ec36cb3",
            "status": "Completed"
            },
            {
            "table": "DimCurrency",
            "partition": "DimCurrency-e5524cc4-a898-433b-91aa-c001b9a6d676",
            "status": "Completed"
            },
            {
            "table": "DimCustomer",
            "partition": "DimCustomer-a31bbd93-e20a-4dee-a33c-7afa27785953",
            "status": "Completed"
            },
            {
            "table": "LocalDateTable_fa65a206-f320-4d5d-abcc-1dc0f051ca7d",
            "partition": "LocalDateTable_fa65a206-f320-4d5d-abcc-1dc0f051ca7d-06a48a0a-a32b-48a3-b113-924aafd6363c",
            "status": "Completed"
            },
            {
            "table": "LocalDateTable_78a4e1b7-a2e5-4bbf-ab68-7c87961b68a2",
            "partition": "LocalDateTable_78a4e1b7-a2e5-4bbf-ab68-7c87961b68a2-5b3ba715-7c84-4e52-b310-485b93cfbe6d",
            "status": "Completed"
            },
            {
            "table": "DimDate",
            "partition": "DimDate-62e2f91b-53e5-4ed3-8618-fec74dba5e0d",
            "status": "Completed"
            },
            {
            "table": "LocalDateTable_e72c294f-0a06-4051-b943-e6bf8389e2c3",
            "partition": "LocalDateTable_e72c294f-0a06-4051-b943-e6bf8389e2c3-891a0e68-d414-4ba3-9c4b-e6f1ec73d4f3",
            "status": "Completed"
            },
            {
            "table": "DimProduct",
            "partition": "DimProduct-3d07cc89-2bd7-4a98-bb37-3368c1562f98",
            "status": "Completed"
            },
            {
            "table": "LocalDateTable_e37e4431-8c1a-449c-8796-b704df200a92",
            "partition": "LocalDateTable_e37e4431-8c1a-449c-8796-b704df200a92-8596ebb8-418f-4e50-a921-dac88c6f1339",
            "status": "Completed"
            },
            {
            "table": "LocalDateTable_73faffeb-a0c7-4ea1-83dc-530823b0fea0",
            "partition": "LocalDateTable_73faffeb-a0c7-4ea1-83dc-530823b0fea0-13795c4e-708f-4ddc-8ea3-5a2f39ae2253",
            "status": "Completed"
            },
            {
            "table": "DimPromotion",
            "partition": "DimPromotion-21e6c333-430e-4350-8c94-cdceb362c4c7",
            "status": "Completed"
            },
            {
            "table": "LocalDateTable_9c19746b-db7d-4b7e-b95d-c66e4b8fefc8",
            "partition": "LocalDateTable_9c19746b-db7d-4b7e-b95d-c66e4b8fefc8-395de144-ad53-41c0-9ec0-68bab6158d99",
            "status": "Completed"
            },
            {
            "table": "LocalDateTable_d96435dd-6110-4246-996c-616c96125e71",
            "partition": "LocalDateTable_d96435dd-6110-4246-996c-616c96125e71-891737ee-c46c-4b9f-bfa8-e4555004e20f",
            "status": "Completed"
            },
            {
            "table": "DimSalesTerritory",
            "partition": "DimSalesTerritory-6d88f938-13d5-49f8-899c-d11b3d346ad5",
            "status": "Completed"
            },
            {
            "table": "FactInternetSales",
            "status": "Completed"
            }
        ]
    }
    """)

    return DatasetRefreshDetail.from_raw(js)


@pytest.fixture
def dataset_refresh_detail_202_status_code_from_raw():
    js = json.loads("""
    {
        "startTime": "2021-12-14T03:46:04.833",
        "type": "Full",
        "commitMode": "Transactional",
        "status": "Unknown",
        "extendedStatus": "NotStarted",
        "currentRefreshType": "Full",
        "numberOfAttempts": 0
        }
    """)

    return DatasetRefreshDetail.from_raw(js)