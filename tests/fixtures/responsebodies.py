import pytest


@pytest.fixture
def get_dataset():
    return """
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


@pytest.fixture
def get_dataset_in_group():
    return """
    {
    "id": "cfafbeb1-8037-4d0c-896e-a46fb27ff229",
    "name": "SalesMarketing",
    "addRowsAPIEnabled": false,
    "configuredBy": "john@contoso.com",
    "isRefreshable": true,
    "isEffectiveIdentityRequired": false,
    "isEffectiveIdentityRolesRequired": false,
    "isOnPremGatewayRequired": false,
    "upstreamDatasets": []
    }
    """


@pytest.fixture
def get_datasets_in_group():
    return """
    {
    "value": [
        {
            "id": "cfafbeb1-8037-4d0c-896e-a46fb27ff229",
            "name": "SalesMarketing",
            "addRowsAPIEnabled": false,
            "configuredBy": "john@contoso.com",
            "isRefreshable": true,
            "isEffectiveIdentityRequired": false,
            "isEffectiveIdentityRolesRequired": false,
            "isOnPremGatewayRequired": false
        }
    ]
    }
    """


@pytest.fixture
def get_refresh_history():
    return """
        {
        "value": [
            {
            "refreshType": "ViaApi",
            "startTime": "2017-06-13T09:25:43.153Z",
            "endTime": "2017-06-13T09:31:43.153Z",
            "status": "Completed",
            "requestId": "9399bb89-25d1-44f8-8576-136d7e9014b1"
            },
            {
            "refreshType": "ViaApi",
            "startTime": "2017-06-13T09:25:43.153Z",
            "endTime": "2017-06-13T09:31:43.153Z",
            "serviceExceptionJson": "{\\"errorCode\\":\\"ModelRefreshFailed_CredentialsNotSpecified\\"}",
            "status": "Failed",
            "requestId": "11bf290a-346b-48b7-8973-c5df149337ff"
            }
        ]
        }
        """


@pytest.fixture
def get_dataset_to_dataflow_links_in_group():
    return """
        {
        "value": [
            {
            "datasetObjectId": "cfafbeb1-8037-4d0c-896e-a46fb27ff229",
            "dataflowObjectId": "928228ba-008d-4fd9-864a-92d2752ee5ce",
            "workspaceObjectId": "f089354e-8366-4e18-aea3-4cb4a3a50b48"
            }
        ]
        }
        """


@pytest.fixture
def get_dataset_users():
    return """
        {
        "value": [
            {
            "identifier": "john@contoso.com",
            "principalType": "User",
            "datasetUserAccessRight": "Read"
            },
            {
            "identifier": "154aef10-47b8-48c4-ab97-f0bf9d5f8fcf",
            "principalType": "Group",
            "datasetUserAccessRight": "ReadReshare"
            },
            {
            "identifier": "3d9b93c6-7b6d-4801-a491-1738910904fd",
            "principalType": "App",
            "datasetUserAccessRight": "ReadWriteReshareExplore"
            }
        ]
        }
        """


@pytest.fixture
def get_datasources():
    return """
    {
  "@odata.context": "http://api.powerbi.com/v1.0/myorg/groups/222f0f33-3abc-4a57-9f98-ff01bd2aaabb/$metadata#datasources",
  "value": [
    {
      "datasourceType": "AnalysisServices",
      "connectionDetails": {
        "server": "My-As-Server",
        "database": "My-As-Database"
      },
      "datasourceId": "33cc5222-3fb9-44f7-b19d-ffbff18aaaf5",
      "gatewayId": "0a2dafe6-0e93-4120-8d2c-fae123c111b1"
    },
    {
      "datasourceType": "AzureBlobs",
      "datasourceId": "e0315274-90b6-4fc0-abf2-2d60d448cb04",
      "gatewayId": "7f1c4e55-544b-403f-b132-da0d3a024674",
      "connectionDetails": {
        "account": "myAccount",
        "domain": "blob.core.windows.net"
      }
    },
    {
      "datasourceType": "File",
      "connectionDetails": {
        "path": "c:\\\\users\\\\username\\\\documents\\\\orders1.xlsx"
      },
      "datasourceId": "33cc5222-3fb9-44f7-b19d-ffbff18aaaf5",
      "gatewayId": "0a2dafe6-0e93-4120-8d2c-fae123c111b1"
    },
    {
      "datasourceType": "Extension",
      "datasourceId": "70540d95-4c8e-41ae-88c6-27a103b12841",
      "gatewayId": "7f1c4e55-544b-403f-b132-da0d3a024674",
      "connectionDetails": {
        "kind": "AzureDataExplorer",
        "path": "https://myserver.kusto.windows.net"
      }
    },
    {
      "datasourceType": "Exchange",
      "datasourceId": "4d126fc8-1568-46aa-ba16-ccf19b18f012",
      "gatewayId": "7f1c4e55-544b-403f-b132-da0d3a024674",
      "connectionDetails": {
        "emailAddress": "john@contoso.com"
      }
    },
    {
      "datasourceType": "OData",
      "connectionDetails": {
        "url": "http://services.odata.org/MyOdata/MyOdata.svc"
      },
      "datasourceId": "33cc5222-3fb9-44f7-b19d-ffbff18aaaf5",
      "gatewayId": "0a2dafe6-0e93-4120-8d2c-fae123c111b1"
    },
    {
      "datasourceType": "Oracle",
      "connectionDetails": {
        "server": "My-Oracle-Server",
        "database": "My-Oracle-Database"
      },
      "datasourceId": "33cc5222-3fb9-44f7-b19d-ffbff18aaaf5",
      "gatewayId": "0a2dafe6-0e93-4120-8d2c-fae123c111b1"
    },
    {
      "datasourceType": "Salesforce",
      "datasourceId": "e8a6e0f5-b244-402a-ba5a-4d578609ede3",
      "gatewayId": "7f1c4e55-544b-403f-b132-da0d3a024674",
      "connectionDetails": {
        "classInfo": "report-detail",
        "loginServer": "https://login.salesforce.com/"
      }
    },
    {
      "datasourceType": "SAPHana",
      "connectionDetails": {
        "server": "My-SapHana-Server",
        "database": "My-SapHana-Database"
      },
      "datasourceId": "33cc5222-3fb9-44f7-b19d-ffbff18aaaf5",
      "gatewayId": "0a2dafe6-0e93-4120-8d2c-fae123c111b1"
    },
    {
      "datasourceType": "SharePointList",
      "connectionDetails": {
        "url": "https://microsoft.sharepoint.com/hello/myproj/"
      },
      "datasourceId": "33cc5222-3fb9-44f7-b19d-ffbff18aaaf5",
      "gatewayId": "0a2dafe6-0e93-4120-8d2c-fae123c111b1"
    },
    {
      "datasourceType": "Sql",
      "connectionDetails": {
        "server": "My-As-Server",
        "database": "My-As-Database"
      },
      "datasourceId": "33cc5222-3fb9-44f7-b19d-ffbff18aaaf5",
      "gatewayId": "0a2dafe6-0e93-4120-8d2c-fae123c111b1"
    }
  ]
}
    """


@pytest.fixture
def get_direct_query_refresh_schedule():
    return """
  {
  "days": [
    "Sunday",
    "Friday",
    "Saturday"
  ],
  "times": [
    "05:00",
    "11:30",
    "17:30",
    "23:00"
  ],
  "localTimeZoneId": "UTC"
  }
  """


@pytest.fixture
def get_parameters():
    return """
  {
  "value": [
    {
      "name": "ServerName",
      "type": "Text",
      "isRequired": true,
      "currentValue": "MyTest.database.windows.net"
    },
    {
      "name": "DatabaseName",
      "type": "Text",
      "isRequired": true,
      "currentValue": "MyTestDB"
    },
    {
      "name": "FromDate",
      "type": "DateTime",
      "isRequired": true,
      "currentValue": "2/8/2002 12:00:00 AM"
    },
    {
      "name": "FilterBlanks",
      "type": "Logical",
      "isRequired": true,
      "currentValue": "TRUE"
    },
    {
      "name": "MaxId",
      "type": "Number",
      "isRequired": true,
      "currentValue": "77"
    },
    {
      "name": "AnyParam",
      "type": "Any",
      "isRequired": true,
      "currentValue": "uu63"
    }
  ]
  }
  """


@pytest.fixture
def get_app():
    return """
    {
      "id": "f089354e-8366-4e18-aea3-4cb4a3a50b48",
      "description": "The finance app",
      "name": "Finance",
      "publishedBy": "Bill",
      "lastUpdate": "2019-01-13T09:46:53.094+02:00",
      "workspaceId": "3d9b93c6-7b6d-4801-a491-1738910904fd",
      "users":[]
    }
    """


@pytest.fixture
def get_apps():
    return """
    {
    "value": [
      {
        "id": "f089354e-8366-4e18-aea3-4cb4a3a50b48",
        "description": "The finance app",
        "name": "Finance",
        "publishedBy": "Bill",
        "lastUpdate": "2019-01-13T09:46:53.094+02:00"
      },
      {
        "id": "3d9b93c6-7b6d-4801-a491-1738910904fd",
        "description": "The marketing app",
        "name": "Marketing",
        "publishedBy": "Ben",
        "lastUpdate": "2018-11-13T09:46:53.094+02:00"
      }
    ]
  }
    """


@pytest.fixture
def get_reports():
    return """
    {
    "value": [
      {
        "appId": "3d9b93c6-7b6d-4801-a491-1738910904fd",
        "datasetId": "cfafbeb1-8037-4d0c-896e-a46fb27ff229",
        "id": "66b2570c-d9d3-40b2-83d9-1095c6700041",
        "name": "SalesMarketing",
        "webUrl": "https://app.powerbi.com/reports/66b2570c-d9d3-40b2-83d9-1095c6700041",
        "embedUrl": "https://app.powerbi.com/reportEmbed?reportId=66b2570c-d9d3-40b2-83d9-1095c6700041&appId=3d9b93c6-7b6d-4801-a491-1738910904fd&config=eyJjbHVzdGVyVXJsIjoiaHR0cHM6Ly9XQUJJLVNPVVRILUNFTlRSQUwtVVMtcmVkaXJlY3QuYW5hbHlzaXMud2luZG93cy5uZXQifQ"
      },
      {
        "appId": "3d9b93c6-7b6d-4801-a491-1738910904fd",
        "datasetId": "cfafbeb1-8037-4d0c-896e-a46fb27ff229",
        "id": "5b218778-e7a5-4d73-8187-f10824047715",
        "name": "MarketingSales",
        "webUrl": "https://app.powerbi.com/reports/5b218778-e7a5-4d73-8187-f10824047715",
        "embedUrl": "https://app.powerbi.com/reportEmbed?reportId=5b218778-e7a5-4d73-8187-f10824047715&appId=3d9b93c6-7b6d-4801-a491-1738910904fd&config=eyJjbHVzdGVyVXJsIjoiaHR0cHM6Ly9XQUJJLVNPVVRILUNFTlRSQUwtVVMtcmVkaXJlY3QuYW5hbHlzaXMud2luZG93cy5uZXQifQ",
        "isOwnedByMe": false,
        "users": [],
        "subscriptions": []
      }
    ]
  }
  """
